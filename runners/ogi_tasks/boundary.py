"""Trusted grading boundary for executed code tasks: the candidate's own output can never authorize its correctness.

    grader   (grade(), trusted)        picks the tests, reads only the evaluator's report, owns the verdict
    evaluator (`python -I boundary.py evaluate`, trusted subprocess, not sandboxed)
                                       execs the dataset's test module and runs each selected test with unittest;
                                       the entry point in the test namespace is a proxy; decides pass/fail per test
    candidate (`boundary.py serve` under bwrap, untrusted, fresh process + fresh dir per test)
                                       holds candidate.py and this file only; receives (args, kwargs) per call and
                                       never sees the test source, the answer registry, the data dir or the verdict

Values cross as one tagged-JSON line per message and are rebuilt by the evaluator into plain builtins
(None/bool/int/float/str/bytes/list/tuple/dict/set/frozenset), so the assertions only ever compare plain data,
never a candidate object with its own __eq__. Other return types are UNSERIALIZABLE. Exceptions cross by name:
a builtin Exception subclass is re-raised as that class, any other name as CandidateError; nothing the
candidate sends can raise SystemExit/KeyboardInterrupt/SkipTest in the evaluator. Any boundary fault during a
test (timeout, crash/EOF, malformed or oversized message, unserializable value) fails that test regardless of
what unittest concluded, so `assertRaises(Exception)` cannot be satisfied by crashing.

Rejected for confirmatory grading: the shared-process variant ("per-test subprocess, verdict derived only by
the trusted parent from a structured outcome"). Candidate and test still share one interpreter there, so the
candidate can patch unittest/TestCase.assert*, rewrite the test function objects or the expected values in
the test module's globals, replace the outcome serializer, or write the structured outcome itself and
os._exit(0) before the real one is emitted. The parent only sees bytes the candidate could have produced, so
the verdict remains candidate-authored. That variant is what the old HARNESS did; it is removed.
"""
from __future__ import annotations

import base64
import builtins
import json
import math
import os
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

MAX_MSG = 16 << 20          # bytes per message line
MAX_DEPTH = 64
CALL_TIMEOUT_DEFAULT = 60.0


# ---------------------------------------------------------------- codec (used on both sides; only dec() is trusted)
def enc(x, depth: int = 0):
    if depth > MAX_DEPTH:
        raise TypeError("UNSERIALIZABLE:too-deep")
    t, d = type(x), depth + 1
    if x is None or t in (bool, int, str):
        return x
    if t is float:
        return x if math.isfinite(x) else {"$": "float", "v": repr(x)}
    if t is list:
        return [enc(i, d) for i in x]
    if t in (tuple, set, frozenset):
        return {"$": t.__name__, "v": [enc(i, d) for i in x]}
    if t is bytes:
        return {"$": "bytes", "v": base64.b64encode(x).decode()}
    if t is dict:
        return {"$": "dict", "v": [[enc(k, d), enc(v, d)] for k, v in x.items()]}
    raise TypeError(f"UNSERIALIZABLE:{t.__module__}.{t.__qualname__}")


_COLL = {"tuple": tuple, "set": set, "frozenset": frozenset}


def dec(x, depth: int = 0):
    """Strict inverse of enc on json.loads output; anything else is MALFORMED. Returns plain builtins only."""
    if depth > MAX_DEPTH:
        raise ValueError("MALFORMED:too-deep")
    t, d = type(x), depth + 1
    if x is None or t in (bool, int, str, float):
        return x
    if t is list:
        return [dec(i, d) for i in x]
    if t is dict and set(x) == {"$", "v"}:
        tag, v = x["$"], x["v"]
        if tag == "float" and v in ("nan", "inf", "-inf"):
            return float(v)
        if tag in _COLL and type(v) is list:
            return _COLL[tag](dec(i, d) for i in v)
        if tag == "bytes" and type(v) is str:
            return base64.b64decode(v, validate=True)
        if tag == "dict" and type(v) is list and all(type(p) is list and len(p) == 2 for p in v):
            return {dec(k, d): dec(val, d) for k, val in v}
    raise ValueError("MALFORMED:untagged-or-unknown")


