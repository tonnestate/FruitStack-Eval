"""Trusted grading boundary for executed code tasks: the candidate's own output can never authorize its correctness.

    grader   (grade(), trusted)        picks the tests, reads only the evaluator's report, owns the verdict
    evaluator (`python -I boundary.py evaluate`, trusted subprocess, not sandboxed)
                                       execs the dataset's test module and runs each selected test with unittest;
                                       the entry point in the test namespace is a proxy; decides pass/fail per test
    candidate (`boundary.py serve` under bwrap, untrusted, fresh process + fresh dir per test)
                                       holds candidate.py and this file only; receives (args, kwargs) per call and
                                       never sees the test source, the answer registry, the data dir or the verdict

Values cross as one tagged-JSON line per message and are rebuilt by the evaluator into plain builtins
(None/bool/int/float/complex/str/bytes/list/tuple/dict/set/frozenset) or, for the declared numpy/pandas forms
below, into fresh objects built by the EVALUATOR's own numpy/pandas out of those plain builtins. The
assertions therefore never see a candidate class or a candidate __eq__. Other return types are
UNSERIALIZABLE. Exceptions cross by name:
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
import re
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
    if t is complex:
        return {"$": "complex", "v": [enc(x.real, d), enc(x.imag, d)]}
    if t is dict:
        return {"$": "dict", "v": [[enc(k, d), enc(v, d)] for k, v in x.items()]}
    if t.__module__.split(".")[0] in ("numpy", "pandas"):
        return _enc_sci(x, d)
    raise TypeError(f"UNSERIALIZABLE:{t.__module__}.{t.__qualname__}")


_COLL = {"tuple": tuple, "set": set, "frozenset": frozenset}


def dec(x, depth: int = 0):
    """Strict inverse of enc on json.loads output; anything else is MALFORMED.

    Returns plain builtins, or - for the numpy/pandas tags - an object freshly built by THIS process's
    numpy/pandas from plain builtins (see the _SCI block). Never unpickles, evals, imports a candidate-named
    module, or touches a candidate class."""
    if depth > MAX_DEPTH:
        raise ValueError("MALFORMED:too-deep")
    t, d = type(x), depth + 1
    if x is None or t in (bool, int, str, float):
        return x
    if t is list:
        return [dec(i, d) for i in x]
    if t is dict and type(x.get("$")) is str:
        tag, keys = x["$"], set(x)
        if keys == {"$", "v"}:
            v = x["v"]
            if tag == "float" and v in ("nan", "inf", "-inf"):
                return float(v)
            if tag in _COLL and type(v) is list:
                return _COLL[tag](dec(i, d) for i in v)
            if tag == "bytes" and type(v) is str:
                return base64.b64decode(v, validate=True)
            if tag == "complex" and type(v) is list and len(v) == 2:
                re_, im = (dec(i, d) for i in v)
                if type(re_) in (int, float) and type(im) in (int, float):
                    return complex(re_, im)
            if tag == "dict" and type(v) is list and all(type(p) is list and len(p) == 2 for p in v):
                return {dec(k, d): dec(val, d) for k, val in v}
        if tag in _SCI and keys == _SCI[tag][0]:
            return _SCI[tag][1](x, d)
    raise ValueError("MALFORMED:untagged-or-unknown")


# ---------------------------------------------------------------- numpy / pandas values (one declared form)
# WHAT CROSSES, in both directions (test arguments as well as candidate return values):
#   numpy scalars      -> the plain Python value (np.int64(3) arrives as 3, np.float64 as float, ...)
#   numpy.ndarray      -> {dtype: numpy dtype.str, shape: [int], v: [flat plain values]}
#   pandas.Series      -> {dtype, name, index, v}    Index/DatetimeIndex/TimedeltaIndex -> {dtype, name, v},
#   pandas.DataFrame   -> {columns, index, dtypes, v: [column-major plain values]}      RangeIndex -> {range, name}
#   complex numbers (as two floats), plus everything enc already took.
# Only bool/int/uint/float/complex/str/bytes/object and tz-naive datetime64/timedelta64 dtypes cross (_DTYPE_OK
# on dtype.str); every leaf value is a plain builtin from .tolist(), except datetime64/timedelta64, which cross
# as their exact int64 counts under the declared dtype - no date string is written or parsed anywhere.
# WHAT DOES NOT CROSS - it raises UNSERIALIZABLE and the task stays INELIGIBLE with that reason:
#   matplotlib Axes/Figure and every other third-party object (sklearn models, WordCloud, Voronoi, ...);
#   datetime.datetime/date/timedelta and pandas Timestamp/Timedelta/NaT scalars; tz-aware datetimes and every
#   other pandas extension dtype (category, nullable Int64/boolean/string); MultiIndex, CategoricalIndex and
#   every other non-flat index; structured/void numpy dtypes; and any container holding one of those.
#   A DatetimeIndex's `freq` is not data and does not cross, so a test that compares freq keeps its task out.
# INTEGRITY: the trusted side rebuilds these with its OWN numpy/pandas from plain builtins only - no pickle, no
# eval, no candidate module import, no candidate class, no candidate __eq__/__reduce__ ever runs in the
# evaluator. A dtype is accepted only as a string matching _DTYPE_OK; shapes/lengths must agree with the data
# actually sent (so a declared 2**40-element array cannot allocate anything), and the 16 MiB message cap plus
# MAX_DEPTH bound the rest. Unknown tags and unknown key sets are MALFORMED, which fails the test.
_DTYPE_OK = re.compile(r"^[<>|]([biufcOUS]\d*|[Mm]8\[(Y|M|W|D|h|m|s|ms|us|ns|ps|fs|as)\])$")
# numpy dtype.str: bool/int/uint/float/complex/object/str/bytes, plus tz-naive datetime64/timedelta64


def _dtype_str(dt) -> str:
    import numpy as np  # noqa: PLC0415
    if not isinstance(dt, np.dtype) or not _DTYPE_OK.match(dt.str):   # pandas extension dtypes are not np.dtype
        raise TypeError(f"UNSERIALIZABLE:dtype.{dt}")
    return dt.str


def _ix_types():
    import pandas as pd  # noqa: PLC0415
    return (pd.Index, pd.RangeIndex, pd.DatetimeIndex, pd.TimedeltaIndex)   # flat indexes only


def _enc_index(ix, d) -> dict:
    import pandas as pd  # noqa: PLC0415
    if type(ix) is pd.RangeIndex:
        return {"range": [ix.start, ix.stop, ix.step], "name": enc(ix.name, d)}
    if type(ix) not in _ix_types():     # MultiIndex, CategoricalIndex, ... (a tz-aware one fails on its dtype)
        raise TypeError(f"UNSERIALIZABLE:pandas.{type(ix).__qualname__}")
    # a DatetimeIndex/TimedeltaIndex loses its `freq` here (it is not data); a test that compares freq
    # therefore fails under the boundary and keeps the task INELIGIBLE rather than comparing something else.
    return {"dtype": _dtype_str(ix.dtype), "name": enc(ix.name, d), "v": _vals(ix.to_numpy(), d)}


def _vals(a, d) -> list:
    """The flat plain values of one numpy array. datetime64/timedelta64 cross as their exact int64 counts
    under the (declared) dtype, so no date string is ever written or parsed; NaT is just its int64 sentinel."""
    a = a.ravel()
    if a.dtype.kind in "Mm":
        return a.view("<i8").tolist()
    return [enc(i, d) for i in a.tolist()]


def _enc_sci(x, d):
    import numpy as np  # noqa: PLC0415
    if isinstance(x, np.generic):                       # numpy scalar -> its plain Python value
        if x.dtype.kind in "Mm":                        # ... except datetime64/timedelta64: int64 + dtype
            return {"$": "ndarray", "dtype": _dtype_str(x.dtype), "shape": [], "v": _vals(np.asarray(x), d)}
        return enc(x.item(), d)
    if type(x) is np.ndarray:
        return {"$": "ndarray", "dtype": _dtype_str(x.dtype), "shape": list(x.shape), "v": _vals(x, d)}
    import pandas as pd  # noqa: PLC0415
    if type(x) is pd.Series:
        return {"$": "series", "dtype": _dtype_str(x.dtype), "name": enc(x.name, d),
                "index": _enc_index(x.index, d), "v": _vals(x.to_numpy(), d)}
    if type(x) is pd.DataFrame:
        return {"$": "dataframe", "columns": [enc(c, d) for c in x.columns.tolist()],
                "index": _enc_index(x.index, d), "dtypes": [_dtype_str(t) for t in x.dtypes],
                "v": [_vals(x.iloc[:, j].to_numpy(), d) for j in range(x.shape[1])]}
    if type(x) in _ix_types():
        return {"$": "index", "v": _enc_index(x, d)}
    raise TypeError(f"UNSERIALIZABLE:{type(x).__module__}.{type(x).__qualname__}")


def _dec_dtype(s):
    import numpy as np  # noqa: PLC0415
    if type(s) is not str or not _DTYPE_OK.match(s):
        raise ValueError("MALFORMED:dtype")
    try:
        return np.dtype(s)
    except TypeError:
        raise ValueError("MALFORMED:dtype") from None


def _dec_list(v, d) -> list:
    if type(v) is not list:
        raise ValueError("MALFORMED:not-a-list")
    return [dec(i, d) for i in v]


def _dec_arr(v, dtype, d):
    """-> a fresh 1-D numpy array of the declared dtype holding the plain values sent (no other input)."""
    import numpy as np  # noqa: PLC0415
    dt, flat = _dec_dtype(dtype), _dec_list(v, d)
    if dt.kind in "Mm":                 # exact int64 counts, never a parsed date
        if not all(type(i) is int for i in flat):
            raise ValueError("MALFORMED:datetime-values")
        return np.array(flat, dtype="<i8").view(dt)
    a = np.empty(len(flat), dtype=dt)
    for i, val in enumerate(flat):      # ponytail: element-wise, so no broadcasting of a nested plain value
        a[i] = val
    return a


def _dec_index(v, d):
    import pandas as pd  # noqa: PLC0415
    if type(v) is not dict:
        raise ValueError("MALFORMED:index")
    keys, name = set(v), dec(v.get("name"), d)
    if keys == {"range", "name"} and type(v["range"]) is list and len(v["range"]) == 3 \
            and all(type(i) is int for i in v["range"]) and v["range"][2] != 0:
        return pd.RangeIndex(*v["range"], name=name)
    if keys == {"dtype", "name", "v"}:
        return pd.Index(_dec_arr(v["v"], v["dtype"], d), name=name)
    raise ValueError("MALFORMED:index")


def _dec_ndarray(x, d):
    shape = x["shape"]
    if type(shape) is not list or not all(type(i) is int and i >= 0 for i in shape):
        raise ValueError("MALFORMED:shape")
    # reshape raises unless the declared shape matches the data actually sent, so a huge shape allocates nothing
    return _dec_arr(x["v"], x["dtype"], d).reshape(shape)


def _dec_series(x, d):
    import pandas as pd  # noqa: PLC0415
    ix, v = _dec_index(x["index"], d), _dec_arr(x["v"], x["dtype"], d)
    if len(v) != len(ix):
        raise ValueError("MALFORMED:series-length")
    return pd.Series(v, index=ix, name=dec(x["name"], d))


def _dec_dataframe(x, d):
    import pandas as pd  # noqa: PLC0415
    cols, dts, data = _dec_list(x["columns"], d), x["dtypes"], x["v"]
    ix = _dec_index(x["index"], d)
    if type(dts) is not list or type(data) is not list or not len(cols) == len(dts) == len(data):
        raise ValueError("MALFORMED:dataframe")
    if any(type(c) is not list or len(c) != len(ix) for c in data):
        raise ValueError("MALFORMED:dataframe-column-length")
    if not cols:
        return pd.DataFrame(index=ix)
    # built column by column under positional keys, then relabelled: duplicate column or index labels (which
    # would misalign an assignment) stay exactly as they were sent.
    df = pd.DataFrame({j: pd.Series(_dec_arr(c, dt, d)) for j, (dt, c) in enumerate(zip(dts, data))})
    df.index, df.columns = ix, pd.Index(cols)
    return df


def _dec_sci_index(x, d):
    return _dec_index(x["v"], d)


_SCI = {"ndarray": ({"$", "dtype", "shape", "v"}, _dec_ndarray),
        "series": ({"$", "dtype", "name", "index", "v"}, _dec_series),
        "dataframe": ({"$", "columns", "index", "dtypes", "v"}, _dec_dataframe),
        "index": ({"$", "v"}, _dec_sci_index)}


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
_SANDBOX = None


def _sandbox():
    """sandbox.py from this file's own directory, loaded by path and cached.

    That directory must NOT go on sys.path: it also holds code.py, which would shadow the stdlib `code`
    module (pdb imports it, and so therefore does doctest, which dataset test modules import) and then fail
    on its relative imports. Loading by path also means no sys.path entry can substitute another module
    named `sandbox` for the one that builds the isolation arguments."""
    global _SANDBOX
    if _SANDBOX is None:
        import importlib.util  # noqa: PLC0415
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sandbox.py")
        spec = importlib.util.spec_from_file_location("ogi_tasks_sandbox", path)
        _SANDBOX = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_SANDBOX)
    return _SANDBOX


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
        sandbox = _sandbox()
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
            except (ValueError, TypeError, RecursionError) as e:
                self._fault(f"MALFORMED:{type(e).__name__}:{e}"[:160])
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
    os.dup2(2, 1)                                   # this directory stays off sys.path on purpose: see _sandbox()
    out.write(json.dumps(evaluate(json.load(sys.stdin))))
    out.flush()
    os._exit(0)                                     # skip interpreter teardown of whatever the dataset tests left


if __name__ == "__main__":
    main()
