"""OFFLINE PROVIDER TRANSPORT for the end-to-end launcher simulation (tests only). PILOT_OFFLINE_SCENARIO: unset = scripted success, "fail" = every dispatch rejected (RATE_LIMITED), "paid" = every offer is a priced (NORMAL) route, "long" = a long customer conversation (prompt > 22 KB). Python imports this module at start-up when its directory is on PYTHONPATH (run_arm.sh prepends
$PILOT_OFFLINE_TRANSPORT, and run_pilot.sh only allows that outside the real base). It replaces EXACTLY ONE thing: plumme.service.default_adapters now returns one scripted adapter instead of the
live provider adapters - the model providers' network transport. Everything above it (PlumMeService, scheduler, leases, _check_execution_budget, receipts, PeachMe, CherryMe, tau2, MangoMe, OrangeMe,
AppleMe, the pilot gate and guard) is the real code. Every dispatch is appended to $PILOT_OFFLINE_TRANSPORT_LOG so a test can prove that nothing else answered."""
import json
import os
import time

if os.environ.get("PILOT_OFFLINE_TRANSPORT"):
    _LOG = os.environ.get("PILOT_OFFLINE_TRANSPORT_LOG", "")
    _STATE = {"sim": 0, "draft": 0, "challenge": 0, "revise": 0}
    _BOOK = {"user_id": "u1", "origin": "JFK", "destination": "SFO", "flight_type": "round_trip", "cabin": "basic_economy", "flights": [], "passengers": [],
             "payment_methods": [], "total_baggages": 0, "nonfree_baggages": 0, "insurance": "no"}

    def _stage(task: str) -> str:
        if "ENDS the interaction" in task:
            return "termination"
        if "[assistant-turn: write the next message of the simulated customer ONLY" in task:
            return "sim"
        if "A colleague criticised it" in task:
            return "revise"
        if "A colleague proposed this solution" in task:
            return "challenge"
        if "additional specialist" in task:
            return "specialist"
        if "not a single valid JSON object" in task:
            return "format"
        return "draft"

    def _answer(stage: str) -> str:
        _STATE[stage] = _STATE.get(stage, 0) + 1
        n = _STATE[stage]
        if stage == "sim":
            if os.environ.get("PILOT_OFFLINE_SCENARIO") == "long":        # a long conversation: the prompt grows past 22 KB (pilot-2 stopped there)
                return ("Please be careful with my request, here are more details. " * 25)[:1500] if n <= 9 else "###STOP###"
            return ["Hi, I want to remove Ethan from reservation H9ZU1C.", "Please look up my date of birth in my profile and book the cheapest direct round trip.",
                    "Yes, please go ahead."][n - 1] if n <= 3 else "###STOP###"
        if stage == "draft":
            if n == 1:
                return json.dumps({"action": "tool", "name": "get_reservation_details", "arguments": {"reservation_id": "H9ZU1C"}})
            if n == 2:
                return json.dumps({"action": "tool", "name": "book_reservation", "arguments": _BOOK})
            return json.dumps({"action": "message", "content": "I have processed your request. Is there anything else?"})
        if stage == "challenge":
            if n == 1:
                return "ISSUES: FOUND\nThe booking uses basic_economy but the customer asked for the cheapest direct flight and the reservation lookup shows a different cabin. Use economy."
            return "ISSUES: NONE\nChecked the cabin against the reservation lookup and the policy: economy is allowed for this fare; passenger count matches the CONVERSATION."
        if stage == "revise":
            return json.dumps({"action": "tool", "name": "book_reservation", "arguments": {**_BOOK, "cabin": "economy"}})
        return json.dumps({"action": "message", "content": "I have processed your request. Is there anything else?"})

    _SPEC = None
    if os.environ.get("PILOT_OFFLINE_CAMPAIGN"):          # COLLAB-1 acceptance: per task and condition scripts (see tests/test_ogi013_collab1_campaign.py); the arm name tells the DOUBLE which script to play
        with open(os.environ["PILOT_OFFLINE_CAMPAIGN"], encoding="utf-8") as _f:
            _SPEC = json.load(_f)
        _ARM = os.environ.get("OGI013_PILOT_ARM", "")
        _REF, _COND = (_ARM.split("/")[-2].replace("_", ":", 1), _ARM.split("/")[-1]) if _ARM.count("/") >= 2 else ("", "")
        _SCRIPT = {**_SPEC.get("tasks", {}).get(_REF, {}).get("*", {}), **_SPEC.get("tasks", {}).get(_REF, {}).get(_COND, {})}
        _CALLS = {"n": 0, "pending": None}

    def _spec_text(stage: str) -> str:
        _STATE[stage] = _STATE.get(stage, 0) + 1
        items = _SCRIPT.get(stage) or []
        item = items[min(_STATE[stage], len(items)) - 1] if items else None
        if item is None:
            return "###STOP###" if stage == "sim" else json.dumps({"action": "message", "content": "OK"}) if stage in ("draft", "revise", "format") else "ISSUES: NONE\nChecked the facts against the materials."
        if stage == "termination":
            return item
        if stage in ("draft", "revise", "format"):
            if "message" in item:
                return json.dumps({"action": "message", "content": item["message"]})
            return json.dumps({"action": "tool", "name": item["name"], "arguments": item.get("arguments", {})})
        return item

    def _install() -> None:
        import plumme.service as service
        from plumme.adapters.base import AdapterError, AdapterResult, ProviderAdapter
        from plumme.models import AuthMode, CostClass, ExecutionProtocol, Modality, RouteOffer, Usage

        families = {"alpha-1": "alpha", "beta-1": "beta", "gamma-1": "gamma", "delta-1": "delta", "gemini-3.1-flash-lite": "gemini"}

        class OfflineAdapter(ProviderAdapter):
            name = "offline-transport"
            priority = 1

            async def discover(self, credential=None):
                return [RouteOffer(adapter=self.name, source_id=self.name, provider=f"offline-{m.split('-')[0]}", model=m, model_family=fam, endpoint="https://offline.invalid/v1",
                                   cost_class=CostClass.NORMAL if os.environ.get("PILOT_OFFLINE_SCENARIO") == "paid" else CostClass.FREE_TIER, supports_text_generation=True, context_window=32000, gateway_id=None, canonical_model_id=None, anonymous=False,
                                   auth_mode=AuthMode.BROKERED, execution_protocol=ExecutionProtocol.OPENAI_CHAT,
                                   modalities=[Modality.TEXT, Modality.VISION] if m.startswith("gemini") else [Modality.TEXT]) for m, fam in families.items()]

            async def execute(self, offer, messages, max_output_tokens, credential):
                task = "\n".join(str(m.get("content", "")) for m in messages)
                stage = _stage(task)
                if os.environ.get("PILOT_OFFLINE_SCENARIO") == "fail":                 # every provider rejects before processing
                    raise AdapterError("RATE_LIMITED", "offline scenario: rate limited", None)
                if _SPEC is not None:
                    _CALLS["n"] += 1
                    every = _SCRIPT.get("fail_every")
                    if stage == "sim" and _SCRIPT.get("sim_fail"):                           # the customer simulator's provider is down: the whole block fails (SIM_ROUTE_FAILED)
                        raise AdapterError("RATE_LIMITED", "scripted simulator outage", None)
                    if stage == "sim":
                        _CALLS["sim_provider"] = offer.provider
                    if every and stage != "sim" and offer.provider != _CALLS.get("sim_provider") and _CALLS["n"] % every == 0:      # never the simulator's own provider: its pinned route must stay usable                                   # a provider that rejects every Nth request before processing
                        raise AdapterError("RATE_LIMITED", "scripted rejection", None)
                    if _CALLS["pending"] is not None and "Continue exactly where it stopped" in str(messages[-1].get("content", "")):
                        text, _CALLS["pending"] = _CALLS["pending"], None
                    else:
                        text = _spec_text(stage)
                        cut = _SCRIPT.get("truncate_first_draft") if stage == "draft" and _STATE.get("draft") == 1 else None
                        if cut and len(text) > cut:                                           # the provider stops at its output limit; PlumMe continues
                            _CALLS["pending"] = text[cut:]
                            exc = AdapterError("SEMANTIC_OUTPUT_FAILURE", f"TRUNCATED_CONTENT finish_reason=length max_tokens={cut}", None, usage=Usage(input_tokens=max(100, len(task) // 4), output_tokens=cut // 4,
                                                                                                                                                         total_tokens=max(100, len(task) // 4) + cut // 4, cost_usd=None))
                            exc.partial_text = text[:cut]
                            raise exc
                else:
                    text = _answer(stage)
                if _LOG:
                    with open(_LOG, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"ts": time.time(), "stage": stage, "provider": offer.provider, "model": offer.model, "pid": os.getpid(), "bytes": len(task.encode("utf-8"))}) + "\n")
                tin = max(100, len(task) // 4)
                return AdapterResult(text=text, usage=Usage(input_tokens=tin, output_tokens=max(8, len(text) // 4), total_tokens=tin + max(8, len(text) // 4), cost_usd=None),
                                     provider_request_id=f"offline-{os.getpid()}-{sum(_STATE.values())}", metadata={"finish_reason": "stop"})

        service.default_adapters = lambda settings, policy=None: [OfflineAdapter()]
        init = service.PlumMeService.__init__

        def init_with_credentials(self, *a, **k):
            init(self, *a, **k)
            for p in {f"offline-{m.split('-')[0]}" for m in families}:
                self.credentials.put(p, "offline-key")

        service.PlumMeService.__init__ = init_with_credentials

    try:
        _install()
    except ImportError:
        pass                      # interpreters that do not run PlumMe (the launcher's python3 helpers) are unaffected; the test proves the patch from the dispatch log