# ---------------------------------------------------------------- untrusted side (runs inside the sandbox)
def serve(entry: str) -> None:
    chan = os.fdopen(os.dup(1), "w")
    os.dup2(2, 1)                                   # candidate prints go to stderr, not onto the channel

    def send(msg):
        chan.write(json.dumps(msg) + "\n")
        chan.flush()

    requests, sys.stdin = sys.stdin, open(os.devnull)
    ns = {"__name__": "__candidate__"}
    try:
        with open("candidate.py") as f:
            exec(compile(f.read(), "candidate.py", "exec"), ns)
        fn = ns[entry]
    except BaseException as e:
        return send({"load_error": type(e).__name__})
    send({"ready": True})
    for line in requests:
        req = json.loads(line)
        try:
            r = fn(*dec(req["args"]), **dec(req["kwargs"]))
        except BaseException as e:
            send({"raise": type(e).__name__, "msg": str(e)[:500]})
            continue
        try:
            send({"ok": enc(r)})
        except (TypeError, ValueError, RecursionError) as e:
            send({"unserializable": str(e)[:200]})


# ---------------------------------------------------------------- trusted side
class CandidateError(Exception):
    """A non-builtin exception raised by the candidate (only its class name crosses the boundary)."""


class BoundaryFault(BaseException):
    """Timeout, crash, malformed/oversized message or unserializable value. BaseException so that no
    assertRaises(Exception) in a test can swallow it; the evaluator also fails the test outright."""


def _exc_class(name: str):
    c = getattr(builtins, name, None) if type(name) is str else None
    return c if isinstance(c, type) and issubclass(c, Exception) else CandidateError


