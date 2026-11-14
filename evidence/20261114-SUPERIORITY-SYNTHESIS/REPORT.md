# Ist FruitStack zumindest teilweise überlegen? Evidenzsynthese vom 14.11.2026

**Status:** explorative Sekundäranalyse vorhandener Rohdaten. Keine neue Studie, keine Modellaufrufe, die 110 reservierten Aufgaben unberührt.
**Reproduktion:** `python3 evidence/20261114-SUPERIORITY-SYNTHESIS/analyze.py` im Repo-Root (nur Standardbibliothek). Es schreibt `results.json` mit SHA-256 jeder Eingabedatei. Jede Zahl unten steht dort unter dem genannten Schlüssel.
**Maßstab:** Die Organisation muss mehr leisten als dieselben Modelle allein, und zwar über Diversität, Rechenaufwand und Abstimmen hinaus (Owner-Ziel 2026-11-07). Eine Demo ist kein Beweis.

## Behauptungen und ihre Belege

Mit „Einzelmodell“ ist der Kontrollarm ohne Organisation gemeint, in der Tabelle als „Single“ bzw. „Kontrolle“ bezeichnet.

| # | Behauptung | Zahl | Schlüssel in `results.json` | Rohdaten |
|---|---|---|---|---|
| C1 | Bei Code schlägt die Organisation das Einzelmodell nicht. | ORG 8/20 gegen SINGLE 8/20; nur ORG richtig 1, nur SINGLE richtig 1; p = 1,0 | `eval006.org_vs_single` | `evidence/EVAL-006/graded.jsonl` (präregistriert: `evidence/EVAL-006/PREREG.md`) |
| C2 | Die Organisation kostet dabei ein Vielfaches. | 10,4× Token, 13,1× Laufzeit, 253 statt 20 Aufrufe | `eval006.token_ratio_*`, `wall_ratio_*`, `provider_calls` | `evidence/EVAL-006/accounting.json` |
| C3 | Kritik und Revision haben keine Note verändert. | 0 von 11 Revisionen | (Audit, nicht neu gerechnet) | `evidence/EVAL-006-AUDIT/AUDIT.md` |
| C4 | Bei MCQ ist keine Aussage möglich. | 53 von 400 geplanten Fragen. Auf 37 sauberen Paaren: Team gegen Luna 4:1 (p = 0,38), Team gegen Nemotron 0:1 (p = 1,0), Ensemble gegen Luna 4:2 (p = 0,69) | `qa2d.*` | `evidence/ogi013-qa2d-v2-closure/inputs/results.jsonl`, Abschlussbericht `QA2D_V2_CLOSURE_REPORT.md` |
| C5 | Bei Recherche ist die Trefferquote des Einzelmodells in allen 4 Läufen höher. | Lauf 1: 11 gegen 44 von 50, Lauf 2: 15 gegen 44, Lauf 3: 19 gegen 35, Lauf 4: 25 gegen 38 (p = 0,015) | `eval005.runs.runN.hit_rate_paired` | `inputs/eval005-rerun/runN.graded.jsonl` |
| C6 | Wenn F3 antwortet, liegt es seltener falsch. Das zeigt nur Lauf 4. | Lauf 4: F3 falsch 1/26, das Einzelmodell auf denselben Aufgaben 7/26, Diskordanz 6:0, p = 0,031. Für 4 Läufe korrigiert: 0,125 | `eval005.runs.run4.selective_paired`, `best_run_p_bonferroni4` | dto. |
| C7 | Über alle Läufe hinweg bleibt davon nichts Signifikantes. | Gepoolte Diskordanz 8:4, p = 0,39. Rein deskriptiv, weil dieselben 50 Aufgaben wiederholt wurden. | `eval005.pooled_selective_discordant` | dto. |
| C8 | In Lauf 4 hat F3 nicht einfach die leichteren Aufgaben gewählt. In Lauf 3 tat es das. | Fehler des Einzelmodells auf den Aufgaben, die F3 beantwortet bzw. ausgelassen hat. Lauf 4: 7/26 gegen 5/24, p = 0,74. Lauf 3: 2/22 gegen 13/28, p = 0,005. | `…control_error_answered_vs_abstained` | dto. |
| C9 | Der Vorteil in Lauf 4 fällt mit einem schwachen Kontrolllauf zusammen. | Das Einzelmodell löste in den Läufen 1 bis 4: 44, 44, 35, 38. Die Kaskade „F3 falls verifiziert, sonst Einzelmodell“ kommt in Lauf 4 auf 44, also genau auf das Niveau des Einzelmodells in Lauf 1 und 2. | `…cascade_vs_control`, `…hit_rate_paired.b_correct` | dto. |
| C10 | F3 kostet ebenfalls ein Vielfaches. | Quota-Einheiten 3,7× bis 6,5×, Laufzeit 3,1× bis 12,6× | `…quota_units`, `…wall_seconds` | dto. |

## Urteil

1. **Eine allgemeine Überlegenheit ist nicht belegt.**
   - Code (C1, C2): kein Gewinn, aber etwa das Zehnfache an Kosten.
   - MCQ (C4): keine Aussage möglich.
   - Recherche (C5): Bei der Trefferquote ist das Einzelmodell in jedem Lauf besser.
