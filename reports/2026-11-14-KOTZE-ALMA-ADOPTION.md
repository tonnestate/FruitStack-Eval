# Abgleich KOTZE und ALMA-LABS mit FruitStack (14.11.2026)

**Quellen:**
- `tonnestate/Kotze` @ ccf378a: C11-Kontrollkern, externer Grader, Konzept- und Forschungspapier.
- `tonnestate/ALMA-LABS` @ 34276e7: Zielbild zur Quellenattribution, Baseline.
- Beide gehören dem Owner. Laut ALMA-Grenzregel darf nichts von FruitStack oder KOTZE **nach ALMA** fließen. Die Richtung ALMA → FruitStack ist methodisch offen.

**Stand von FruitStack:** Geprüft wurde am Live-Code. Live sind CherryMe-029ed42, PeachMe-b4bd852, PlumMe-c0e7edd und AnanasMe-eeab9c8.

## Mechanismen aus KOTZE

| KOTZE-Mechanismus | FruitStack live | Entscheidung |
|---|---|---|
| Externer Grader: versiegeltes Manifest, Oracle-Hash-Prüfung, geschützte Tests wiederhergestellt, bwrap, eine Note pro (Studie, Aufgabe, Arm), ITT | Teilweise vorhanden: Doppelprüfung ohne Studien-Schlüssel, kein Oracle-Hash, kein ITT | **Übernommen:** `fruitstack_eval/study_gate.py` mit Tests in `tests/test_study_gate.py` |
| Abschluss nur nach unabhängigem Verifier, Worker-Behauptung ≠ fertig | Teilweise: `evidence_label` VERIFIED/PARTLY/UNVERIFIED wird angezeigt und die Antwort entsprechend markiert, der Zustand bleibt aber COMPLETED | Vorerst behalten. Das Label erfüllt den Zweck. |
| Ausgeführte Prüfung in der Schleife | Nur im Eval-Pfad vorhanden (`runners/code_checks.py`, Tests aus der Aufgabenstellung, bwrap). Aurora übergibt weder `verifier` noch `check_author`. | **Erst messen** (Studie B), dann in Aurora einbauen |
| Loop-Convergence-Gate: Wiederholung nur, wenn sich Evidenz geändert hat | Teilweise: Brother re-examiniert nur geänderten Text, AppleMe NO_PROGRESS → STOP | Nicht nachbauen. Die Kritik braucht zuerst Prüfsignale (Zeile oben). |
| Hypothesen-Frontier, Widerlegtes nie erneut | Teilweise: `research_tree.py` (FALSIFIED terminal) plus Prompt-Hinweis, aber keine harte Sperre | Kleine Sperre möglich, Nutzen bei max_rounds = 2 aber unbelegt. Zurückgestellt. |
| Kontextpaket aus kanonischem Zustand | Teilweise: CogC-Pakete. `continuity.py` (inkl. widerlegter Hypothesen) ist ungenutzt. | Erst bei langen Missionen relevant. Zurückgestellt. |
| Eskalationsprofile: Einzelworker als Standard | Vorhanden: Lane L1 → ein Worker, CherryMe-Triage → Organisation | Behalten. Kalibrierung über Studie A. |
| Ablationsleiter A0 → A8: jede Komplexitätsstufe nur nach Nachweis bei gleichen Kosten | Fehlt als Programm | **Übernommen als Vorgehen:** Studien A und B laufen über `study_gate` |

## Methodik aus ALMA-LABS

| ALMA-Prinzip | Übertragung auf FruitStack |
|---|---|
| Lockbox: einmal ausgewertetes, vorab eingefrorenes Set | Gilt für die Aufgabenpools der Studien A und B (vgl. die getunten DRAFT-Aufgaben in EVAL-005) |
| Gruppierte Splits ohne Leckage | Tuning- und Testaufgaben werden nach Quelle bzw. Familie getrennt, nicht nach Zeile |
| Kalibrierung nur auf Out-of-Fold-Daten, Abstain erst nach eigener Evaluation | Gilt für die Kaskade bzw. Enthaltung in Studie A |
| Positive, negative und inkonklusive Ergebnisse werden gleich gespeichert | Wird bereits gelebt (EVAL-006 negativ veröffentlicht) |
| Modell-Attribution von Texten | Später möglich: Prüfen, ob freie PlumMe-Routen wirklich das angegebene Modell liefern (Donor-Identität, vgl. PLUMME-DONOR-RECOVERY-001). Braucht gelabelte Daten. Nicht jetzt. |

## Konsequenz

Weitere Laufzeitmechanismen ohne Messung widersprechen sowohl dem Owner-Ziel als auch KOTZEs eigener Adoptionsregel. Diese Regel lautet: Zusätzliche Komponenten werden nur behalten, wenn sie einen vorab festgelegten Endpunkt bei gleichen Kosten verbessern.

**Reihenfolge:**
1. `study_gate` (erledigt)
2. Studie B: ausgeführte Prüfung an gegen aus, gleiche Aufgaben, gleiches Modell
3. Bei Nutzen: `check_author` in Aurora-Code-Missionen
4. Studie A: Kaskade