class Candidate:
    """One sandboxed candidate process for one test."""

    def __init__(self, code: str, entry: str, *, python: str, timeout: float, mem_mb: int, confirmatory: bool,
                 allow_unsandboxed: bool):
        import sandbox  # noqa: PLC0415  (evaluator puts this directory on sys.path)
        self.deadline, self.dead = time.monotonic() + timeout, None
        self.dir = tempfile.mkdtemp(prefix="ogi-cand-")
        with open(os.path.join(self.dir, "candidate.py"), "w") as f:
            f.write(code)
        shutil.copy(__file__, os.path.join(self.dir, "boundary.py"))
        cmd, self.isolation = sandbox.wrap(["boundary.py", "serve", entry], self.dir, python, confirmatory=confirmatory,
                                           allow_unsandboxed=allow_unsandboxed and not confirmatory)
        self.err = tempfile.TemporaryFile()
        self.p = subprocess.Popen(cmd, cwd=self.dir, env=sandbox.env(self.dir), stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=self.err, start_new_session=True,
                                  preexec_fn=lambda: sandbox.limits(int(timeout) + 1, mem_mb))
        self.buf = b""
        hello = self._recv()
        le = hello.get("load_error")
        self.load_error = None if hello == {"ready": True} else (le[:100] if type(le) is str else "MALFORMED_HELLO")

    def _fault(self, kind: str):
        self.dead = self.dead or kind
        self.close()
        raise BoundaryFault(kind)

    def _recv(self) -> dict:
        fd = self.p.stdout.fileno()
        while b"\n" not in self.buf:
            left = self.deadline - time.monotonic()
            if left <= 0 or not select.select([fd], [], [], left)[0]:
                self._fault("TIMEOUT")
            chunk = os.read(fd, 1 << 16)
            if not chunk:
                self._fault("CRASH_EOF")
            self.buf += chunk
            if len(self.buf) > MAX_MSG:
                self._fault("OVERSIZED")
        line, self.buf = self.buf.split(b"\n", 1)
        try:
            msg = json.loads(line)
        except (ValueError, RecursionError):
            self._fault("MALFORMED")
        if type(msg) is not dict:
            self._fault("MALFORMED")
        return msg

    def call(self, args: tuple, kwargs: dict):
        if self.dead:
            raise BoundaryFault(self.dead)
        try:
            line = (json.dumps({"args": enc(list(args)), "kwargs": enc(kwargs)}) + "\n").encode()
        except (TypeError, ValueError) as e:
            raise BoundaryFault(f"UNSERIALIZABLE_ARGUMENT:{e}") from None
        fd = self.p.stdin.fileno()
        os.set_blocking(fd, False)
        while line:
            left = self.deadline - time.monotonic()
            if left <= 0 or not select.select([], [fd], [], left)[1]:
                self._fault("TIMEOUT")
            try:
                line = line[os.write(fd, line):]
            except BlockingIOError:
                continue
            except BrokenPipeError:
                self._fault("CRASH_EOF")
        msg = self._recv()
        keys = set(msg)
        if keys == {"ok"}:
            try:
                return dec(msg["ok"])
            except (ValueError, TypeError, RecursionError):
                self._fault("MALFORMED")
        if keys == {"raise", "msg"} and type(msg["msg"]) is str:
            raise _exc_class(msg["raise"])(msg["msg"])  # the candidate's own exception, as plain builtin class
        if keys == {"unserializable"}:                  # the type name is candidate-reported: evidence text only
            self._fault("UNSERIALIZABLE_RETURN:" + str(msg["unserializable"]).removeprefix("UNSERIALIZABLE:")[:100])
        self._fault("MALFORMED")

    def stderr_tail(self) -> str:
        self.err.seek(0, 2)
        self.err.seek(max(0, self.err.tell() - 1500))
        return self.err.read().decode(errors="replace")

    def close(self):
        if self.p.poll() is None:
            try:
                os.killpg(self.p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.p.wait()
        shutil.rmtree(self.dir, ignore_errors=True)


def harness_namespace(code_prompt: str, entry: str) -> dict:
    """The dataset's own prelude (imports/constants from code_prompt, trusted text) without the entry stub."""
    import ast  # noqa: PLC0415
    tree = ast.parse(code_prompt + "    pass\n")
    tree.body = [n for n in tree.body if not (isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == entry)]
    ns = {"__name__": "__ogi_tests__"}
    exec(compile(tree, "<code_prompt>", "exec"), ns)
    return ns


def evaluate(spec: dict) -> dict:
    """Run spec["names"] from spec["test_src"] against spec["code"] behind the boundary. Trusted."""
    per, faults, load_error, isolation, tail = {}, {}, None, None, ""
    try:
        ns = harness_namespace(spec.get("code_prompt") or "", spec["entry"])
        holder = {}

        def proxy(*args, **kwargs):
            c = holder["c"]
            try:
                return c.call(args, kwargs)
            except BoundaryFault as f:
                holder["faults"].append(str(f))
                raise

        ns[spec["entry"]] = proxy
        exec(compile(spec["test_src"], "<tests>", "exec"), ns)
    except BaseException as e:   # noqa: BLE001 - the dataset prelude/test module itself failed (environment)
        return {"per_test": dict.fromkeys(spec["names"], False), "setup_error": f"{type(e).__name__}: {e}"[:300]}
    for name in spec["names"]:
        holder["faults"] = []
        if load_error is not None:
            per[name] = False
            continue
        try:
            c = holder["c"] = Candidate(spec["code"], spec["entry"], python=spec["python"], timeout=spec["timeout"],
                                        mem_mb=spec["mem_mb"], confirmatory=spec["confirmatory"],
                                        allow_unsandboxed=spec["allow_unsandboxed"])
        except BoundaryFault as f:
            per[name], faults[name] = False, [str(f)]
            continue
        isolation = c.isolation
        try:
            if c.load_error is not None:
                load_error, per[name] = c.load_error, False
                continue
            cls, meth = name.split(".")
            r = unittest.TestResult()
            try:
                unittest.TestSuite([ns[cls](meth)]).run(r)     # suite, so setUpClass/tearDownClass run
            except BoundaryFault:
                pass
            per[name] = (r.testsRun == 1 and r.wasSuccessful() and not r.skipped and not r.expectedFailures
                         and not holder["faults"])
            if holder["faults"]:
                faults[name] = holder["faults"]
        finally:
            c.close()
            tail = c.stderr_tail()
    return {"per_test": per, "faults": faults, "load_error": load_error, "isolation": isolation,
            "candidate_stderr_tail": tail}


def main() -> None:
    if sys.argv[1] == "serve":
        return serve(sys.argv[2])
    out = os.fdopen(os.dup(1), "w")                 # the report channel; dataset tests that print go to stderr
    os.dup2(2, 1)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    out.write(json.dumps(evaluate(json.load(sys.stdin))))
    out.flush()
    os._exit(0)                                     # skip interpreter teardown of whatever the dataset tests left


if __name__ == "__main__":
    main()
