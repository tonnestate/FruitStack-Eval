# PNP-001 results, 2026-11-18

Output of the FruitStack research campaigns on the PNP-001 objective (exact finite structure of positive 1-in-3-SAT, matroid ports, Gal rank bounds). Everything here is a **finite or restricted-model fact**. Nothing bears on P vs NP itself, and nothing is a general lower bound.

## Contents
- `registers/DISCOVERY-REGISTER.md` - every finding D-010..D-016e, D-014d-f with its status (proved / computed / inconclusive / negative). **Start here.**
- `registers/FAILED-RUNS-REGISTER.md` - failed runs and their reasons (kept deliberately; failed cycles are not counted as results).
- `registers/THEOREM-D013.md` - proof that the 1-in-3 MUS clutter is not a matroid port for n >= 6.
- `registers/LIT-REASSESSMENT-2026-11-18.md` - literature items; all are UNVERIFIED unless the register says otherwise.
- `lab/circuits`, `lab/gal`, `lab/ports` - the scripts and small outputs behind the register entries (exact circuit sizes via SAT, Gal matrices, forbidden-minor checks).
- `campaign-logs/` - raw logs of the two autonomous campaigns and the proofbook copy they wrote (staging copy; the live proofbook was not changed).

## Reading guide
- Independently re-checked by the director: D-016 (`lab/gal/recheck_d016.py`), D-016e (elementary proof in the register), D-014f (proof in the register), D-013 (two independent scripts, see the theorem file).
- Not independently re-checked: entries marked so in the register, in particular **D-014d: the "Gal ratio 20 for XOR-SAT n=5" claim is unverified** (no witness matrix exported; a later run reached only 15).
- Novelty of D-013 against the literature is not yet checked.