2. **Teilweise Überlegenheit gibt es nur als Hypothese, und zwar in einer einzigen Dimension: Zuverlässigkeit, wenn geantwortet wird (C6).**
   - Sie hält der Mehrfachkorrektur nicht stand (C6) und auch nicht der Poolung über alle Läufe (C7).
   - Sie ist mit einer schwankenden Kontrolle konfundiert (C9). Das AUTO-Einzelmodell zieht je Lauf andere Modelle.
   - Die Aufgaben sind DRAFT. Das System wurde zwischen den Läufen an genau diesen Aufgaben nachgebessert (siehe `inputs/eval005-rerun/REVISIONS.txt`).
3. **Die prüfenswerte Form der Hypothese ist eine Kaskade:** Die Organisation dient als Verifikations-Gate vor dem Einzelmodell, nicht als Ersatz dafür (C9). Das wäre eine echte organisatorische Funktion, nämlich Arbeitsteilung zwischen Antworten und Prüfen. Sie ist bisher nicht nachgewiesen.
4. **Warum die Organisation bisher nichts bringt** (EVAL-006-Audit, C3):
   - De facto gibt es nur eine starke Modelllinie.
   - Die zweiten Meinungen kommen von schwachen Gratismodellen.
   - Es gibt keine ausgeführte Prüfung, also hat die Kritik keine Grundlage.
   - Die festen Budgets passen nicht zum Codex-Pfad (~17,7k Token pro Aufruf).
   - Der adaptive Pfad, mit dem Aurora heute arbeitet, wurde nie evaluiert.

## Offene Punkte, die diese Daten nicht schließen können

| Offener Punkt | Warum offline nicht lösbar | Was es bräuchte |
|---|---|---|
| Kontrolle darf sich nicht enthalten | Eine echte Risk-Coverage-Kurve braucht eine Kontrolle mit Konfidenz oder Enthaltung. | Studie A |
| Kontrolle zieht wechselnde Modelle | Die AUTO-Ziehung ist je Lauf anders, das ergibt Varianz zwischen den Läufen (C9). | Kontrollmodell fest pinnen |
| Aufgaben getunt und DRAFT | Die vorhandenen Daten lassen sich nicht nachträglich zurückhalten. | Frische, zurückgehaltene Aufgaben mit vom Owner freigegebenen Referenzen |
| Gleicher Rechenaufwand | Bisher gibt es keine Kontrolle mit dem ~4-fachen Budget (z. B. Self-Consistency). | Studie A, Kontrollarm 3 |
| Adaptiver Aurora-Pfad | Er wurde in keiner Studie ausgeführt. | Studie B |
| Code mit ausgeführter Prüfung | EVAL-006 hatte keine ausgeführte Prüfung. | Studie B |

## Präregistrierungsentwurf (nicht gesperrt; braucht Owner-Freigabe für Aufgaben und Budget)

**Studie A: Kaskade und selektive Genauigkeit (Recherche).**
- **Hypothese H1:** Die Kaskade „F3, falls verifiziert, sonst dasselbe Einzelmodell“ macht weniger Fehler als
  - (a) dasselbe Einzelmodell allein,
  - (b) dasselbe Einzelmodell mit Enthaltungsanweisung und anschließender Rückfallebene,
  - (c) eine Self-Consistency-Kontrolle mit gleichem Rechenbudget.
- **Primärer Endpunkt:** Fehlerquote bei gleicher Gesamtabdeckung (100 %), gepaarter exakter McNemar, α = 0,05, einseitig H1. Sekundär: AURC der Risk-Coverage-Kurve.
- **Modell:** Das Kontrollmodell ist fest gepinnt, nicht AUTO.
- **Aufgaben:** n ≥ 100 frische Aufgaben, nicht die 110 reservierten und nicht die 50 DRAFT-Aufgaben aus EVAL-005. Sie werden vor dem ersten Lauf eingefroren und es gibt kein Tuning daran.
- **Abbruch:** Fallen mehr als 10 % der Fälle aus Infrastrukturgründen aus, wird der Lauf ungültig. Diese Fälle werden berichtet, nicht stillschweigend ersetzt.
- **Fallzahl:** Sie wird vor der Sperrung per Power-Rechnung festgelegt. Als Planungsannahmen dienen die beobachteten Diskordanzen: optimistisch Lauf 4 mit 6:0 auf 50 Paare, konservativ gepoolt 8:4 auf 200 Paare. Daraus folgt n ≥ 100, eher mehr.

**Studie B: Code mit ausgeführter Prüfung im adaptiven Pfad.**
- **Voraussetzungen:**
  - Die Organisation führt die sichtbaren Tests aus, bevor sie revidiert.
  - Eine kompetente zweite Modelllinie ist dabei, damit sich der Effekt der Organisation vom bloßen Neu-Ziehen trennen lässt.
- **Kontrolle:** Dasselbe Modell mit gleichem Budget und mit Testausführung (pass@k).
- **Endpunkt:** versteckte Tests, gepaart.

## Herkunft

- Die EVAL-005-Läufe stammen vom 2026-11-12. Die Kopien der `graded.jsonl` liegen unter `inputs/eval005-rerun/`, das Original unter `/root/fruits/research/FRUITSTACK-EVAL-005-RERUN-20261112/` auf dem VPS. Die Revisionsstände stehen in `inputs/eval005-rerun/REVISIONS.txt`.
- Der Grader ist `fse-inquiry/1`, verblindet. Als richtig gilt `verdict_ok`.
- Eine Enthaltung von F3 zählt bei der Trefferquote als nicht gelöst.
