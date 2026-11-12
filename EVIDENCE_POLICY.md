# EVIDENCE-POLICY/1 (2026-11-12)

What counts as admissible evidence is a property of the task. It is declared in the task's reference (`evidence_class`)
before any run, and it is never changed after results exist.

| `evidence_class` | admissible evidence for the verified (F3) arm | typical task |
|---|---|---|
| `PRIMARY_REQUIRED` (default) | only sources on the primary-source allowlist (standards bodies, official registers, statutes, agencies) | claims whose authority is a primary document |
| `AUTHORITATIVE_SECONDARY` | additionally named authoritative secondary sources (must be listed in the evaluation's own versioned protocol) | ordinary factual claims |

Rules
1. A reference without the field is `PRIMARY_REQUIRED`. Every FSE-INQUIRY/1 task, including the 50-task inquiry pilot
   (`tasks/dev/pilot_inquiry_tasks_DRAFT.jsonl`), stays `PRIMARY_REQUIRED`; its scoring rubric (`fse-inquiry/1`) is frozen.
2. A revised evidence policy needs a separately versioned evaluation with its own task file, protocol and fresh data. It
   may not re-grade, pool with or re-analyse earlier observations.
3. Reports keep three numbers apart for every arm: factual correctness (grader), evidence compliance (answer backed by
   admissible verified evidence; NOT_MEASURED for arms without an evidence requirement) and abstention rate. A control
   arm that answers from model knowledge measures factual correctness only and is never presented as verified correctness.
4. Engineering defects (search crashes, unparsed PDFs, failed extraction calls) are fixed in the responsible component
   and measured as such; they are not evidence-policy questions.

## Source eligibility versions (2026-11-12)
Runner config key `source_policy` selects CherryMe's `SOURCE_POLICIES` entry; absent = `PRIMARY-ALLOWLIST/1` (all EVAL-005 runs 1-4).
`PRIMARY-ALLOWLIST/2` (owner decision 2026-11-12) adds BIPM, IUPAC, Unicode Consortium (standards/reports/charts/data paths), CERN
(home.cern, CDS records) and official German federal government publications (bundesregierung.de editorial paths, recht.bund.de).
News media are not primary sources. A run under /2 is a separate evaluation version and is never pooled with /1 runs.
