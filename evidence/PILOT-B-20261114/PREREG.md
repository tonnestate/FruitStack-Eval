# PILOT-B: Hilft die ausgeführte Prüfung der adaptiven Organisation bei Code? Präregistrierung (exploratorisch)

**Owner-Freigabe:** 2026-11-14 („Natürlich mach ein Pilotlauf“).

**Status:** Gesperrt vor dem ersten Modellaufruf. Dieser Commit enthält den Studienplan `study_manifest.json` und dessen Hash, `d2ae8ec4ee61a9b32a8e7c3b3747e262525c7e60135e99a554fb4378ac95447c`.

## Frage

Bringt die aus der Aufgabe abgeleitete ausgeführte Prüfung (`runners/code_checks.py`, `plan.task_derived_checks`) im adaptiven Pfad mehr korrekte Lösungen? Die Arme unterscheiden sich nur in diesem Schalter.

## Arme

- **NOCHECK (Kontrolle):** `config/fs_runtime/adaptive_nocheck.toml`
- **CHECK (Behandlung):** `config/fs_runtime/adaptive.toml`

Für beide Arme gilt:
- **Ablauf:** derselbe Missionspfad (`runners/eval006.py` `org()`). Ob überhaupt Forschung läuft, entscheiden CherryMes Inquiry und Triage, wie bei Aurora.
- **Quellen und Plan:** dieselben eingefrorenen Quellen, nämlich der Live-Release-Stand (`REVISIONS.txt`), und dieselbe adaptive Planung.
- **Start:** derselbe Competence-Startzustand, getrennter PlumMe-Zustand pro Arm.
- **Kosten:** Zero-Charge, FREE_ONLY.
- **Reihenfolge:** je Aufgabe abwechselnd, erst NOCHECK, dann CHECK.

## Aufgaben

- 40 Aufgaben aus BigCodeBench v0.1.4 (Apache-2.0, sha256 `d9a49658…`), **ohne** BigCodeBench-Hard. Damit sind weder die 110 reservierten noch die 20 EVAL-006-Aufgaben dabei.
- Die Reihenfolge ist mit Seed 20261114 gezogen. Eine Aufgabe gilt als geeignet, wenn ihre Referenzlösung in der Sandbox besteht. Aus 60 geprüften Aufgaben sind 40 geeignet, siehe `eligibility.json`.
- Es gibt kein Tuning an diesen Aufgaben.

## Endpunkte

- **Primär:** Bestanden heißt: alle Tests bestehen (sichtbare und versteckte, offizielle BCB-Semantik) und der Tamper-Audit ist sauber. Der Test ist der gepaarte exakte McNemar, zweiseitig, über `fruitstack_eval.study_gate`. Es zählen alle registrierten Aufgaben (Intention-to-treat): Fehlt ein Ergebnis oder ist es inkonklusiv, gilt es als nicht bestanden. Die Bewertung ist blind, mit verdeckten Schlüsseln und gemischter Reihenfolge. Jede Aufgabe wird pro Arm genau einmal bewertet.
- **Sekundär (deskriptiv):**
  - Wie oft wurde Forschung aktiviert, und aus welchen Gründen?
  - Wie verteilen sich die Entscheidungslabel (VERIFIED, UNVERIFIED, REFUTED)?
  - Kosten: Provider-Aufrufe, Token und Laufzeit.
  - Ausfallbelege und Abstürze.

## Auswertungsregeln

- **Pilotcharakter:** Bei n = 40 ist dies ein Pilot. Ein p-Wert unter 0,05 ist kein Nachweis, nur ein Hinweis für eine bestätigende Studie mit größerem n.
- **Wenig Diskordanz:** Liefern die Arme nur wenige unterschiedliche Ergebnisse, wird das als „kein Unterschied erkennbar“ berichtet.
- **Keine Aktivierung:** Aktiviert die Triage auf einer Aufgabe keine Forschung, kann die Prüfung dort nicht wirken. Das wird separat berichtet. Die Aufgaben bleiben trotzdem in der Hauptanalyse (ITT).
- **Ungültiger Lauf:** Sind mehr als 10 % der Aufgaben-Arm-Paare INCONCLUSIVE oder ohne Modellausgabe, gilt der Lauf als **infrastrukturell ungültig** und wird so berichtet.

## Nachtrag 1 (2026-11-14, vor der ersten Bewertung): abgebrochener Start und Korrektur

**Was passiert ist**

- Der erste Start brach nach 16 Aufgaben-Arm-Läufen ab, das sind 8 Aufgaben × 2 Arme. Keiner dieser Läufe hat einen Provider-Aufruf gemacht oder eine Lösung erzeugt. Es wurde nichts bewertet und kein Ergebnis gesehen.
- Die Datensätze sind aufbewahrt in `RUN/aborted-1-no-HOME/`.

**Ursache**

- Jeder Arm startete mit einem PlumMe-Zustand, der nur aus der Competence-Kopie vom 2026-11-12 bestand.
- Ohne die Live-Fehlerhistorie wählte PlumMe für gpt-6-luna die Route `llm7`. Live hat diese Route 130 Fehlschläge und 0 Erfolge.
- Diese Route ist als NORMAL eingestuft und hat keinen Preis. PlumMe lässt sie trotzdem zu, weil die Owner-Regel vom 2026-11-09 lautet: „Die Paywall entscheidet; llm7 gilt als free account.“ PeachMe (`peachme/cost.py`) verweigert dagegen jeden Dispatch auf eine NORMAL-Route ohne Preis (PRICE_NOT_VERIFIED).
- Die Mission endete deshalb still als UNRESOLVED, mit 0 Aufrufen und ohne Ausfallbeleg.
- Dieser Widerspruch zwischen den Komponenten ist ein eigener Befund und wird separat berichtet.

**Korrektur**

- Beide Arme starten jetzt aus derselben Kopie des aktuellen Live-Auswahlzustands von PlumMe: `competence.jsonl`, `pool_quarantine.json`, `pool_health.json`, `failure_receipts.jsonl`, `host_policy.json` und `verify_cooldown.json`. Die Hashes stehen in `state-seed.sha256`.
- Die Einheit läuft jetzt mit `HOME` und `PATH`.
- Aufgaben, Arme, Endpunkte und Auswertung sind unverändert. Das Studienmanifest ist unverändert, mit demselben Hash wie oben.

**Smoke-Test**

- Vor dem Neustart lief ein Smoke-Test mit einer Nicht-Studienaufgabe (`SMOKE/1`, a+b).
- Ergebnis: 1 Provider-Aufruf, eine Lösung erzeugt.
