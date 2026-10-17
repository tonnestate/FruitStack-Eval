# FRUITSTACK — Konsolidiertes Gesamtdossier (2026-10-17)

Autor: Claude Code · Auftrag: P0 FRUITSTACK GLOBAL CONSOLIDATION & SCIENTIFIC EVALUATION · Stand der Daten: 2026-10-17
Reproduktion: `bash /root/fruits/research/FRUITSTACK-CONSOLIDATION-005/run_all.sh` (offline, kein Provider-Aufruf). Eingabe-Hashes: `INPUT_HASHES.sha256`. Ergebnis-JSONs: `repro/*.json`.
Methode: Es wurde **keine** zweite Bewertungsengine gebaut. Alle Noten stammen aus FruitStack-Evals registriertem Grader `fse inquiry grade` (`fse-inquiry/1`, Referenzen nie im System), alle Schätzer aus `fruitstack_eval.pilot.analyze` (FSE `6e2ef14`). Die Skripte zählen Receipts und rufen diese Funktionen auf.
Nicht verändert: OGI-012 (geparkt), alle eingefrorenen Worktrees, alle Rohdaten, alle `main`/`sync/local-truth`-Stände. Keine neuen Provider-Aufrufe.

---

## 0. Kurzurteil

> **Ergänzung 2026-10-17 (§11, FRUITSTACK-SCIENCE-100):** Das 9/50-Defizit entsteht überwiegend vor/nach den Modellen (17 Aufgaben: Quellenpflicht-Gate stellt gar keine Modellfrage; 9: Schlüsselstufe; 6: Verifikationsregeln), nicht durch schwache Modelle; beobachtete Auswahl-Obergrenze 41/50.

> **Ergänzung 2026-10-17 (§12, FRUITSTACK-COGNITIVE-RECOVERY/1):** CherryMe 0.4.1 (`cc/cognitive-recovery-001`, 5a6adad, nicht gemergt/installiert) behebt die vier nachgewiesenen Verlustmechanismen; Offline-Replay fallweise in §12.1 (17/17 Vorab-Blockaden, 4/9 Schlüsselverluste, 1/6 Verifikationsfehler beseitigt, Rest teils nur mit neuen Modellantworten prüfbar). Keine Erfolgsquote behauptet.

> **Ergänzung 2026-10-17 (§13, FRUITSTACK-COGNITIVE-INTEGRATION/2):** CherryMe 0.4.2 (a70fa36): vollständiges privates Beitragsbuch, lineage-bewusste Unabhängigkeit (AUTO gab zwei Workern dasselbe Modell — behoben), Konsolidierungsrecord, Schlüsselkette (alle 9 Fälle: 7 verifiziert, 1 unverifiziert gekennzeichnet, 1 in keinem Beitrag), Mission-Record-Kette + unabhängiger FSE-Leser, FSE-MARGINAL/1 auf den vorhandenen Beobachtungen (Unabhängigkeit ungemessen, 17 blockierte Fälle PARTIALLY_OBSERVED/NOT_MEASURABLE), Fallmatrix, Registrierungsentwurf (nicht gestartet). Keine neue Inferenz.

> **Ergänzung 2026-10-17 (§14, Forensik der organisationalen Intelligenz):** Fehlerzuordnung der C-Arme (D2: 28 Gate-Blockaden, 12 Infrastruktur, 1 Zeitlimit, 0 falsche Synthese; D1c: 7/7 Infrastruktur), Integrationsverlustrate 20/32 (D2) mit 13 vor und 7 bei der Synthese (nur Aufruf-Ausfälle), Synthesizer-Bewertung, Modellketten, Architekturlücke, Entwurf PREREG-ORGSYNTH-3, Eigentümerentscheidung. Keine neue Inferenz; OGI-012 nicht gelesen.

| Ebene | Stand |
|---|---|
| **Technisch funktionsfähig** | Ja, offline belegt: Missionspfad PEACH-MISSION/1 läuft gegen echtes MangoMe, PlumMe, CherryMe RG/2, AppleMe und PeachMe mit Scripted-Fake-Provider (Suiten: CherryMe 336, PeachMe 240, PlumMe 455, AppleMe 92, FruitStack-Eval 311, Worker/Cutover 10). **Kein** Beleg für Leistung. |
| **Organisatorisch funktionsfähig** | Demonstriert nur offline: eine Identität von Annahme bis Checkpoint, Verantwortungsgraph, unabhängige Prüfung durch andere Modellfamilie, eine Budgetkette, Wissensrückführung nur für Verifiziertes. **Nicht** demonstriert im Betrieb: Der produktive Worker kann MangoMe/OrangeMe in seinem Venv nicht laden (§1.4). |
| **Wissenschaftlich nachgewiesen** | **Nichts, was die OGI-Hypothese stützt.** Es gibt keinen einzigen gültigen, ausreichend großen Vergleich „Organisation gegen Einzelmodell/Kontrolle“ auf der heutigen Architektur. Die vorhandenen Vergleiche älterer Architekturen sind negativ oder nicht entscheidungsfähig, und der größte (9/50 gegen 37/50) ist durch dokumentierte Versorgungsmängel konfundiert. |

**Gesamtbewertung der OGI-Hypothese: nicht gestützt, aber auch nicht widerlegt — unentschieden wegen fehlender gültiger Daten.** Die Beobachtungsrichtung ist durchgehend ungünstig (mehr Aufrufe und Tokens, keine bessere Note). Das ist ein Befund und wird nicht umetikettiert.

---

## 1. Technischer Gesamtstand

### 1.1 Komponenten (Zuständigkeit aus dem Code)

| Komponente | Zuständigkeit (Code-Beleg) | `main` = `sync/local-truth` | Release-Branch (Commit) | Prod `venv-host` (editierbar auf Sync-Klon) |
|---|---|---|---|---|
| CherryMe | Kognition: Verantwortungsgraph RG/2, Delegation, Eskalation/Deeskalation, Verdichtung (`cherryme/engine.py`, `responsibility.py`, `ensemble.py`) | `a667256` (0.3.4) | `cc/cherryme-responsibility-brain` `62379fc` (0.4.0) | 0.3.4 |
| PlumMe | Versorgung, Kompetenzprofile, Skills, `ParentBudget`, Readiness | `122b81b` (0.1.12) | `cc/plumme-0.1.15-release` `12c57fd` | 0.1.11 (MCP-Venv 0.1.12) |
| PeachMe | Session, Budget-Ledger, Reflex-Signale, Mission (`mission.py`), Brücke zu MangoMe/OrangeMe/CherryMe/PomeloMe | `main` `1bc90f8`, **kein** `sync/local-truth` | `cc/peachme-cherryme-budget-bridge` `cc29f8d` (0.8.4) | 0.8.3 |
| AppleMe | Deterministische Beobachtung, operative Signale | `8dfc33f` (0.1.2) | `cc/appleme-0.1.4-release` `a00b4ac` | 0.1.2 |
| MangoMe | Autoritative WorkIdentity, Turn-Bindung, Checkpoints | `9800946` (0.3.23) | — | **nicht importierbar im Prod-Venv** |
| OrangeMe | Projekt-/Chat-Ledger (`ProjectLedger.get/put` mit Revisionsprüfung) | `953e725` (0.1.1) | — | **nicht installiert**; braucht private GitHub-Ledger-Repos |
| PomeloMe | Kontrollierte externe Effekte (von PeachMe angebunden) | `b62f64b` (0.1.0) | — | 0.1.0; in diesen Aufgaben kein Effekt |
| BlueberryMe | Egress-/Offenlegungsautorität | `23a8e68` | — | **nirgends installiert**; nur die Egress-Schnittstelle (`authorize_model_input`) existiert |
| BananaMe | Repository-Intelligenz für Coding-Agenten | `aa68979` | — | nicht im Laufzeitpfad (nur im PeachMe-Eigentumsvertrag genannt) |
| CogC | Kontext-Kompression (CherryMe hat eigenes `cogc.py`) | `ae29782` | — | kein Laufzeitbeleg in den Läufen |
| FruitStack-Eval | Unabhängige Bewertung | `6e2ef14` (0.2.0) | `cc/fse-rg2-evidence` `5aaa734` | 0.2.0 (editierbar auf `tonnestate-repos`) |

Alle Pakete im Prod-Venv sind **editierbare Installationen auf die Sync-Klone** (`/root/fruits/sync/*`): Das Vorrücken eines Klons ändert den laufenden Code sofort.

### 1.2 Wer kommuniziert im realen Aufgabenfluss — wer steht nur daneben

Aus Imports und Aufrufstellen (nicht aus READMEs):

| Verbindung | Befund |
|---|---|
| CherryMe → PlumMe (Registry, Investigator, Entscheidungsprotokoll, Kompetenzprofile, Fehlerquittungen) | real, in allen Läufen |
| CherryMe → AppleMe (`observe_event`) | real; „Aktivität ist kein Erkenntnisgewinn“ |
| CherryMe → MangoMe | nur Recovery-Evidenz (`mangome_checkpoint_sink`) und lokaler Outbox; in den Evaluationsarmen `LOCAL_OUTBOX_ONLY` |
| PeachMe → MangoMe/OrangeMe/PlumMe | real implementiert (Restore, Gedächtnis, Einzelschritt), **in keiner Evaluation und nicht im alten Worker genutzt** |
| PeachMe → CherryMe | war bei aktivem Budget verweigert; jetzt über ParentBudget überbrückt (Branch) |
| FruitStack-Eval → CherryMe/PlumMe/AppleMe | real |
| FruitStack-Eval → PeachMe/MangoMe | bis zum Reader `FSE-ORG-OBSERVATION/1` keine; der Reader liest nur Missionsrecords und wurde nur mit Offline-Records getestet |
| Produktiver Worker → PeachMe/MangoMe/OrangeMe | im Live-Stand `/opt/fruitstack/integration/aurora_mission_worker.py` **keine**; die umgestellte Fassung liegt gestaged |

### 1.3 Behobene Integrationslücken (am Code belegt)

1. **Budget:** Provider-Dispatches wurden pro Lease gezählt; im Lauf D4 entstanden 60 Ausführungen für 14 genehmigte Aufrufe (FS-INTEGRITY-005, `REPORT_FS005.md`). Behoben durch ein gemeinsames `ParentBudget`; offline belegt, live nicht.
2. **PeachMe ↔ CherryMe:** Ein Inquiry unter Session-Budget war pauschal verweigert. Jetzt ParentBudget aus dem Restbudget plus exakte Verbuchung; ein Inquiry ohne Dispatch bucht **keinen** Call mehr und gibt die Reservierung frei.
3. **Autorität:** Der MangoMe-Restore meldet `productive_execution_allowed` nie als wahr (Turn-Bindung erforderlich). PeachMes Kontextprüfung wäre daher immer gescheitert. Jetzt autorisiert der gebundene, bei jedem Lesen neu geprüfte Turn; `consult_brain` hat dieselbe Autorität wie der reguläre Inferenzpfad (Kontext, Reflex, Egress-Policy).
4. **Aufrufgrenze:** PeachMe verwarf `call_budget > budget`. Ein Verantwortungsgraph braucht mehrere Dispatches pro Frage; die Regel ist entfernt.
5. **Wissenswiederverwendung:** Nur exakt gleichwertige Behauptungen; ähnliche gehen als unverifizierter Hinweis an den Worker.

### 1.4 Schnittstellen, die einen echten durchgängigen Betrieb noch verhindern

| # | Schnittstelle | Befund |
|---|---|---|
| 1 | Worker ↔ MangoMe | `mangome` ist im Prod-Venv `/opt/fruitstack/venv-host` **nicht importierbar** (geprüft: nur `pomelome` vorhanden). Der Missionspfad meldet dort `COMPONENT_UNAVAILABLE`. |
| 2 | Aurora ↔ WorkIdentity | Aurora-Aufträge tragen keine admittierte WorkIdentity. Der Worker verweigert sie (`WORK_IDENTITY_REQUIRED`) und admittiert nichts selbst. |
| 3 | OrangeMe | Nicht installiert; verlangt private GitHub-Ledger-Repos und ein initialisiertes `memory/working`. |
| 4 | Egress | BlueberryMe nirgends installiert; ohne benannte Eigentümer-Freigabe (`OWNER_QUESTIONS`) verweigert der Worker. |
| 5 | PeachMe-Wahrheit | `main` ohne `sync/local-truth`-Spiegel (AGENTS.md: Stopp). |
| 6 | FruitStack-Eval | `main` und OGI-Linie divergiert (73 voraus, 5 dahinter). |

## 2. Verantwortungs- und Integrationsstruktur (Missionspfad PEACH-MISSION/1)

```
Aufgabenannahme ─ MangoMe: Turn-Bindung (EXECUTE) auf EXISTIERENDER WorkIdentity (nie erzeugt)
 → PeachMe-Session ─ MangoMe-Restore + OrangeMe-Gedächtnis (Kontext, Fingerprint)
 → Session-Budget → PlumMe-ParentBudget (jeder Dispatch reserviert VOR Egress)
 → CherryMe RG/2: Zerlegung in Verantwortungen, PlumMe-Kompetenz/Skill-Besetzung, Delegation,
   unabhängige Prüfung (andere Modellgruppe UND Familie), Verdichtung (korrelierte Modelle = eine Stimme)
 → AppleMe/Reflex-Signale → eine Formulierungsstufe (regulärer Schritt, gleiches Budget)
 → verifiziertes Wissen (hashverkettet) → MangoMe-Checkpoint (Findings, Verantwortliche, Evidenzreferenzen, Budgetquittung)
 → OrangeMe-Ledger (nur Verifiziertes) → Missionsrecord → FruitStack-Eval-Reader (unabhängig)
```

Zuständigkeiten bleiben getrennt: MangoMe autoritativ für Arbeitszustand und Turn, OrangeMe für sein Ledger, CherryMe für die kognitive Entscheidung, PlumMe für Modelle/Skills/Budget, AppleMe nur Beobachtung, FruitStack-Eval nur Bewertung. Es gibt keinen zweiten Router, keinen zweiten Speicher, keine zweite Planungsinstanz.

## 3. Entwicklungsbranches (Release-Satz)

Alle gepusht, **nichts gemerged**. Gemeinsamer Zielzustand getestet: PlumMe 0.1.15, AppleMe 0.1.4, PeachMe 0.8.4, CherryMe 0.4.0 — Suiten grün (Zahlen §0). Cutover-Werkzeug und gestagter Worker: `/root/fruits/integration/rg2-staging/` (`rg2_cutover.py preflight|snapshot|plan|apply|rollback`). Aktueller Preflight: alle vier sind Fast-Forwards; einziger Blocker ist der fehlende PeachMe-Spiegel.

---

## 4. Untersuchungsregister und reproduzierte Ergebnisse

Legende: „reproduziert“ = aus Rohdaten mit FSE-Grader/-Schätzer neu berechnet und mit den gespeicherten Zahlen verglichen.

| ID | Untersuchung | Aufgaben | Systemstand | Status | Reproduktion |
|---|---|---|---|---|---|
| D1a | EVAL-001: F1/F2/F3-ACE (partiell) | 3 | PlumMe 0.1.8, CherryMe 0.2.5 | exploratorisch | Noten 9/9 identisch |
| D1b | EVAL-002: F1 gegen F2 (extra12) | 12 | PlumMe 0.1.8, zwei `:free`-Modelle | exploratorisch | Noten 24/24 identisch; Tokens exakt (F1 2.329/3.072, F2 3.899/5.245) |
| D1c | F2 gegen F3 (`paired-resumable-001`) | 12 | PlumMe 0.1.10 / CherryMe-Kandidat | exploratorisch, mit Abstürzen | Noten 24/24 identisch |
| D2 | **F3 gegen AUTO-Einzelaufruf-Kontrolle** (Dev) | 50 | PlumMe 0.1.12 `122b81b`, CherryMe `a667256` | exploratorisch (Entwurfsaufgaben, keine freigegebenen Referenzen) | Noten 100/100 identisch, Schätzer identisch |
| D2b | F1-DEV gegen F3-DEV | 50 | CherryMe 0.3.4 | Dev; F3-Arm **leer** (0 Aufrufe) | Noten 100/100 identisch |
| D3 | ROUTE-ARMS-ABC/2 (A direkt, B föderiert, C hierarchischer Schatten) | 160 | PlumMe `c6e939a`, CherryMe `ca62a28` | **konfirmatorisch registriert**, aber Versorgung/Routing, nicht Organisation | Zählungen und Tests identisch |
| D4 | AUTO-Analyse (A gegen B) | 160 | – | Dev | identisch |
| D5 | Wissenswiederverwendung (`expl-reuse`) | 6 von 10 | CherryMe 0.3.2 | Abbruch, **nur mit-Gedächtnis-Arm** | nur Zählung |
| D6 | G2-Kalibrierung der freien Modelle | 6 Modelle × 24 | – | Qualifikation | nur Lesen |
| D7 | FS-INTEGRITY-005 (D4/D5-Diagnose) | 2 | – | Offline-Abnahme | Bericht gelesen |
| D8 | OGI-010 | 0 | – | **nie ausgeführt** | – |
| D9 | OGI-011 | 0 konfirmatorisch | rev 3.5 | blockiert (Versorgung); Versuch 1 und Smoke nur als Verbrauch | Receipts gezählt |
| D10 | OGI-012 (geparkt) | 2 von 96 Einheiten | PlumMe `494e6f5`, CherryMe `4ba1c32` | konfirmatorisch, **abgebrochen bei 2 %** | Zählung |
| D11 | RG/2-Missionsrecords | 0 reale | RG/2 | **nur Offline/Scripted** | – |
| D12 | AURORA-Claim-B-Korpus | 48 | – | Korpus/Qualifikation, keine Leistungsdaten | – |

### 4.1 D2 — 9/50 gegen 37/50 (reproduziert, mit Korrekturen)

Verglichen wurden: **Kontrolle** = ein ungepinnter PlumMe-AUTO-Aufruf mit derselben Recherche und denselben Auszügen (bis zu 7 Anläufe), **gegen F3** = die integrierte Kette (CherryMe-Untersuchung, unabhängige zitatgebundene Verifikation, Wissensspeicher, AppleMe) auf PlumMe-AUTO, 50 Entwurfsaufgaben, derselbe Grader.

| | Kontrolle | F3 |
|---|---|---|
| richtig (Note 1,0) | **37/50 = 0,74** | **9/50 = 0,18** |
| halb richtig (0,5) | 1 | 9 |
| falsch/Enthaltung | 12 | 32 (31 Enthaltungen, 1 nicht abgeschlossene Zeitüberschreitung) |
| mittlere Nützlichkeit | 0,75 | 0,27 |
| Provider-Receipts | 118 | **854** |
| berichtete Tokens | 34.090 | **818.165** |
| Wandzeit (Summe) | 806 s | 15.059 s (+ ein nicht abgeschlossener Task mit Deckel 1.200 s) |
| `cost_usd` | in 85/118 Receipts null | in 472/854 null |

F3 minus Kontrolle: Erfolgsrate **−0,56 [−0,74; −0,42]**, Nützlichkeit −0,48 [−0,70; −0,29] (Cluster-Bootstrap nach Subfamilie). Konkordanz: nur Kontrolle richtig 32, nur F3 richtig 4, beide 5, keiner 9. Exakter Vorzeichentest auf 32 gegen 4: p ≈ 1,9·10⁻⁶ (deskriptiv).

**Die Zahlen sind korrekt.** Abweichungen vom gespeicherten Bericht:
- Der Bericht nennt **808** Versuche und **764.714** Tokens für F3. Die Roh-Receipts zeigen **854** und **818.165**. Die Differenz (46 Receipts, 53.451 Tokens) gehört vollständig zu dem nicht abgeschlossenen Task `inq-org-06`, dessen Verbrauch im Ergebnis nicht verbucht wurde (`quota_units` 0). Der wahre F3-Aufwand ist also etwas höher als berichtet (24× statt ~22× Tokens).
- Der Bericht gruppiert 19/31 (F3 beantwortet/Enthaltung); mit dem Timeout als nicht beantwortet sind es 18/32. Kontrolle richtig auf den von F3 beantworteten Aufgaben: 11 (Bericht: 12). Auf den übrigen 32: 26 (Bericht: 25). Kein Einfluss auf das Ergebnis.
- Fehlerklassen: Gesamt aus Roh-Receipts F3: 392 fehlgeschlagen von 854 (RATE_LIMITED 112, SEMANTIC_OUTPUT_FAILURE 83, FORBIDDEN 80, BILLING 58, TIMEOUT 31, MODEL_NOT_FOUND 16, PROVIDER_UNAVAILABLE 10, MALFORMED 2). Die Zahlen im Bericht (FORBIDDEN 61, RATE_LIMITED 51, …) beziehen sich auf einen anderen Ausschnitt (die Fenster der Enthaltungen) und sind **nicht identisch reproduziert**; die Richtung stimmt.

**Ursachen, die die Abweichung erklären können (aus den Originaldaten und dem Nachtrag):**
1. 31 von 50 F3-Aufgaben endeten als `INCOMPLETE(SUPPLY)` — die unabhängige Verifikation braucht mehrere gelieferte Antworten, die freien Routen scheiterten.
2. Dokumentierte Versorgungsmängel (Nachtrag im Originalbericht): die lokale FreeLLMAPI-Quelle (`FLM_KEY` nicht exportiert) fehlte in **beiden** Armen; Trial-Credit-Routen wurden zugelassen (NVIDIA, alle 75 Versuche 403); Ausfälle wurden pro Modell statt pro Pool gezählt; Admission ohne Ausführungsbeleg.
3. Die Kontrolle wurde **nach** dem ersten Lauf definiert und nach zwei verworfenen Varianten (Protokollabweichung, im Bericht offengelegt).
4. Wo F3 antwortete, war es nicht besser: 9 volle Treffer plus 9 halbe bei 18 Antworten (Kontrolle auf denselben 18: 11 volle).

**Schlussfolgerung (zulässig):** Unter dieser Versorgung war die damalige Kette teurer, langsamer und schlechter. **Nicht zulässig:** daraus auf die OGI-Hypothese zu schließen — der Vergleich testet vor allem die Versorgungsschicht.

### 4.2 D1 — EVAL-001/002

- **D1b (12 Aufgaben):** F1 (ein Modell, 256 Tokens) **1/12**, F2 (feste Zwei-Modell-Einstimmigkeit, keine Organisation) **7/12**; Differenz +0,50 [+0,083; +0,833], exakter Vorzeichentest p = 0,070. Wichtig: bei F1 sind **7 von 12 Ausgaben ohne strukturierte Antwort** (das Reasoning-Modell wurde bei 256 Tokens abgeschnitten). Der Unterschied ist damit überwiegend ein Format-/Obergrenzen-Artefakt, **kein** Organisationseffekt. F2 hatte keinerlei CherryMe-Beteiligung.
- **D1a (3 Aufgaben):** F1 2/3, F2 2/3, F3-ACE 3/3; p = 1,0; nicht entscheidungsfähig.
- **D1c (12 Aufgaben, F2 gegen F3):** F2 7/12, F3 5/12; Differenz −0,17 [−0,50; +0,25]; Vorzeichentest p = 0,69. F3 lieferte bei 7 von 12 Aufgaben **keine Antwort** (ein Absturz „AppleMe nicht installiert“, übrige leere Ausgaben/Versorgung). Bedingte Genauigkeit bei geliefertem Ergebnis: F3 5/5, F2 7/7. Der Unterschied liegt in der Lieferung, nicht in der Qualität.
- Spätere F3-Einzelversuche (`f3-grounded-extra12-r1..r4`, `f3-exec-002-x01-r*`): je 1 Aufgabe, 0 erfolgreiche Modellantworten (CREDENTIAL_EXHAUSTED/RATE_LIMITED) — Versorgungsprotokoll, keine Leistungsdaten.

### 4.3 D3/D4 — ROUTE-ARMS-ABC/2 (Versorgung/Routing, nicht Organisation)

160 Rechenaufgaben, Pool {gpt-oss-20b, gpt-oss-120b}, korrekte Auslieferung insgesamt (Genauigkeit unter Gelieferten: 100 % in A und B):

| Arm | beantwortet | richtig gesamt | Receipts | Tokens (Receipts) | Tokens (gespeicherte Auswertung) |
|---|---|---|---|---|---|
| A direkt | 114 | **0,7125** | 139 | 111.951 | 111.951 |
| B föderiert (Failover) | 126 | **0,7875** | 175 | **147.252** | 123.669 |
| C hierarchischer Schatten | 121 | 0,73125 | 174 | **153.311** | 126.127 |

- **H1 A gegen B (registrierter Haupttest):** 7 gegen 19 Diskordante, exakter McNemar p = 0,0290, Risikodifferenz +7,5 pp [1,25; 13,75] → laut Protokoll „SUPPORTED“. Holm über drei Paare: p = 0,087. **Sensitivität ohne Quoten-erschöpfte Aufgaben (n = 131): p = 0,34, Differenz +3,1 pp [−1,5; 8,4]** — der Effekt verschwindet, wenn die Versorgungsausfälle entfernt werden. Er betrifft also **Verfügbarkeit** (Failover), nicht Kognition.
- A gegen C: p = 0,69; B gegen C: p = 0,136 → der Adaptive Modellzug (C) bringt nichts.
- **Korrektur:** Die gespeicherte Tokenzahl von B und C **unterschlägt** die Tokens fehlgeschlagener Anläufe (B +23.583 = +19 %, C +27.184 = +22 %). Der wahre Mehraufwand der Failover-Arme ist größer als berichtet. Die Genauigkeitsanalyse bleibt unberührt.
- D4 (A gegen B, andere Routenfamilie): 0,869 gegen 0,844, p = 0,22 — kein Unterschied.

### 4.4 D5/D6/D7 — Gedächtnis, Kalibrierung, Budget

- **D5:** 6 von 10 Aufgaben nur mit Gedächtnis, kein Kontrollarm. In zwei Aufgaben wurden 7 bzw. 8 Wissensaufrufe wiederverwendet; keine der beiden wurde gelöst (Status UNKNOWN). Settled: 2 von 6. D2: 18 Befunde veröffentlicht, 0 wiederverwendet. → kein Wirksamkeitsbeleg.
- **D6 (G2-Kalibrierung, 6 freie Modelle × 24 Aufgaben):** gpt-oss-120b 18/24 (0,75); Qwen 3/24; Nemotron-Super 1/24; Gemma, Llama, Mistral 0/24 (Auslieferung gleich Genauigkeit, d. h. praktisch keine Antworten geliefert; die Ursache wurde hier nicht einzeln geprüft). Ergebnis: `INSUFFICIENT_ELIGIBLE_LINEAGES` — **nur eine nutzbare Modelllinie**. Die Voraussetzung für unabhängige Mehrmodell-Prüfung war im freien Pool zeitweise nicht erfüllt.
- **D7:** Der historische D4-Lauf verbrauchte 60 Ausführungen für 14 genehmigte Aufrufe; 13 Abschneidungen (31.209 Tokens). Behoben und offline belegt, live nicht.

### 4.5 D8–D10 — OGI-010/011/012

- **OGI-010:** nie ausgeführt. **OGI-011:** blockiert durch Versorgung; kein konfirmatorischer Dispatch. Verbrauch: Versuch 1: 8 Receipts, 6.207 Tokens (4 beantwortete Arm-Läufe, Ausgaben nie gelesen); Smoke/Qualifikation: 77 Receipts, 27.882 Tokens (davon RATE_LIMITED 19, SEMANTIC_OUTPUT_FAILURE 13, PROVIDER_UNAVAILABLE 4).
- **OGI-012** (geparkt bei 2 von 96 Einheiten, Registerlaufregel „keine Zwischenergebnisse“ gilt weiter; die folgende Zeile ist **kein** Analyse-Blick und kein Look im Sinne der sequentiellen Grenzen): 26 Receipts, 19.626 Tokens, 2 × RATE_LIMITED. Beide Einheiten wurden von **allen** fünf Armen (drei Einzelmodelle, B, C) voll richtig beantwortet — Deckeneffekt bei n = 2. C benötigte **3** bzw. **11** Dispatches und 55 s bzw. 251 s; ein Einzelmodell 1 Dispatch und 3–18 s. In beiden Einheiten stand der Status von C auf `INCOMPLETE(SUPPLY)` bzw. `CONFLICT`; die endgültige Antwort kam vom Kompositionsschritt (`COMPOSER_UNVERIFIED`). Nicht entscheidungsfähig.

### 4.5b Verbrauch aller ausgewerteten Läufe (Receipts; `cost_usd` überall null = unbekannt)

| Lauf | Provider-Receipts | davon erfolgreich | berichtete Tokens | Wandzeit |
|---|---|---|---|---|
| D1b F1 (12 Aufgaben) | 12 | 12 | 5.401 | 120 s (Summe) |
| D1b F2 | 24 | 22 | 9.144 | 199 s (Summe) |
| D1c (F2+F3, davon 24 Suchaufrufe) | 81 | 69 | 68.755 | – |
| D2 Kontrolle | 118 | 42 | 34.090 | 806 s |
| D2 F3 | 854 | 462 | 818.165 | 15.059 s (+1 ohne Zeit) |
| D3 A / B / C | 139 / 175 / 174 | 114 / 126 / 121 | 111.951 / 147.252 / 153.311 | – |
| D4 A / B | 204 / 189 | 147 / 151 | 111.251 / 99.224 | – |
| OGI-011 Versuch 1 / Smoke | 8 / 77 | 4 / 41 | 6.207 / 27.882 | – |
| OGI-012 (2 Einheiten) | 26 | 24 | 19.626 | – |

Receipts zählen auch Fehlversuche; lokale Ablehnungen (`failure_receipts`, z. B. D3 46/34/39) sind keine Dispatches und stehen nicht darin.

### 4.6 D11 — RG/2 und der heutige Missionspfad

Reproduziert wurde nur das, was ein Test beobachten kann: Abläufe mit echten MangoMe-/PlumMe-/CherryMe-/AppleMe-Objekten, aber Fake-Provider, Scripted Antworten. Das ist **TECHNICAL_ONLY**. Aus Scripted Workern folgt keine Modellleistung.

---

## 5. Bewertung der Fähigkeiten A bis H

| | Frage | Status | Begründung und Evidenz |
|---|---|---|---|
| **A** | Problemlösung | **INDICATED** (ältere Architektur); heutiger Missionspfad **TECHNICAL_ONLY** | Die ältere Kette lieferte unabhängig bewertete richtige Antworten (D1a 3/3, D1c 5/5 bei Lieferung, OGI-012 2/2 Einheiten), aber ihre Qualität bei Lieferung ist nicht besser als die Kontrolle (D2: 9 volle von 18 gegen 11). Die Kontrolle löste 74 %. |
| **B** | Organisationsvorteil | **UNKNOWN** (kein gültiger Test); Beobachtungsrichtung ungünstig | D2 −0,56 [−0,74; −0,42], D1c −0,17 [−0,5; 0,25], D1a/OGI-012 Decke. Alle Vergleiche entweder durch Versorgungsmängel konfundiert, zu klein oder an der Decke. Es gibt keinen Beleg für einen Vorteil. |
| **C** | Verantwortungsteilung/unabhängige Prüfung | **UNKNOWN** empirisch; Mechanismus **TECHNICAL_ONLY** | OGI-012 t3-002: Verifier prüften 3 Quellen, promoteten 2, Status blieb CONFLICT; n = 1. RG/2-Unabhängigkeit (Gruppe und Familie) nur im Test. |
| **D** | Eskalation | **UNKNOWN**; Aufwand wächst nachweislich | Mehr Aufrufe ohne bessere Note: OGI-012 C 3/11 Dispatches gegen 1 bei gleicher Note; D2 24× Tokens bei schlechterem Ergebnis. Kein Beleg für Grenznutzen; Ex-post-Grenznutzen (`marginal`) ist erst seit RG/2 erfassbar und noch nie live gemessen. |
| **E** | Entscheidungsverdichtung | **TECHNICAL_ONLY** | Verdichtung mit Dissens/Lineage ist implementiert und offline belegt. In den realen Läufen stammte die Endantwort vom Kompositionsschritt, nicht vom Claim-Status (`COMPOSER_UNVERIFIED`). |
| **F** | Organisatorisches Gedächtnis | **UNKNOWN**; Mechanismus **TECHNICAL_ONLY** | D5 ohne Kontrollarm, 0 Lösungen mit Wiederverwendung; D2 0 Wiederverwendung. Zero-Call-Wiederverwendung offline gezeigt. |
| **G** | Ressourcenökonomie | **DEMONSTRATED** (beschreibend, ältere Architektur) | D2: 7,2× Receipts, 24× Tokens, 19× Wandzeit bei einem Viertel der Treffer. D3: Failover +19 % Tokens für +7,5 pp. `cost_usd` ist in 100 % der geprüften Receipts null: **Kosten in Währung unbekannt, nicht null**. |
| **H** | Robustheit | **INDICATED**; Failover (B gegen A) **DEMONSTRATED** im engen Sinn | Failover erhöht die Auslieferung (D3, aber nur durch Verfügbarkeit). Bei Versorgungsmangel enthielt sich F3 (31/50) statt zu raten, verbrauchte aber 854 Receipts. Wiederaufnahme nach Neustart und Budgetbegrenzung nur offline. Quotenerschöpfung, abgebrochene Ausführung und Modellmangel sind die dominierenden Befunde aller realen Läufe. |

Jede Zeile bezieht sich auf die **jeweils untersuchte Architektur**. Keine ältere Zahl gilt als Leistungsnachweis des heutigen PEACH-MISSION/1-Systems.

## 6. Abgrenzung der drei Ebenen

- **Technisch:** Komponenten laufen, Tests sind grün, Budget- und Identitätsketten sind offline konsistent. Das ist die Aussage von 336/240/455/92/311 Tests. Sie sagt nichts über Leistung.
- **Organisatorisch:** Die Verbindung MangoMe → PeachMe → CherryMe → PlumMe → AppleMe → MangoMe/OrangeMe → Evaluator ist offline mit echten Komponenten demonstriert. Im Betrieb scheitert sie an den Schnittstellen aus §1.4.
- **Wissenschaftlich:** Es fehlt der gültige, ausreichend große, unabhängig bewertete Vergleich Organisation gegen Kontrolle. Die vorhandenen Daten stützen die Hypothese nicht.

## 7. Gesamtbewertung der OGI-Hypothese

1. Es existiert **kein** Beleg für einen Organisationsvorteil.
2. Es existiert **keine** gültige Widerlegung, weil die einzigen großen negativen Vergleiche (D2, D1c) mit Versorgungsausfällen konfundiert sind.
3. Der einzige registrierte Haupttest mit „SUPPORTED“ (D3 H1) betrifft **Failover**, nicht Kognition, und verschwindet in der Sensitivität.
4. Die freie Versorgung selbst ist der dominierende Störfaktor: eine nutzbare Modelllinie in der Kalibrierung, hohe Raten von RATE_LIMITED/FORBIDDEN/SEMANTIC_OUTPUT_FAILURE, Abbrüche in den OGI-Läufen.
5. Die Methodik ist bereit (registrierte Grader, Cluster-Bootstrap, sequentielle Grenzen, eingefrorenes OGI-012-Paket); es fehlen gültige Daten.

## 8. Verbleibende entscheidungsrelevante Einschränkungen

1. **Kein gültiger Vergleich auf der heutigen Architektur.** Jede Leistungsaussage braucht neue Inferenz.
2. **Versorgung:** kostenlose Modelle liefern instabil; in der Kalibrierung war nur eine Linie nutzbar; Llama/Mistral/Gemma lieferten 0.
3. **Aufgabenvalidität:** D2 nutzt Entwurfsaufgaben ohne freigegebene Referenzen; D3/D4 sind Rechenaufgaben mit Deckeneffekt (100 % bei Lieferung).
4. **Kosten unbekannt:** `cost_usd` ist in den geprüften Receipts durchgehend null.
5. **Offene Betriebsschnittstellen** (§1.4) — der Missionspfad läuft nur offline.

## 9. Cutover-Zustand

- **Vorbereitet, nicht angewendet:** Release-Satz (§3), gestagter Worker, `rg2_cutover.py` (im Sandbox-Test: Preflight, Snapshot, Apply mit Tests vor Veröffentlichung, Rollback), `OWNER_APPROVAL.template.json`.
- **Preflight heute:** vier Fast-Forwards möglich; ein Blocker (PeachMe-Spiegel).
- **Zusätzlich nötig vor einem echten Betrieb** (nicht allein durch den Cutover erledigt): MangoMe im Worker-Venv importierbar machen oder eine MangoMe-Transportschicht festlegen; WorkIdentity-Quelle für Aurora; OrangeMe-Konfiguration; Egress-Policy.
- **Zwei getrennte Freigaben** (§10).

## Anhang A — Reproduktion

`run_all.sh` ruft nacheinander `repro/d1_eval001.py`, `d2_f3_vs_control.py`, `d3_route_arms.py`, `d5_misc.py`, `d6_resources.py` auf. Grundlage sind die in `INPUT_HASHES.sha256` gelisteten Dateien (Aufgaben, Ergebnisse, Noten, Analysen).

## Anhang B — Nicht reproduziert oder ohne Zugriff

- Fehlerklassen-Zahlen des D2-Berichts (FORBIDDEN 61 …) und „19/31“: anderer Ausschnitt/Zählweise; Gesamtzahlen reproduziert, Ausschnitt nicht (§4.1).
- „140 erfolgreiche Antworten im breiten F3-Lauf“ (Codex-Statuseintrag) und „948/107 freie Modelle“ (Katalog): Rohdaten nicht gefunden bzw. Katalogstand, nicht reproduziert.
- Live-Verhalten von RG/2, ParentBudget und Missionspfad: nur Offline-Tests, keine Betriebsdaten.
- Kostenwerte in Währung: nicht vorhanden.
- Keras-Gate (`MQ-GATE/1`): `INSUFFICIENT_EVIDENCE` (zu wenige Zeilen/Modelle, kein Basislinien-Vorsprung); OPE: „NOT_ALL_TARGETS_IDENTIFIABLE“ — keine Aussage.

## Anhang C — Bestehende Berichte, die dieses Dossier nutzt (keine parallele Wahrheit)

`evidence/20261014T-F3-vs-AUTO-CONTROL-DEV/REPORT.md`, `evidence/20261014T023511Z-DEV-F1DEV-F3DEV/REPORT.md`, `FRUITSTACK-EVAL-001/exec-2026-10-11/extra12-report.md`, `exploratory-summary.json`, `fs-integrity-005/REPORT_FS005.md`, `OGI-011_ARCHIVE_STATUS.md`, `ogi-012/PARKED_STATE.md`, `abc2-analysis/analysis.json`, `f2f3-free/calibration/pair-decision.json`.

## 10. Eigentümerentscheidung

**Freigabe 1 — Produktion (einzige zusammengefasste Freigabe, ohne neue Inferenz):** Cutover des Release-Satzes (§3) in der Reihenfolge PlumMe → AppleMe → PeachMe → CherryMe → Worker mit `rg2_cutover.py apply`. Sie muss mitentscheiden: (a) die PeachMe-Linie bzw. den fehlenden `sync/local-truth`-Spiegel, (b) die FruitStack-Eval-Zusammenführung (oder ausdrücklich „nicht Teil dieses Release“), (c) die WorkIdentity-Quelle für Aurora-Aufträge und den MangoMe-Zugang des Worker-Venvs, (d) die OrangeMe-Konfiguration, (e) die Egress-Policy. Danach muss die Truth-Writer-Quittung des Longrunners erneuert werden.

**Freigabe 2 — Forschungsinferenz (getrennt, providerwirksam):** Erst sie erlaubt gültige Daten für die offenen Fragen A–F. Mindestens: ein vorab registrierter Vergleich auf der heutigen Architektur (Organisation gegen registrierte Kontrolle auf demselben Modellpool und denselben Aufgaben, mit freigegebenen Referenzen und ausreichender Stichprobe); die Wiederaufnahme von OGI-012 ist ausdrücklich ein eigener Schritt und nur mit den dort geltenden Preflight-Regeln zulässig. Ohne diese Freigabe bleibt die wissenschaftliche Antwort „unentschieden“.

---

## 11. Wissenschaftliche Ursachen- und Potenzialanalyse (FRUITSTACK-SCIENCE-100, 2026-10-17)

Grundlage: dieselben 50 Entwicklungsaufgaben und Rohartefakte wie §4.1 (F3 9/50 vs. AUTO-Kontrolle 37/50), rein offline, keine Modell-Provider-Aufrufe. Reproduktion: `repro/d7_forensics.py` → `repro/d7_cases.json` (Fallrekonstruktion), `repro/d8_report.py` (Tabelle), `repro/d7_hgi_search_replay.json` (Such-Wiederholung, siehe 11.2). Referenzen gehen nur in die Bewertung ein, nie in eine Auswahl. **Die 50 Aufgaben bleiben Entwicklungsdaten; nichts hier ist konfirmatorisch.**

### 11.1 Ursachenverteilung (alle 50 Fälle; Rohdaten-Zuordnung, UNKNOWN nur wo Rohdaten nicht entscheiden)

| Ursache / verantwortlicher Prozessschritt | Fälle | davon Kontrolle voll richtig (= verlorenes Potenzial) |
|---|---|---|
| F3 voll richtig | 9 | – |
| **Keine Modellfrage gestellt: Retrieval lieferte keine zulässige Primärquelle (Host-Grounding-Gate)** (16) + Abruf nie erfolgreich (tech-03) | 17 | 14 |
| **Schlüsselstufe** lieferte nichts/UNKNOWN obwohl der Schlüssel in verifizierten Zitaten steht (Verdikt richtig, 0.5) | 7 | 5 (Rest: F3 > Kontrolle) |
| Schlüsselstufe falsch/nicht belegt (hist-09, tech-02) | 2 | 1 |
| **Verifikation lehnt wahrheitsgemäße Urteile ab** (Quorum/Teilbeleg/Zitatprüfung): hist-05, hist-08, org-01, sci-09, tech-01, tech-05 | 6 | 5 |
| Korrekter Vorschlag nie promotet (law-07, sci-05, tech-08) | 3 | 2 |
| Quellen abgerufen, aber Fakt nicht im Auszug (law-05, org-10, tech-10) | 3 | 2 |
| Verifier-Quorum nicht erreichbar (hist-04, Versorgungsausfälle) | 1 | 1 |
| Kein zulässiges Modell (law-03) | 1 | 1 |
| Zeitlimit 1200 s (org-06, Ursache innerhalb der Aufgabe nicht rekonstruierbar = UNKNOWN) | 1 | 1 |

„Versorgung" erklärt nur 3–4 Fälle (law-03, hist-04, org-06 und Teile von hist-08/org-01 über fehlende Verifier-Worker). Die große Lücke ist **Pipeline-Design**: 17 von 41 Nicht-Treffern entstehen, bevor ein Modell gefragt wird.

### 11.2 Was HOST_GROUNDING_INVALID tatsächlich auslöst (Antwort auf die Frage berechtigt/fehlerhaft)

1. **Es wird keine Modellantwort zurückgewiesen.** Das Label entsteht in `CherryMe/cherryme/plumme_bridge.py` (`_investigate_async`): für grounded Fragetypen (SCIENCE, REUSE, GAP) ruft die Bridge *vor* jedem Modellaufruf den Host-Provider (`KnowledgeFirstGrounder` → `LiveWebRetriever`) auf; **jede** Ausnahme daraus (auch `HOST_GROUNDING_UNAVAILABLE`, „No allowlisted primary source returned a usable excerpt", „search failed") wird zu `HOST_GROUNDING_INVALID` umbenannt. Der Text steht nur im Feld `note`; `events.jsonl` persistiert nur „All candidate providers failed." — der konkrete Grund ist in den Läufen **nicht** gespeichert (Befund: Telemetrielücke).
2. **Berechtigt oder fehlerhaft?** Für die 16 Null-Grounding-Aufgaben zeigt eine Wiederholung der Suche (nur Websuche, kein Modell; heutige Ergebnisse, daher indikativ): bei 12 von 16 lieferte die Suche Treffer, aber **10 von 12 hatten null Treffer auf der Primärquellen-Allowlist** (Wikipedia, Britannica, BIPM-nahe Fachseiten, gdpr-info.eu u. a. liegen nicht auf der Liste), 2 hatten 1–3 Allowlist-Treffer (Abruf/Auszug unbrauchbar), 4 Suchaufrufe scheiterten technisch (CalledProcessError, vermutlich Rate-Limit). Die **Kontrolle** (derselbe Retriever, gleiche Aufgaben) bekam bei 15 von 16 ebenfalls keine Quelle — und beantwortete 13 von 16 **aus dem Modellwissen richtig** (voll). Das Gate hat also keine falsche Aussage abgefangen; es hat **richtiges Modellwissen verhindert**, weil CherryMe grounded Fragen ohne Quelle gar nicht stellt. Das ist weder „berechtigte Zurückweisung einer unbelegten Behauptung" noch ein Validierungsfehler im Sinne fehlerhafter Zitat-/Hash-Prüfung, sondern ein **Designkonflikt**: Quellenpflicht als Vorbedingung für jede Frage vernichtet korrekte, aber unbelegte Erkenntnis (kritischer Fall der Fragestellung: FruitStack vernichtet korrekte Erkenntnisse selbst — am Code und an den Daten belegt, für diese 17 Aufgaben).
3. **Nicht geprüft/UNKNOWN:** ob zusätzlich Validierungsregeln (HTTPS, Hash, Duplikat nach Redirect: `seen` wird vor dem Redirect gesetzt, `validate()` lehnt doppelte `source_ref` nach Redirect ab) in einzelnen Fragen gültige Quellen verworfen haben; bei Aufgaben mit Abrufen aber HGI-Versuchen (z. B. 3–9 pro Aufgabe) ist der Grund nicht persistiert.
4. **Zweite Zurückweisungsstufe (Verifier, tatsächliche Urteile über Modellvorschläge):** Von 163 Quell-Verifier-Einträgen waren 63 PROMOTED (alle in Übereinstimmung mit der Referenz — Precision der Promotion in dieser Stichprobe 63/63). Abgewiesen: 40× NOT_ADDRESSED_BEIDE (Auszug enthält den Fakt nicht — berechtigt bzgl. Beleg, aber Folge der 1500-Zeichen-Auszugsauswahl), 32× Verifier-Worker fehlte (Versorgung; in 9 davon stimmte der vorhandene Worker mit der Referenz überein), 13× Workers uneinig (in 11 davon stimmte genau ein Worker mit der Referenz überein — das feste Zwei-Worker-Quorum kann ohne dritten Blick nicht entscheiden), 6× Zitat ungültig/uneinig (6/6 mit einem korrekten Worker), und **9× PARTIAL_SUPPORT_VALUE_MISSING mit beiden Workern = Referenz** (hist-05: „11" aus „Apollo 11" gilt als fehlender Anspruchswert; org-02/org-05: „2023"). Das sind **fehlerhafte Zurückweisungen durch die Regel „jeder ziffernhaltige Anspruchswert muss im Zitat stehen"**: Bezeichner (Missionsnummer) werden wie Werte behandelt. Konsequenz: hist-05 verloren (Kontrolle 1.0), org-05 auf 0.5 begrenzt.

### 11.3 Potenzialanalyse (vollständig richtig = 1.0; Halbtreffer separat)

| Größe | Wert | Definition / Beleg |
|---|---|---|
| Actual Organization (F3) | 9/50 voll (+9 Halb, 13.5 Punkte) | graded, §4.1 |
| Single Best (beste beobachtete Einzelinstanz) | AUTO-Kontrolle 37/50 voll (37.5 Punkte) | eine ungepinnte PlumMe-AUTO-Frage; kein Per-Modell-Vergleich möglich, da pro Aufgabe nur das Endmodell antwortet |
| Best-of-N Oracle (post hoc, nur Obergrenze) | **41/50 voll** (42.5 Punkte) | Vereinigung der *beobachteten* Endantworten von Kontrolle und F3; Referenz wirkte nur in der Bewertung |
| Lost Potential | 32 Aufgaben, 29 Punkte (Kontrolle > F3) | Tabelle 11.1, Spalte 3 |
| Unsolved Potential | 9 Aufgaben ohne vollständig richtigen Beitrag: hist-02, hist-08, law-07, org-04, org-10, tech-06 (beide 0.0) + 3 mit höchstens Halbtreffer (hist-07, org-03, tech-02) | in diesen Fällen enthielten die **beobachteten** Antworten die Lösung nicht |
| Beitrag, der nur F3 hatte | 4 voll (hist-01, org-09, law-09, tech-09) + 3 Halb (hist-07, org-03, tech-02) | **Achtung:** hist-01, hist-07, org-03, org-09 sind Fälle, in denen der Kontrollaufruf **0 Tokens/keine Antwort** lieferte (8 Kontrollausfälle insgesamt). Echter Wissenszuwachs durch Organisation gegenüber einer *antwortenden* Kontrolle: law-09, tech-09, tech-02 (3 Fälle) |

Grenze der Aussage: das beobachtete Oracle (41) ist keine theoretische Obergrenze des Modellpools. Pro Aufgabe wurde nur *eine* Kontrollantwort und eine F3-Entscheidung beobachtet; das, was andere Poolmodelle geantwortet hätten, ist **UNKNOWN** (die Pool-Zusammensetzung wechselte zudem durch Versorgungsausfälle). 100 % beobachtet nicht erreichbar: bei 9 Aufgaben enthält keine beobachtete Antwort die Lösung.

### 11.4 Organisationshypothese — was die Daten sagen

- **Erhalt korrekter Einzelbeiträge:** nein. 17 Aufgaben (Gate) + 7 (Schlüsselstufe) + 6 (Verifikation) + 3 (nie promotet) = 33 Fälle, in denen ein korrekter Beitrag (Modellwissen, Verdikt eines Workers oder Zitat) existierte oder hätte existieren können und die Organisation ihn nicht zum Endergebnis gemacht hat.
- **Zweite/dritte unabhängige Perspektive:** hilft dort, wo sie zugelassen ist — Verifier-Quorum promotete 63/63 mit Referenzübereinstimmung; die 11 + 6 Fälle mit genau einem korrekten Worker zeigen, dass bei Zwei-Worker-Uneinigkeit ein *dritter* Blick der naheliegende, aber nie vorhandene Mechanismus ist (das Quorum ist fest 2). Zusätzliche Beiträge **schaden**, wenn sie nur Veto-Rechte haben (Teilbeleg-Regel, Quorum, Quellenpflicht) statt Evidenz zu liefern: die Veto-/Auswahlstufen kosten in diesen Daten mehr korrekte Ergebnisse (22 Aufgaben: Verifikation 6, Vorschlag nie promotet 3, Quorum 1, Schlüsselstufe 9, Auszugsauswahl 3), als sie falsche abfangen (in keinem Fall wurde ein falsches Verdikt promotet; die Falsch-Positiv-Rate der Promotion war 0, aber auch die Ausbeute 9/50).
- **Mehr Modelle: Wissen oder nur Kosten?** Aufwand F3 818 165 Tokens/854 Receipts gegenüber Kontrolle 34 090 Tokens (≈ 24×) für 9 vs. 37 volle Treffer. Gewinn an Wissen nachweisbar nur in 3 Fällen (law-09, tech-09, tech-02). Kein Beleg, dass mehr Modelle Wissen *addieren*; Beleg, dass sie Kosten addieren.
- **Systematisch vs. versorgungsbedingt:** Designregeln (deterministisch wiederholbar) 29 Fälle (Quellenpflicht/Allowlist 17, Schlüsselstufe 9, Auszugsauswahl 3); gemischt Regel + fehlende Verifier 6 (Verifikationsstufe); rein versorgungsbedingt 3 (law-03, hist-04, org-06 unklar/UNKNOWN).
- **Mehrheitsentscheid/Schweigen:** „UNKNOWN" statt Antwort (Schlüsselstufe, kein Grounding) ist hier kein Zeichen von Sorgfalt, sondern Informationsverlust: 13 der 17 Gate-Fälle hatte die Kontrolle richtig beantwortet.

### 11.5 Das 100-%-Ziel als messbares Ziel (Stufenleiter)

1. Sind alle richtigen Antworten in den beobachteten Beiträgen enthalten? **Nein:** 41/50 (82 %); bei 9 Aufgaben nicht. (Ob andere Poolmodelle sie enthielten: UNKNOWN.)
2. Erkennt die Organisation sie? **Nein:** F3 nutzt 9 von 41 (22 %).
3. Kann sie fehlende Lösungen erzeugen? **Nicht belegt:** kein Fall, in dem F3 allein aus Evidenz eine Antwort geliefert hätte, die die Kontrolle (mit Antwort) verfehlte, außer law-09, tech-09, tech-02.
4. Fangen unabhängige Prüfungen Fehler ohne Wissensverlust? **Fehler gefangen: ja (0 falsche Promotionen), ohne Wissensverlust: nein** (22 Aufgaben mit verlorenem korrektem Beitrag, s. 11.4).
5. Schließt die gemeinsame Entscheidung alle Aufgaben? **Nein.** Die Grenze: solange keine beobachtete Antwort die Lösung enthält (9 Aufgaben), kann Konsolidierung nichts liefern; 100 % ist für dieses Benchmark mit dem beobachteten Material **nicht erreichbar**, 82 % ist die beobachtete Auswahl-Obergrenze.

### 11.6 Übertragbarkeit auf RG/2

Belegt (Code/Tests, offline): RG/2 hat kein Quellenpflicht-Gate vor der Frage, keine feste Quorum-Veto-Regel und kann ohne Modellaufruf auf bestehende Erkenntnis zurückgreifen (Zero-Call-Pfad); es plant Verantwortlichkeiten dynamisch. Daraus folgt **nicht**, dass RG/2 die obigen Verluste vermeidet: die Verifier-/Schlüsselstufen-Regeln stammen aus CherryMe-Legacy und wurden hier nicht mit RG/2 gemessen. Es gibt **keine** empirische Messung von RG/2 auf denselben Aufgaben; historische F3-Zahlen werden nicht übertragen. Nicht untersucht: Verhalten der Konsolidierung bei echter Meinungsverschiedenheit mehrerer unabhängiger Modelle, Wirkung eines dritten Verifiers, Wirkung der Allowlist auf RG/2.

### 11.7 Vorregistrierbares Studiendesign (nächster Schritt)

- **Aufgaben:** frisches konfirmatorisches Set (nicht die 50 Dev-Aufgaben), Referenzen vorab freigegeben, Seed nach Code-Freeze; stratifiziert nach Fragetyp (Fakt, Mehrquellen, widersprüchlich, ohne verfügbare Primärquelle).
- **Arme (gleiche Aufgaben, gleicher Modellpool, gleiche Informationszugänge, gleiche Budgets pro Aufgabe):** (A) bestes Einzelmodell mit gleichem Quellenzugang; (B) unorganisiert-multi: dieselben Modelle, feste Regel (Mehrheit/first-valid), keine Verifikation; (C) volle Organisation (RG/2) mit Quellenzugang *und* dem Recht, ungegründete Antworten als „UNGEBELEGT" zu liefern; optional (D) Ablation: C ohne Veto-Stufen. Interleaved, zufällige Reihenfolge, ITT-Analyse.
- **Bewerter:** unabhängiger Grader (`fse inquiry grade`), Referenzen nur dort; Ausfälle der Versorgung als eigene Kategorie, nicht als Fehler der Organisation.
- **Messgrößen:** Erfolgsrate (voll/halb), Abdeckung und Abstention (Silence ≠ Intelligenz → Abstention separat, nicht als „richtig"), Kosten, tatsächliche Providerdispatches, Wandzeit; **Konsolidierungsqualität als eigenes Objekt:** Anteil der beobachtet korrekten Einzelbeiträge, die die Endauswahl erreichen (Preservation Rate), Anteil falscher Beiträge, die ausgeschlossen werden (Rejection Precision), Anzahl verlorener korrekter Beiträge je Prozessschritt.
- **Entscheidungsregel:** C > bestes von A und B bei vorab festgelegtem Margin m auf Cluster-robustem Test; Powerrechnung gemäß OGI-011-Revision 3 als Ausgangspunkt (N ≈ 96 Einheiten für +0.20), mit Ressourcenvergleich.
- **Vorbedingungen aus dieser Analyse (vor jedem Lauf zu beheben, sonst misst die Studie wieder das Gate):** Persistenz des echten Grounding-Fehlergrunds; Erlaubnis ungegründeter Fragen mit Kennzeichnung; Bezeichner (Missionsnummer) nicht als Anspruchswert behandeln; dritter Verifier bei 1:1-Uneinigkeit; Schlüsselstufe mit Wiederholung statt Einzelaufruf.

### 11.8 Fall-für-Fall-Tabelle (50 Aufgaben)

| Aufgabe | Ref (Verdikt/Schlüssel) | Kontrolle | F3 | Ursache (Prozessschritt) | Befund | F3-Receipts/Tokens | Kontr.-Tokens |
|---|---|---|---|---|---|---|---|
| inq-hist-01 | SUPPORTED/1957-03-25 | 0.0 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 6/5310 | 0 |
| inq-hist-02 | SUPPORTED/1989-11-09 | 0.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 0 |
| inq-hist-03 | REFUTED/1990-10-03 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 490 |
| inq-hist-04 | REFUTED/1992-02-07 | 1.0 | 0.0 | VERIFIER_QUORUM_UNREACHABLE | 2 Quelle(n) ohne zweiten Verifier; Versuche {'OK': 1, 'HOST_GROUNDING_INVALID': 5, 'NO_ELIGIBLE_NEURON': 6}; Ausfälle {'BILLING_OR_CREDIT_EXHAUSTED': 3, 'RATE_LIMITED': 3 | 7/1812 | 535 |
| inq-hist-05 | SUPPORTED/1969-07-20 | 1.0 | 0.0 | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifier-Urteil in Richtung Wahrheit, nicht promotet: ['PARTIAL_SUPPORT_VALUE_MISSING', 'WORKERS_DISAGREE', 'PARTIAL_SUPPORT_VALUE_MISSING', 'PARTIAL_SUPPORT_VALUE_MISSIN | 46/56257 | 1213 |
| inq-hist-06 | REFUTED/2002-01-01 | 1.0 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 37/40822 | 1014 |
| inq-hist-07 | SUPPORTED/1948-12-10 | 0.0 | 0.5 | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Verdikt richtig; Schlüssel steht in verifizierten Zitaten, wurde aber nicht extrahiert (Ausgabe 'UNKNOWN') | 11/4286 | 0 |
| inq-hist-08 | REFUTED/2009-12-01 | 0.0 | 0.0 | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifier-Urteil in Richtung Wahrheit, nicht promotet: ['VERIFIER_WORKER_MISSING'] | 6/3298 | 0 |
| inq-hist-09 | REFUTED/1985-06-14 | 1.0 | 0.5 | KEY_EXTRACTION_ERROR | Verdikt richtig; Schlüsselstufe lieferte '1990-06-19' statt '1985-06-14' (key_grounded=True) | 50/52412 | 1360 |
| inq-hist-10 | SUPPORTED/1989 | 1.0 | 0.5 | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Verdikt richtig; Schlüssel steht in verifizierten Zitaten, wurde aber nicht extrahiert (Ausgabe 'UNKNOWN') | 9/4355 | 892 |
| inq-law-01 | SUPPORTED/4 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 504 |
| inq-law-02 | SUPPORTED/2018-05-25 | 1.0 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 27/32130 | 326 |
| inq-law-03 | REFUTED/72 | 1.0 | 0.0 | NO_ELIGIBLE_MODEL | PlumMe: keine zulässige Route ({'NO_ELIGIBLE_NEURON': 6, 'HOST_GROUNDING_INVALID': 2}) | 4/0 | 865 |
| inq-law-04 | SUPPORTED/1689 | 1.0 | 0.5 | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Verdikt richtig; Schlüssel steht in verifizierten Zitaten, wurde aber nicht extrahiert (Ausgabe 'UNKNOWN') | 29/31156 | 860 |
| inq-law-05 | SUPPORTED/2025-02-02 | 1.0 | 0.0 | RETRIEVED_BUT_NOT_ADDRESSED | Quellen abgerufen; Verifier ['WORKERS_DISAGREE', 'NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'VERIFIER_WORKER_MISSING', 'VERIFIER_WORKER_MISSING'] | 35/22487 | 1374 |
| inq-law-06 | REFUTED/2025-08-02 | 1.0 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 34/33798 | 3297 |
| inq-law-07 | REFUTED/1 | 0.0 | 0.0 | CORRECT_PROPOSAL_NOT_RECOGNIZED | Vorschlag mit richtigem Verdikt ({'REFUTED': 4, 'UNKNOWN': 4}) nie promotet; Verifier ['NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BO | 26/25784 | 649 |
| inq-law-08 | SUPPORTED/3 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 410 |
| inq-law-09 | REFUTED/2065 | 0.0 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 34/38902 | 532 |
| inq-law-10 | REFUTED/16 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 258 |
| inq-org-01 | SUPPORTED/2013-07-01 | 1.0 | 0.0 | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifier-Urteil in Richtung Wahrheit, nicht promotet: ['VERIFIER_WORKER_MISSING'] | 6/3796 | 1590 |
| inq-org-02 | SUPPORTED/2023-04-04 | 1.0 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 26/28213 | 820 |
| inq-org-03 | REFUTED/2024-03-07 | 0.0 | 0.5 | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Verdikt richtig; Schlüssel steht in verifizierten Zitaten, wurde aber nicht extrahiert (Ausgabe 'UNKNOWN') | 12/9154 | 0 |
| inq-org-04 | REFUTED/2020-01-31 | 0.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 0 |
| inq-org-05 | SUPPORTED/20 | 1.0 | 0.5 | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Verdikt richtig; Schlüssel steht in verifizierten Zitaten, wurde aber nicht extrahiert (Ausgabe 'UNKNOWN') | 30/31152 | 942 |
| inq-org-06 | SUPPORTED/51 | 1.0 | 0.0 | BUDGET_ABORT | Zeitlimit (1200 s) ohne Abschluss: 46 Receipts, Retrieval 10/10; Ergebnis nie geschrieben (Ursache innerhalb der Aufgabe nicht rekonstruierbar) | 46/53451 | 645 |
| inq-org-07 | REFUTED/1948-04-07 | 1.0 | 0.5 | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Verdikt richtig; Schlüssel steht in verifizierten Zitaten, wurde aber nicht extrahiert (Ausgabe 'UNKNOWN') | 29/34394 | 1200 |
| inq-org-08 | REFUTED/1954 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 347 |
| inq-org-09 | SUPPORTED/1998-06-01 | 0.0 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 43/55563 | 0 |
| inq-org-10 | REFUTED/193 | 0.0 | 0.0 | RETRIEVED_BUT_NOT_ADDRESSED | Quellen abgerufen; Verifier ['NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH'] | 19/22368 | 0 |
| inq-sci-01 | SUPPORTED/299792458 | 1.0 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 23/26631 | 402 |
| inq-sci-02 | REFUTED/2019-05-20 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 603 |
| inq-sci-03 | SUPPORTED/4 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 596 |
| inq-sci-04 | SUPPORTED/-273.15 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 388 |
| inq-sci-05 | REFUTED/candela | 1.0 | 0.0 | CORRECT_PROPOSAL_NOT_RECOGNIZED | Vorschlag mit richtigem Verdikt ({'REFUTED': 4}) nie promotet; Verifier [] | 5/8950 | 444 |
| inq-sci-06 | REFUTED/8 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 284 |
| inq-sci-07 | SUPPORTED/7 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 688 |
| inq-sci-08 | REFUTED/5730 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 623 |
| inq-sci-09 | REFUTED/384400 | 1.0 | 0.0 | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifier-Urteil in Richtung Wahrheit, nicht promotet: ['QUOTE_INVALID_OR_DISAGREE', 'WORKERS_DISAGREE'] | 19/21450 | 964 |
| inq-sci-10 | SUPPORTED/8848.86 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 561 |
| inq-tech-01 | SUPPORTED/8446 | 1.0 | 0.0 | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifier-Urteil in Richtung Wahrheit, nicht promotet: ['QUOTE_INVALID_OR_DISAGREE', 'VERIFIER_WORKER_MISSING'] | 34/15182 | 679 |
| inq-tech-02 | REFUTED/9114 | 0.0 | 0.5 | KEY_EXTRACTION_ERROR | Verdikt richtig; Schlüsselstufe lieferte 'UNKNOWN' statt '9114' (key_grounded=False) | 29/33020 | 412 |
| inq-tech-03 | SUPPORTED/8259 | 1.0 | 0.0 | RETRIEVAL_FETCH_FAILED | Abrufe {None: 12}, keiner brauchbar; Versuche {'HOST_GROUNDING_INVALID': 8} | 0/0 | 506 |
| inq-tech-04 | SUPPORTED/2023-10-02 | 1.0 | 0.5 | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Verdikt richtig; Schlüssel steht in verifizierten Zitaten, wurde aber nicht extrahiert (Ausgabe 'UNKNOWN') | 34/6857 | 801 |
| inq-tech-05 | REFUTED/3.13 | 1.0 | 0.0 | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifier-Urteil in Richtung Wahrheit, nicht promotet: ['WORKERS_DISAGREE', 'WORKERS_DISAGREE'] | 52/44300 | 2921 |
| inq-tech-06 | SUPPORTED/2022-09-13 | 0.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 669 |
| inq-tech-07 | SUPPORTED/128 | 1.0 | 0.0 | NO_GROUNDING_RETRIEVAL_EMPTY | alle 8 Versuche HOST_GROUNDING_INVALID, 0 Abrufe, 0 Modellaufrufe: der Host lieferte keine zulässige Primärquelle; es gibt keinen ungegründeten Pfad | 0/0 | 319 |
| inq-tech-08 | REFUTED/256 | 1.0 | 0.0 | CORRECT_PROPOSAL_NOT_RECOGNIZED | Vorschlag mit richtigem Verdikt ({'REFUTED': 1, 'UNKNOWN': 2}) nie promotet; Verifier ['NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'VERIFIER_WORKER_MISSING'] | 33/18351 | 208 |
| inq-tech-09 | REFUTED/2008-12-03 | 0.5 | 1.0 | F3_CORRECT | Antwort vollständig richtig | 31/30327 | 649 |
| inq-tech-10 | REFUTED/4 | 1.0 | 0.0 | RETRIEVED_BUT_NOT_ADDRESSED | Quellen abgerufen; Verifier ['NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'NOT_ADDRESSED_BOTH', 'VERIFIER_WORKER_MISSING'] | 22/22197 | 1250 |

Hinweis: Kontroll-Tokens 0 = Kontrollaufruf ohne Antwort (Versorgungsausfall, 8 Aufgaben). Zeilen mit "Keine Modellfrage" = 0 Modellaufrufe auf F3-Seite.


---

## 12. Kognitive Wiederherstellung (FRUITSTACK-COGNITIVE-RECOVERY/1, 2026-10-17)

**Änderung:** CherryMe 0.4.1, Branch `cc/cognitive-recovery-001` (Basis `cc/cherryme-responsibility-brain` 62379fc; Commits 8f09556 und 5a6adad, nicht gemergt, nicht installiert; Volltest 354 passed). Keine neue Architektur, keine zweite Bewertungs-Engine; PlumMe, MangoMe, OrangeMe, AppleMe unverändert.

| Verlustmechanismus (SCIENCE-100) | Korrektur | Code |
|---|---|---|
| Quellenpflicht verhindert die Frage | Frage wird gestellt; Antwort = UNVERIFIED-Kandidat (nie Evidenz, nie Claim-Status, nie Wissensspeicher/Projektgedächtnis); Claim endet INCOMPLETE(UNVERIFIED); nur ein Kandidat je Claim, keine weiteren Modelle für dasselbe Retrieval-Problem; verfügbare, aber nicht primäre Treffer nur als Leads | `plumme_bridge._investigate_core`, `engine`, `outcome` |
| HOST_GROUNDING_INVALID undifferenziert | persistierte Ursachen `NO_ADMISSIBLE_SOURCE`, `NO_SEARCH_RESULTS`, `RETRIEVAL_ERROR` (Schritt SEARCH/ALLOWLIST/FETCH, Zähler, keine Inhalte), `INVALID_GROUNDING` (fail-closed), `NO_RETRIEVER` (Konfiguration); Retrieval-Fehler ist kein Provider-Fehler (`retrieval_failures`, Terminal-Ursache RETRIEVAL), belastet keinen Worker | `host_grounding.grounding_failure`, `host_retrieval` |
| Bezeichner wie Zahlenwerte | Subjekt-Bezeichner („Apollo 11“, „TLS 1.3“) müssen in der QUELLE stehen, nicht im Zitat; behauptete Werte (Datum, Zahl) weiter im Zitat Pflicht | `verification.split_claim_values` |
| festes Zwei-Worker-Quorum | dritter unabhängiger Verifier bei Dissens (`max_workers=3`), Relation braucht zwei übereinstimmende Worker; ungelöster Dissens bleibt erhalten, verifiziert nichts | `verification.EvidenceVerifier` |
| Schlüsselstufe UNKNOWN | deterministische Extraktion aus verifizierten Zitaten (Typ aus Frage, REFUTED verwirft Claim-Wert, thematische Überlappung Pflicht, Gleichstand = AMBIGUOUS); Delegation nur einmal bei echter Mehrdeutigkeit, Wert muss wörtlich in verifiziertem Zitat stehen; Kette protokolliert | `keys.extract_key/resolve_key` |
| Beiträge gehen unbemerkt verloren | Beitragsbuch: Worker, Evidenz, Status (UNVERIFIED/SOURCE_BACKED/DISSENT/VERIFIED), Disposition, Grund, `potentially_lost`; in `outcomes.jsonl`; nur VERIFIED+ACCEPTED ist gedächtnisfähig | `contributions`, `engine._ledger_summary` |

### 12.1 Fallweise Abnahme (Offline-Replay der neuen Codeversion auf aufgezeichneten Daten; Reproduktion `repro/d9_cognitive_replay.py` → `repro/d9_result.json`, Tabelle `repro/d10_sec12.py`)

Regeln: keine neuen Provider-Aufrufe; Referenzen nur zur nachträglichen Auswertung; wo eine neue Modellantwort nötig wäre, steht „nicht abspielbar“. **Es wird keine neue Erfolgsquote behauptet.**

| Aufgabe | Klasse | vorher | Replay mit neuem Code | Mechanismus | Rest |
|---|---|---|---|---|---|
| inq-hist-02 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat UNKNOWN; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | keine aufgezeichnete Modellantwort zum Abspielen |
| inq-hist-03 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat REFUTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-law-01 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat SUPPORTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-law-08 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat SUPPORTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) RETRIEVAL_ERROR@FETCH | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-law-10 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat REFUTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-org-04 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat UNKNOWN; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) RETRIEVAL_ERROR@FETCH | **BESEITIGT** | keine aufgezeichnete Modellantwort zum Abspielen |
| inq-org-08 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat REFUTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) RETRIEVAL_ERROR@SEARCH | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-sci-02 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat REFUTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-sci-03 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat SUPPORTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-sci-04 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat SUPPORTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-sci-06 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat REFUTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-sci-07 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat SUPPORTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) RETRIEVAL_ERROR@SEARCH | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-sci-08 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat REFUTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-sci-10 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat SUPPORTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) RETRIEVAL_ERROR@SEARCH | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-tech-03 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat SUPPORTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) RETRIEVAL_ERROR@FETCH | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-tech-06 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat REFUTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) NO_ADMISSIBLE_SOURCE@ALLOWLIST | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 0.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-tech-07 | 17 Vorab-Blockade | 0 Modellaufrufe, HOST_GROUNDING_INVALID×8 | Frage gestellt (1 Dispatch), UNVERIFIED-Kandidat SUPPORTED; Ergebnis INCOMPLETE(UNVERIFIED); Wissensspeicher 0; Ursache (Replay) RETRIEVAL_ERROR@SEARCH | **BESEITIGT** | Kandidat bleibt unbelegt (Kontrolle 1.0); Richtigkeit nicht Teil dieser Abnahme |
| inq-hist-07 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: keine Antwort); Schlüssel in verif. Zitaten: True | DETERMINISTIC 1948-12-10 SINGLE_CANDIDATE | **BESEITIGT** | Wert stimmt mit Referenz (nur Auswertung) |
| inq-hist-09 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: Antwort 'ne 1990.\nKEY: 1990-06-19'); Schlüssel in verif. Zitaten: True | AMBIGUOUS  TOPICAL_OVERLAP_TOO_LOW | **TEILWEISE (1 Delegationsaufruf nötig, nicht abspielbar)** | mehrdeutig -> bewusst nicht geraten |
| inq-hist-10 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: keine Antwort); Schlüssel in verif. Zitaten: True | DETERMINISTIC 1989 SINGLE_CANDIDATE | **BESEITIGT** | Wert stimmt mit Referenz (nur Auswertung) |
| inq-law-04 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: keine Antwort); Schlüssel in verif. Zitaten: True | NOT_IN_EVIDENCE  NO_CANDIDATE_OF_TYPE_IN_VERIFIED_QUOTES | **OFFEN** | Wert nicht in verifizierter Evidenz |
| inq-org-03 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: keine Antwort); Schlüssel in verif. Zitaten: True | DETERMINISTIC 2024-03-07 SINGLE_CANDIDATE | **BESEITIGT** | Wert stimmt mit Referenz (nur Auswertung) |
| inq-org-05 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: keine Antwort); Schlüssel in verif. Zitaten: True | AMBIGUOUS  UNRESOLVED_AMBIGUITY | **TEILWEISE (1 Delegationsaufruf nötig, nicht abspielbar)** | mehrdeutig -> bewusst nicht geraten |
| inq-org-07 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: keine Antwort); Schlüssel in verif. Zitaten: True | AMBIGUOUS  UNRESOLVED_AMBIGUITY | **TEILWEISE (1 Delegationsaufruf nötig, nicht abspielbar)** | mehrdeutig -> bewusst nicht geraten |
| inq-tech-02 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: Antwort 'KEY: UNKNOWN'); Schlüssel in verif. Zitaten: False | AMBIGUOUS  TOPICAL_OVERLAP_TOO_LOW | **TEILWEISE (1 Delegationsaufruf nötig, nicht abspielbar)** | mehrdeutig -> bewusst nicht geraten |
| inq-tech-04 | 9 Schlüsselverlust | KEY UNKNOWN (Schlüsselstufe: keine Antwort); Schlüssel in verif. Zitaten: True | DETERMINISTIC 2023-10-02 SINGLE_CANDIDATE | **BESEITIGT** | Wert stimmt mit Referenz (nur Auswertung) |
| inq-hist-05 | 6 Verifikationsfehler | PARTIAL_SUPPORT_VALUE_MISSING×7, WORKERS_DISAGREE×1 | abgespielt: NONE -> SUPPORTED | **BESEITIGT** | Bezeichner-Regel + Quelle enthält '11' |
| inq-hist-08 | 6 Verifikationsfehler | VERIFIER_WORKER_MISSING×2 | abgespielt: NONE -> NONE | **GEÄNDERT, NICHT ABSPIELBAR** | benötigt dritten Verifier bzw. fehlende Worker = neue Modellantworten; Versorgungslücke bleibt Versorgungslücke |
| inq-org-01 | 6 Verifikationsfehler | VERIFIER_WORKER_MISSING×3 | abgespielt: NONE -> NONE | **GEÄNDERT, NICHT ABSPIELBAR** | benötigt dritten Verifier bzw. fehlende Worker = neue Modellantworten; Versorgungslücke bleibt Versorgungslücke |
| inq-sci-09 | 6 Verifikationsfehler | VERIFIER_WORKER_MISSING×1, QUOTE_INVALID_OR_DISAGREE×1, WORKERS_DISAGREE×1 | abgespielt: NONE -> NONE | **GEÄNDERT, NICHT ABSPIELBAR** | benötigt dritten Verifier bzw. fehlende Worker = neue Modellantworten; Versorgungslücke bleibt Versorgungslücke |
| inq-tech-01 | 6 Verifikationsfehler | QUOTE_INVALID_OR_DISAGREE×1, VERIFIER_WORKER_MISSING×1 | abgespielt: NONE -> NONE | **GEÄNDERT, NICHT ABSPIELBAR** | benötigt dritten Verifier bzw. fehlende Worker = neue Modellantworten; Versorgungslücke bleibt Versorgungslücke |
| inq-tech-05 | 6 Verifikationsfehler | NOT_ADDRESSED_BOTH×6, WORKERS_DISAGREE×3, VERIFIER_WORKER_MISSING×3 | abgespielt: NONE -> NONE | **GEÄNDERT, NICHT ABSPIELBAR** | benötigt dritten Verifier bzw. fehlende Worker = neue Modellantworten; Versorgungslücke bleibt Versorgungslücke |
| inq-law-07 | 3 nicht übernommene Vorschläge | Vorschläge {'REFUTED': 4, 'UNKNOWN': 4} verworfen, nicht aufgezeichnet | Ledger: PROPOSAL / SOURCE_BACKED / RETAINED_UNVERIFIED, in potentially_lost sichtbar | **TEILWEISE** | nicht mehr verloren, aber ohne Verifikation weiterhin nicht übernommen |
| inq-sci-05 | 3 nicht übernommene Vorschläge | Vorschläge {'REFUTED': 4} verworfen, nicht aufgezeichnet | Ledger: PROPOSAL / SOURCE_BACKED / RETAINED_UNVERIFIED, in potentially_lost sichtbar | **TEILWEISE** | nicht mehr verloren, aber ohne Verifikation weiterhin nicht übernommen |
| inq-tech-08 | 3 nicht übernommene Vorschläge | Vorschläge {'REFUTED': 1, 'UNKNOWN': 2} verworfen, nicht aufgezeichnet | Ledger: PROPOSAL / SOURCE_BACKED / RETAINED_UNVERIFIED, in potentially_lost sichtbar | **TEILWEISE** | nicht mehr verloren, aber ohne Verifikation weiterhin nicht übernommen |

### 12.2 Ergebnis der Abnahme

- **17 Vorab-Blockaden:** Mechanismus in 17/17 beseitigt (Frage gestellt, Kandidat UNVERIFIED, Claim-Status unverändert, nichts im Wissensspeicher, kein Provider-Fehler). Zum Abspielen lag in 15/17 eine aufgezeichnete Modellantwort der Kontrolle vor. Die Ursachen sind aus einer heutigen Suchwiederholung abgeleitet (die Läufe haben sie nicht persistiert). Dass die zurückgehaltenen Kandidaten teilweise inhaltlich mit der Referenz übereinstimmen (14 von 15), ist **kein Leistungsnachweis**: die Antworten stammen aus dem Kontrollarm und bleiben UNVERIFIED.
- **9 Schlüsselverluste:** 4 beseitigt (deterministisch, alle vier stimmen mit der Referenz überein), 4 bewusst nicht geraten (Gleichstand/Mehrdeutigkeit; erst ein einziger Delegationsaufruf löst sie, nicht abspielbar), 1 Wert steht nicht in der Evidenz (law-04: Wert in „2024/1689“-Form, nicht unterstützt). Restrisiko: ein deterministischer Wert kann falsch sein, wenn die verifizierten Zitate einen anderen Wert gleichen Typs enthalten; die Kette ist protokolliert (im Replay trat das nicht auf, die früher beobachteten Fehlgriffe `hist-09`, `tech-02` werden jetzt als mehrdeutig abgewiesen).
- **6 Verifikationsfehler:** 1 beseitigt (hist-05: Bezeichner-Regel), 5 geändert, aber ohne neue Modellantworten nicht abspielbar (dritter Verifier bzw. fehlende Verifier-Worker; fehlende Versorgung bleibt Versorgungslücke). Ein Teil der Blockade bleibt gewollt: `2023` in org-02/org-05 ist ein behaupteter Wert und muss im Zitat stehen.
- **3 nicht übernommene Vorschläge:** nicht mehr verloren (Ledger), aber weiterhin nicht übernommen, solange keine Verifikation sie trägt.
- **Sicherheitsprüfung (nichts fälschlich VERIFIED):** im Relations-Replay über alle 50 Aufgaben ergibt der neue Code keinen Claim-Status, der der Referenz widerspricht (0 Abweichungen; alt: 0). Die Prüfung ist konservativ (dritte Verifier-Antworten und Werte aus nicht aufgezeichneten Zitaten werden nicht gezählt). Zusätzlich sichern 18 neue Tests ab: ungegründete Antworten werden nie Evidenz, Claim-Status, Wissensspeichereintrag oder gedächtnisfähig; ein einzelner Worker verifiziert nie; ungelöster Dissens verifiziert nichts.

### 12.3 Verbleibende wissenschaftliche Einschränkungen

1. Keine Erfolgsquote: das Replay zeigt, dass Mechanismen nicht mehr greifen, nicht dass FruitStack mehr Aufgaben löst. Die 50 Dev-Aufgaben bleiben Diagnose-/Regressionsmaterial.
2. Nicht abgedeckt, weil nicht in der Anordnung: abgerufen, aber Fakt nicht im Auszug (law-05, org-10, tech-10), Quorum durch Versorgungsausfall (hist-04), kein zulässiges Modell (law-03), Zeitlimit (org-06).
3. Die Endkomposition des Harness (`runners/f2f3_epoch2.py`, eingefroren) nutzt die neuen Funktionen noch nicht; ein unverifizierter Kandidat muss dort als solcher gekennzeichnet ausgegeben werden (eigene Kennzahl „verifiziert richtig“ vs. „unverifiziert richtig“), sonst vermischt eine Bewertung beides.
4. Die neue Codeversion ist weder gemergt noch installiert (Produktion unverändert 0.3.4); RG/2 wurde nicht gegen Kontrolle gemessen.
5. Die Ursache der Vorab-Blockaden stammt aus einer Suchwiederholung von heute; die Läufe haben sie nicht aufgezeichnet.

Damit ist die Voraussetzung geschaffen, RG/2 erstmals gegen eine unabhängige Kontrolle zu messen (Studiendesign §11.7); eine Messung hat nicht stattgefunden.


---

## 13. Kognitive Integration (FRUITSTACK-COGNITIVE-INTEGRATION/2, 2026-10-17)

**Stand:** CherryMe 0.4.2 (`cc/cognitive-recovery-001`, a70fa36), PeachMe 0.8.4 (`cc/peachme-cherryme-budget-bridge`, Test-Commit 712e07f), FruitStack-Eval (`cc/fse-rg2-evidence`, Commit siehe 13.10). Nichts gemergt, nichts installiert, keine Inferenz, OGI-012 und alle eingefrorenen Protokolle unberührt. Dieser Abschnitt **ersetzt** die Schlüsselzahlen aus §12 (dort 4 von 9; nach den Korrekturen unten 7 verifiziert + 1 unverifiziert gekennzeichnet + 1 in keinem Beitrag vorhanden); die übrigen Befunde aus §11/§12 bleiben.

### 13.1 Beitragserhalt
Jeder Versuch hinterlässt eine Zeile im bestehenden `ContributionLedger`: tatsächliche (begrenzte) Antwort, extrahierte Fakten und Schlüsselkandidaten, Frage und Verantwortung, Modell-Identität und Abstammung (PlumMe-`lineage_summary`), Evidenzverweise und Retrieval-Zustand, Selbstvertrauen (ausdrücklich nicht Korrektheit), Verifikationsstatus und Dissens, Grund der Disposition, Receipt und Ressourcen, stabile ID `CT-…`. Rohantworten stehen **nur** in der privaten Datei `contributions.jsonl` im CherryMe-Arbeitsbereich (0600, nach jeder Frage fortgeschrieben, optional `content_policy` als Datenschutzgrenze); Events, Outcomes, `organization_record()` und der MangoMe-Checkpoint tragen IDs und Digests. UNVERIFIED-Beiträge bleiben Arbeitshypothesen/Leads: sie sind nie Evidenz, nie Claim-Status, nie `KnowledgeStore`, nie OrangeMe (dort nur abgeschlossene verifizierte Befunde). Belege: `tests/test_cognitive_integration_002.py` (Erhalt, Privatheit, Unterbrechung), PeachMe `test_the_contribution_chain_survives_into_the_work_state…`.

### 13.2 Unabhängigkeit und Mehrmodell-Zusammenarbeit
- **Gefundener Fehler:** Im AUTO-Modus erhielten zwei verschiedene Worker-Karten dasselbe Modell (PlumMe wählt BEST; die Karte war nur eine Präferenz). Das widerspricht „Routenredundanz ist keine zweite Meinung“. **Behoben:** AUTO schließt Abstammungslinien aus, die für diese Frage über einen anderen Worker bereits beigetragen haben (`exclude_independence_keys`); gibt es keine zweite ausführbare Linie, entsteht `NO_INDEPENDENT_WORKER_AVAILABLE` und die Verantwortung bleibt ausdrücklich ungedeckt (Test mit einem Modell über zwei Routen).
- Der Ein-Kandidat-Deckel nach Retrieval-Fehler ist aufgehoben: der **unveränderte Retrieval-Fehler** wird je Frage gemerkt und nicht von jedem Worker wiederholt, die **kognitiven Beiträge** sind nicht gedeckelt (weitere unabhängige Gruppen, solange Ensemble-Ziel/Verantwortungsgraph es verlangen). Uneinigkeit ist ein Auflösungsbedarf, kein Veto (`unresolved_alternatives`).
- Unabhängigkeitsstatus nach `independence_between`: SAME_COGNITIVE_IDENTITY, DISTINCT_LINEAGE_CORRELATION_UNMEASURED, EMPIRICALLY_INDEPENDENT/CORRELATED (nur mit FSE-G2-Paarverdikt), INDEPENDENCE_UNKNOWN. In den vorhandenen Daten tragen alle Linien nur die Basis HEURISTIC (Modellfamilie).

### 13.3 Konsolidierung
`consolidate()` (CHERRY-CONSOLIDATION/2) beantwortet je Beitrag in Aktivierungsreihenfolge: vorher Bekanntes, Beitrag, Neues (strukturell: Verdikt, Schlüssel, Evidenzverweise — nicht lexikalisch), Beziehung (FIRST / SUPPORTS_EXISTING / CONTRADICTS_EXISTING / EXTENDS / REDUNDANT), unabhängige Stützung (nur mit empirischer Unabhängigkeit und SOURCE_BACKED/VERIFIED), im Endergebnis berücksichtigt, potenziell verloren, Ressourcenwert. `present_decision()`/`render_decision()` geben ein Ergebnis nur dort als UNVERIFIED aus, wo der Aufgabenvertrag es erlaubt, mit Statuszeilen und den Alternativen; sie stufen nie hoch. Ausfälle werden getrennt klassifiziert (MODEL_UNAVAILABLE, QUOTA_EXHAUSTED, TRUNCATION, TIMEOUT, MALFORMED_OUTPUT, RETRIEVAL_FAILURE, INSUFFICIENT_EVIDENCE, COGNITIVE_DISAGREEMENT).

### 13.4 Ende-zu-Ende
Eine echte Mission (MangoMe-WorkIdentity → PeachMe-Session → PlumMe → CherryMe RG/2 → AppleMe → Checkpoint) erhält die Beitragskette redigiert im Arbeitszustand (PeachMe-Test, 241 passed). Der unabhängige Leser `runners/ogi_org_events.contribution_chain` (FruitStack-Eval) prüft den Mission Record **allein** und meldet: Beitrag ohne ID/Digest/Receipt/Modellidentität, nicht konsolidiert, UNVERIFIED als gedächtnisfähig, UNVERIFIED-Art als VERIFIED, abgeschlossen ohne unabhängiges verifiziertes Quorum, Rohantwort im geteilten Record. Der echte Mission Record (Fixture `peach_mission_records_v2.json`) liest sich ohne Flag; FSE-Suite 319 passed.

### 13.5 Schlüsselkette (alle neun historischen Schlüsselprobleme)
Ursachen und Auflösung: `org-05` (Tagesangabe „1“ eines Datums und „20.“ Mitglied) — Datumsteile sind keine Zählwerte, Ordinalzahl beantwortet die Mitgliederzahl; `org-07` (zwei Daten) — Klausel „in Kraft“ statt „angenommen“ entscheidet; `law-04` — der **Widerspruch** zwischen früherer Evidenzanalyse (Teilstring `1689` im Zitat) und `NOT_IN_EVIDENCE` war ein Parser-Fehler (Kennung `2024/1689` wurde ausgeschlossen); jetzt „nach dem Schrägstrich“; `hist-09` — das volle Datum steht nur in unverifizierten Modellbeiträgen, das Jahr 1985 ist verifiziert → Rückgabe als `UNVERIFIED_CANDIDATE` mit Herkunft, alle Kandidaten bewahrt; `tech-02` — der Schlüssel steht in **keinem** Beitrag der Kette (kein erfundener Wert).

| Aufgabe | Status (neu) | Wert | stimmt mit Referenz (nur Auswertung) | Kandidaten (Herkunft protokolliert) |
|---|---|---|---|---|
| inq-hist-07 | DETERMINISTIC | 1948-12-10 | True | 1948-12-10 |
| inq-hist-09 | UNVERIFIED_CANDIDATE | 1985-06-14 | True | 1985-06-14, 1990-06-19 |
| inq-hist-10 | DETERMINISTIC | 1989 | True | 1989 |
| inq-law-04 | DETERMINISTIC | 1689 | True | 1689 |
| inq-org-03 | DETERMINISTIC | 2024-03-07 | True | 2024-03-07 |
| inq-org-05 | DETERMINISTIC | 20 | True | 20 |
| inq-org-07 | RANKED | 1948-04-07 | True | 1948-04-07, 1946-07-22 |
| inq-tech-02 | NOT_IN_EVIDENCE | – | None | – |
| inq-tech-04 | DETERMINISTIC | 2023-10-02 | True | 2023-10-02 |

Über alle 18 Aufgaben mit verifizierten Zitaten und Verdikt: 0 falsche Werte (Auswertung gegen Referenz), 0 erfundene. Die Regeln wurden an den neun Fällen entwickelt (Entwicklungsdaten); der Befund ist Regressionsmaterial, keine Leistungsmessung.

### 13.6 Marginaler Erkenntnisgewinn aus den vorhandenen Beobachtungen (FSE-MARGINAL/1)
Drei Sichten, nie vermischt (Reihenfolge = Aktivierungsreihenfolge, vorangehende Menge = alle früheren Aktivierungen; Quelle: Receipts der 50 Aufgaben, `repro/d11_marginal.json`):

| Sicht | Aufgaben messbar | nicht messbar | teilweise beobachtet | gemessen: Gewinn | Nullgewinn | Regression (Endergebnis schlechter als bester Einzelbeitrag) |
|---|---|---|---|---|---|---|
| A: F3-Vorschläge | 17 | 20 | 13 | 0 | 13 | 4 |
| B: Kontrolle, dann F3-Vorschläge | 25 | 2 | 23 | 2 | 8 | 15 |
| C: Verifier-Urteile | 22 | 24 | 4 | 0 | 18 | 4 |

Lesart (strikt getrennt):
1. **Sicht A:** In 17 Aufgaben lieferten ≥ 2 verschiedene Abstammungslinien ein Verdikt; **kein** späterer Beitrag war richtig, wo alle früheren falsch waren (0 gemessene Komplementarität). In 13 dieser Aufgaben waren alle Linien richtig (Deckeneffekt: nichts zu ergänzen); in 4 gemischt. Das ist ein gemessener Nullgewinn **bei geringer Messkraft** (Aufgaben auf Verdiktebene leicht), kein Beleg gegen Komplementarität im Allgemeinen. 58 Lieferungen stammten von einer Linie, die schon beigetragen hatte (Wiederholung, keine zweite Meinung), 80 von 115 Lieferungen brachten strukturell nichts Neues.
2. **Sicht B (querarm):** 2 Aufgaben mit gemessenem Gewinn (law-09, tech-02), 8 Nullgewinn; 15 Regressionen. In 13 dieser Regressionen waren **alle** Linien richtig und trotzdem war das F3-Endergebnis schlechter: das ist **Pipeline-Verlust** (technischer Defekt, §11/§12/§13.5), kein Modellbefund.
3. **Sicht C:** 22 Aufgaben, überwiegend Übereinstimmung der Urteile (18 Nullgewinn bei übereinstimmenden Richtungen), 4 Regressionen = ebenfalls Konsolidierungsverlust.
4. **Unabhängigkeit:** FSE-G2-Paartest auf diesen Daten: alle 45 Linienpaare je Sicht `INSUFFICIENT_SHARED_TASKS` (Schwelle 40 gemeinsame Aufgaben, 60 Aufrufe) → Unabhängigkeit **ungemessen**; weder bestätigt noch widerlegt. Eine Aussage „unabhängige Modelle ergänzen sich nicht“ ist daher aus diesen Daten **nicht** ableitbar.
5. **Versorgung getrennt:** nicht gelieferte Aktivierungen (A: 431 von 546) sind NOT_MEASURABLE_NO_DELIVERY und nie Nullgewinn. Ausfallklassen aller Receipts/Kontrollversuche: {"QUOTA_EXHAUSTED": 170, "CONTROL:QUOTA_EXHAUSTED": 35, "CONTROL:MODEL_UNAVAILABLE": 37, "MALFORMED_OUTPUT": 83, "TIMEOUT": 31, "MODEL_UNAVAILABLE": 106, "OTHER": 2, "CONTROL:MALFORMED_OUTPUT": 4, "CONTROL:OTHER": 13}.
6. Ressourcen (alle Aktivierungen Sicht A): Aufrufe 546, Tokens 507206.

### 13.7 Die 17 historisch blockierten Fälle
Befund: in diesen Fällen wurde im F3-Lauf **kein** Modell gefragt; die Kontrolle lieferte in 15 von 17 Fällen genau **einen** Modellbeitrag, in 2 Fällen keinen. Damit ist weder ein positiver noch ein Nullgewinn mehrerer Modelle gemessen.

| Aufgabe | ausgeführtes Modell (Kontrolle) | Linie | Kontroll-Fehlversuche vor Lieferung | Klasse | Offline messbar | braucht neue Inferenz |
|---|---|---|---|---|---|---|
| inq-hist-02 | – | – | 7 | **NOT_MEASURABLE** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-hist-03 | nvidia/nemotron-3.5-lightning:free | nemotron | 1 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-law-01 | liquid/lfm-2.5-2.6b:free | lfm | 4 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-law-08 | nvidia/nemotron-3-super-120b-a12b:free | nemotron | 0 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-law-10 | gemini-3.1-flash-lite | gemini-flash-lite | 2 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-org-04 | – | – | 7 | **NOT_MEASURABLE** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-org-08 | nvidia/nemotron-3-super-120b-a12b:free | nemotron | 0 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-sci-02 | stealth/glyph-cluster | glyph | 0 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-sci-03 | liquid/lfm-2.5-2.6b:free | lfm | 0 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-sci-04 | nvidia/nemotron-3-super-120b-a12b:free | nemotron | 0 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-sci-06 | poolside/laguna-xs-2.1:free | laguna | 1 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-sci-07 | openai-fast | openai | 4 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-sci-08 | stealth/glyph-cluster | glyph | 0 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-sci-10 | nvidia/nemotron-3-super-120b-a12b:free | nemotron | 0 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-tech-03 | stepfun/step-5-preview-free | step | 2 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-tech-06 | openai-fast | openai | 1 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |
| inq-tech-07 | poolside/laguna-s-2.1:free | laguna | 0 | **PARTIALLY_OBSERVED** | Lieferung, Richtigkeit des einen Beitrags | zweite/dritte Linie, Komplementarität, Konsolidierungswirkung |

Zulässige Alternativen je Aufgabe: UNBEKANNT (kein Fähigkeits-Snapshot zum Dispatch-Zeitpunkt gespeichert; im selben Lauf liefen erfolgreich 11 Linien). Es werden keine kontrafaktischen Antworten erzeugt.

### 13.8 Fallmatrix (alle 41 Aufgaben mit Verlust)
| Aufgabe | vorhandene bzw. fehlende Information | Ursache | Verarbeitungsschritt (Modul) | Korrektur | Offline-Replay | Rest / benötigte Modellbeobachtungen |
|---|---|---|---|---|---|---|
| inq-hist-02 | Kontrolle 0.0; Kontrolle ohne Antwort; keine korrekte Information in beobachteten Beiträgen | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat – UNVERIFIED, Claim unverändert (keine aufgezeichnete Antwort) | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-hist-03 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat REFUTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-hist-04 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | VERIFIER_QUORUM_UNREACHABLE | Verifikation (zweiter unabhängiger Worker nicht verfügbar) — PlumMe (Versorgung); CherryMe (dritter Prüfer) | dritter Prüfer; fehlende Worker explizit klassifiziert | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | Versorgung (Verifier-Worker fehlten) zweiter/dritter unabhängiger Verifier |
| inq-hist-05 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifikation (Quorum, Teilbeleg-Regel, fehlende Verifier-Worker) — CherryMe (`verification`); Versorgung der Verifier-Worker: PlumMe | Bezeichner ≠ Wert; dritter Prüfer; Dissens bleibt erhalten | Replay: NONE -> SUPPORTED (Bezeichner-Regel) | dritter Prüfer bzw. neu verfügbare Verifier-Worker |
| inq-hist-07 | Kontrolle 0.0; Schlüssel in verifizierten Zitaten; korrektes Verdikt in Modellvorschlägen | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Schlüsselstufe (ein Modellaufruf ohne Wiederholung) — CherryMe (`keys`) | deterministische Schlüsselextraktion + Kandidatenkette | Replay: Wert verifiziert (1948-12-10) | nur bei Mehrdeutigkeit: ein Delegationsaufruf |
| inq-hist-08 | Kontrolle 0.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifikation (Quorum, Teilbeleg-Regel, fehlende Verifier-Worker) — CherryMe (`verification`); Versorgung der Verifier-Worker: PlumMe | Bezeichner ≠ Wert; dritter Prüfer; Dissens bleibt erhalten | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | Versorgung + Verifier-Worker fehlten dritter Prüfer bzw. neu verfügbare Verifier-Worker |
| inq-hist-09 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | KEY_EXTRACTION_ERROR | Schlüsselstufe — CherryMe (`keys`) | deterministische Extraktion; Wert aus unverifizierten Beiträgen nur gekennzeichnet | Replay: Wert nur als UNVERIFIED_CANDIDATE mit Herkunft (1985-06-14) | Datum nur als UNVERIFIED (Quelle belegt nur das Jahr) unabhängige Quelle/Modell für den Wert |
| inq-hist-10 | Kontrolle 1.0; Schlüssel in verifizierten Zitaten; korrektes Verdikt in Modellvorschlägen | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Schlüsselstufe (ein Modellaufruf ohne Wiederholung) — CherryMe (`keys`) | deterministische Schlüsselextraktion + Kandidatenkette | Replay: Wert verifiziert (1989) | nur bei Mehrdeutigkeit: ein Delegationsaufruf |
| inq-law-01 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat SUPPORTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-law-03 | Kontrolle 1.0 | NO_ELIGIBLE_MODEL | Modellversorgung (kein zulässiges Modell) — PlumMe | Ausfall als MODEL_UNAVAILABLE klassifiziert, nicht wiederholt | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | Versorgung ausführbares Modell |
| inq-law-04 | Kontrolle 1.0; Schlüssel in verifizierten Zitaten; korrektes Verdikt in Modellvorschlägen | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Schlüsselstufe (ein Modellaufruf ohne Wiederholung) — CherryMe (`keys`) | deterministische Schlüsselextraktion + Kandidatenkette | Replay: Wert verifiziert (1689) | nur bei Mehrdeutigkeit: ein Delegationsaufruf |
| inq-law-05 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen | RETRIEVED_BUT_NOT_ADDRESSED | Auszugsauswahl der Quelle — CherryMe (`host_retrieval`) | einmal alternatives Textfenster derselben Seite | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | erneuter Abruf (Seiteninhalt nicht gespeichert) |
| inq-law-07 | Kontrolle 0.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | CORRECT_PROPOSAL_NOT_RECOGNIZED | Konsolidierung: Vorschlag ohne Verifikation verworfen — CherryMe (`contributions`) | Beitragsbuch SOURCE_BACKED/RETAINED_UNVERIFIED; `present_decision` (nur wo der Vertrag es erlaubt) | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | unabhängige Verifikation des Vorschlags |
| inq-law-08 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat SUPPORTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-law-10 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat REFUTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-org-01 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifikation (Quorum, Teilbeleg-Regel, fehlende Verifier-Worker) — CherryMe (`verification`); Versorgung der Verifier-Worker: PlumMe | Bezeichner ≠ Wert; dritter Prüfer; Dissens bleibt erhalten | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | Verifier-Worker fehlten (Versorgung) dritter Prüfer bzw. neu verfügbare Verifier-Worker |
| inq-org-03 | Kontrolle 0.0; Schlüssel in verifizierten Zitaten; korrektes Verdikt in Modellvorschlägen | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Schlüsselstufe (ein Modellaufruf ohne Wiederholung) — CherryMe (`keys`) | deterministische Schlüsselextraktion + Kandidatenkette | Replay: Wert verifiziert (2024-03-07) | nur bei Mehrdeutigkeit: ein Delegationsaufruf |
| inq-org-04 | Kontrolle 0.0; Kontrolle ohne Antwort; keine korrekte Information in beobachteten Beiträgen | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat – UNVERIFIED, Claim unverändert (keine aufgezeichnete Antwort) | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-org-05 | Kontrolle 1.0; Schlüssel in verifizierten Zitaten; korrektes Verdikt in Modellvorschlägen | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Schlüsselstufe (ein Modellaufruf ohne Wiederholung) — CherryMe (`keys`) | deterministische Schlüsselextraktion + Kandidatenkette | Replay: Wert verifiziert (20) | nur bei Mehrdeutigkeit: ein Delegationsaufruf |
| inq-org-06 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | BUDGET_ABORT | Zeitlimit 1200 s, Lauf abgebrochen — Harness/PlumMe-Zeit; CherryMe-Persistenz | Beitragsbuch nach jeder Frage persistiert | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | Wiederholung unter Zeitlimit |
| inq-org-07 | Kontrolle 1.0; Schlüssel in verifizierten Zitaten; korrektes Verdikt in Modellvorschlägen | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Schlüsselstufe (ein Modellaufruf ohne Wiederholung) — CherryMe (`keys`) | deterministische Schlüsselextraktion + Kandidatenkette | Replay: Wert verifiziert (Klausel-Rang) (1948-04-07) | nur bei Mehrdeutigkeit: ein Delegationsaufruf |
| inq-org-08 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat REFUTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-org-10 | Kontrolle 0.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen | RETRIEVED_BUT_NOT_ADDRESSED | Auszugsauswahl der Quelle — CherryMe (`host_retrieval`) | einmal alternatives Textfenster derselben Seite | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | erneuter Abruf (Seiteninhalt nicht gespeichert) |
| inq-sci-02 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat REFUTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-sci-03 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat SUPPORTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-sci-04 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat SUPPORTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-sci-05 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | CORRECT_PROPOSAL_NOT_RECOGNIZED | Konsolidierung: Vorschlag ohne Verifikation verworfen — CherryMe (`contributions`) | Beitragsbuch SOURCE_BACKED/RETAINED_UNVERIFIED; `present_decision` (nur wo der Vertrag es erlaubt) | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | unabhängige Verifikation des Vorschlags |
| inq-sci-06 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat REFUTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-sci-07 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat SUPPORTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-sci-08 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat REFUTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-sci-09 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifikation (Quorum, Teilbeleg-Regel, fehlende Verifier-Worker) — CherryMe (`verification`); Versorgung der Verifier-Worker: PlumMe | Bezeichner ≠ Wert; dritter Prüfer; Dissens bleibt erhalten | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | dritter Prüfer bzw. neu verfügbare Verifier-Worker |
| inq-sci-10 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat SUPPORTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-tech-01 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifikation (Quorum, Teilbeleg-Regel, fehlende Verifier-Worker) — CherryMe (`verification`); Versorgung der Verifier-Worker: PlumMe | Bezeichner ≠ Wert; dritter Prüfer; Dissens bleibt erhalten | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | dritter Prüfer bzw. neu verfügbare Verifier-Worker |
| inq-tech-02 | Kontrolle 0.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | KEY_EXTRACTION_ERROR | Schlüsselstufe — CherryMe (`keys`) | deterministische Extraktion; Wert aus unverifizierten Beiträgen nur gekennzeichnet | Replay: Wert in keinem Beitrag; kein Schlüssel erfunden | Schlüssel in keinem beobachteten Beitrag: anderes Modell nötig unabhängige Quelle/Modell für den Wert |
| inq-tech-03 | Kontrolle 1.0 | RETRIEVAL_FETCH_FAILED | Host-Retrieval (Abruf) — CherryMe | wie oben (RETRIEVAL_ERROR@FETCH) | Replay: Frage gestellt, Kandidat SUPPORTED UNVERIFIED, Claim unverändert | wie oben |
| inq-tech-04 | Kontrolle 1.0; Schlüssel in verifizierten Zitaten; korrektes Verdikt in Modellvorschlägen | KEY_STAGE_SKIPPED_DESPITE_KEY_IN_VERIFIED_QUOTE | Schlüsselstufe (ein Modellaufruf ohne Wiederholung) — CherryMe (`keys`) | deterministische Schlüsselextraktion + Kandidatenkette | Replay: Wert verifiziert (2023-10-02) | nur bei Mehrdeutigkeit: ein Delegationsaufruf |
| inq-tech-05 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | VERIFICATION_REJECTED_TRUE_EVIDENCE | Verifikation (Quorum, Teilbeleg-Regel, fehlende Verifier-Worker) — CherryMe (`verification`); Versorgung der Verifier-Worker: PlumMe | Bezeichner ≠ Wert; dritter Prüfer; Dissens bleibt erhalten | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | dritter Prüfer bzw. neu verfügbare Verifier-Worker |
| inq-tech-06 | Kontrolle 0.0; keine korrekte Information in beobachteten Beiträgen | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat REFUTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-tech-07 | Kontrolle 1.0 | NO_GROUNDING_RETRIEVAL_EMPTY | Host-Retrieval / Quellenpflicht-Gate vor der Frage — CherryMe (`plumme_bridge`, `host_retrieval`) | Frage wird gestellt; UNVERIFIED-Kandidat mit Antwort, Identität, Ressourcen; Ursache persistiert; kein Wiederholen der Suche je Worker | Replay: Frage gestellt, Kandidat SUPPORTED UNVERIFIED, Claim unverändert | zweite/dritte Abstammungslinie auf derselben Aufgabe (Komplementarität) |
| inq-tech-08 | Kontrolle 1.0; Schlüssel nur in unverifizierten Beiträgen/Auszügen; korrektes Verdikt in Modellvorschlägen | CORRECT_PROPOSAL_NOT_RECOGNIZED | Konsolidierung: Vorschlag ohne Verifikation verworfen — CherryMe (`contributions`) | Beitragsbuch SOURCE_BACKED/RETAINED_UNVERIFIED; `present_decision` (nur wo der Vertrag es erlaubt) | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | unabhängige Verifikation des Vorschlags |
| inq-tech-10 | Kontrolle 1.0 | RETRIEVED_BUT_NOT_ADDRESSED | Auszugsauswahl der Quelle — CherryMe (`host_retrieval`) | einmal alternatives Textfenster derselben Seite | nicht abspielbar (neue Modellantwort/Seiteninhalt nötig) | erneuter Abruf (Seiteninhalt nicht gespeichert) |

### 13.9 Offene wissenschaftliche Fragen (nur mit unabhängigen Modellbeobachtungen beantwortbar)
1. Ergänzen sich unabhängige Linien auf Aufgaben ohne zulässige Primärquelle? (17 Fälle haben höchstens eine Beobachtung.)
2. Welche Linien sind empirisch unabhängig (G2: ≥ 60 Kalibrieraufrufe je Linie, ≥ 40 gemeinsame Aufgaben)?
3. Hilft ein dritter Prüfer bei 1:1-Uneinigkeit (6 Verifikationsfälle und `tech-05` brauchen neue Antworten)?
4. Wie groß ist der Konsolidierungsgewinn (Entscheidungsgewinn über den besten Einzelbeitrag) mit der reparierten Pipeline?
5. Nennt ein weiteres Modell den fehlenden Schlüssel in `tech-02` (RFC 9114)?
Entwurf der Studie: `PREREG_COGINT_2_DRAFT.md` (vorbereitet, nicht eingefroren, nicht gestartet).

### 13.10 Belege
CherryMe a70fa36 (368 Tests), PeachMe 712e07f (241 Tests mit CherryMe 0.4.2), FSE: `fruitstack_eval/marginal.py`, `runners/ogi_org_events.contribution_chain`, Tests, Fixture, `repro/d11_marginal.py`, `repro/d12_sec13.py`, `PREREG_COGINT_2_DRAFT.md`.


---

## 14. Forensik der organisationalen Intelligenz: C-Arm-Fehlerzuordnung und Synthese-Engpass (2026-10-17)

**Methodik und Grenzen.** Alle Zahlen stammen aus Rohbeobachtungen (Receipts, Ergebnisdateien, Journale, Konfigurationen) und dem registrierten Grader `fse-inquiry/1`; Referenzen gehen nur in die Bewertung ein. Regelwerk und Rechenwege: `fruitstack_eval/failure_attribution.py` (Schema FSE-FAILURE-ATTRIBUTION/1, CLI `fse failure-attribution`, 9 Tests; das ältere Modul `attribution.py` = Build-Zeit-Zuordnung bleibt unverändert), Rohdatenleser `repro/d13_attribution.py`, Statistiken `repro/d14_stats.py`, Text `repro/d15_sec14.py`; Ausgaben `repro/d13_attribution.jsonl` (ein Datensatz je Studie/Arm/Aufgabe mit Evidenz und Zuordnung), `repro/d13_attribution.json`, `repro/d14_stats.json`. Code-Stände: FruitStack-Eval `cc/fse-rg2-evidence` (Commit im Abschluss), CherryMe `cc/cognitive-recovery-001` a70fa36 (nur für Klassifikationshilfen `classify_failure`, `split_claim_values`; die analysierten Läufe liefen auf a667256/0.3.4 bzw. älteren Kandidaten). OGI-012 (2/96) wurde **nicht** gelesen; keine neue Inferenz, kein Provider-Aufruf. Entwicklungsaufgaben mit Entwurfsreferenzen: Diagnose, keine konfirmatorische Messung. Fehlendes bleibt UNKNOWN. **Korrektur:** das Signal `key_in_verified_quotes` in `d7_forensics.py` zählte auch ungegründete Worker-Texte; nach der Korrektur ändert sich für 5 Aufgaben nur das Signal (hist-05, hist-09, law-07, sci-09, tech-09), keine Ursachenklasse und keine Zahl aus §11.

### 14.1 Berücksichtigte C-Arme (nicht gepoolt) und Ausschlüsse
| Studie | C-Arm (genaue Definition) | Aufgaben | Synthese | Budgets/Grenzen (bestätigt) |
|---|---|---|---|---|
| D2 | **F3**: PlumMe 0.1.12 `122b81b` AUTO, CherryMe `a667256`/0.3.4: Fragenkette SCIENCE→REUSE→GAP→FALSIFY, Host-Retrieval (Allowlist, ≤ 4 Quellen), EvidenzVerifier-Quorum 2, Statusableitung, **Schlüsselstufe = ein AUTO-Modellaufruf ohne Wiederholung**, Wissensspeicher | 50 | deterministische Statusableitung + ein Syntheseaufruf (KEY_PROMPT) | 4 Fragen, 14 Dispatches (nur am Fragenanfang geprüft), `timeout 1200` je Aufgabenschritt (`dev_f3_shard.sh:10`, Journal org-06: 1200,0 s), Ausgabe 1024 Tokens, 120 s je Aufruf |
| D1c | **F3 (älterer Kandidat)**, PlumMe 0.1.10: 2× `ddgs-text-search`, Proposer `north-mini-code:free`, **Antwort-/Synthese-Worker `nemotron-3.5-lightning:free` (2048 Tokens) dann `north-mini-code:free` (512 Tokens)**; selbstständige Rechen-/Datumsaufgaben | 12 (9 ausgeführt, 3 Credential-erschöpft) | zwei Modellaufrufe | Ausgabegrenzen 2048/512 (aus den Receipts) |
| D1a | ACE_ADVISED_TWO_WORKER: Abstammungen nvidia + cohere, deterministische Regel „erste strukturierte Antwort, wenn keine Uneinigkeit, sonst Enthaltung“ | 3 | Regel, kein Modell | – (alle 3 Endnoten 1,0: keine Fehlschläge) |
Als **Kontrollen mit deterministischer Komposition** (nicht C): D1b F2 (12) und D1c F2 (12), feste Zweimodell-Regel. **Ausgeschlossen:** ROUTE-ARMS-ABC/2 C („hierarchischer Schatten“: adaptiver Einzelmodellzug ohne Synthese), D2b F3-DEV (0 Aufrufe), D5 (nur Mit-Gedächtnis-Arm), OGI-010 (nie ausgeführt), OGI-011 (keine konfirmatorische Ausführung), **OGI-012 (geschützt)**, D11 (keine realen Missionsrecords). Brother-Mode-Aufzeichnungen sind nicht als unabhängig beobachtbare Datensätze vorhanden (kein Mensch-integrierter Vergleichsarm; nichts erfunden).

### 14.2 Deliverable 1 — Fehlerzuordnung (primär = früheste nachweisbare, hinreichende Ursache)
**D2/F3, 50 Aufgaben, 41 nicht vollständig richtig:**
| Klasse | primär | beitragend | Aufgaben (primär) |
|---|---|---|---|
| GATE_BLOCK | 28 | 12 | davon 17 vor jeder Modellfrage (Retrieval-/Quellenpflicht-Gate): hist-02, hist-03, law-01, law-08, law-10, org-04, org-08, sci-02, sci-03, sci-04, sci-06, sci-07, sci-08, sci-10, tech-03, tech-06, tech-07; übrige: hist-05, hist-09, law-05, law-07, org-10, sci-05, sci-09, tech-02, tech-05, tech-08, tech-10 |
| INFRASTRUCTURE | 12 | 11 | hist-04, hist-07, hist-08, hist-10, law-03, law-04, org-01, org-03, org-05, org-07, tech-01, tech-04 (7× Syntheseaufruf ohne Antwort: hist-07, hist-10, law-04, org-03, org-05, org-07, tech-04; 4× fehlende Verifier-Worker: hist-04, hist-08, org-01, tech-01; 1× kein zulässiges Modell: law-03) |
| BUDGET | 1 | 5 | org-06 (Zeitlimit 1200 s verifiziert; beitragend bei inq-hist-05, inq-law-07, inq-sci-09, inq-tech-08, inq-tech-10: Fragenbudget 4 erschöpft) |
| INTEGRATION_LOSS | 0 | 7 | keine Aufgabe, in der die Synthese Information, die sie erhielt, falsch verarbeitet hätte; als beitragend bei den 7 Synthese-Aufruf-Ausfällen |
| NO_CORRECT_CONTRIBUTION | 0 | – | keine (wo Beiträge fehlten, wird sie nicht vergeben) |
| UNKNOWN | 0 | – | – |
Terminalbedingungen der fehlgeschlagenen D2-Aufgaben: entschieden oder INCOMPLETE ohne Budgetgrenze 35, Fragenbudget erschöpft 5, Zeitlimit 1. Wiederherstellbarkeit ohne neue Inferenz: {"NO_NO_ARM_INTERNAL_CONTRIBUTION": 18, "YES_ONLY_AS_UNVERIFIED": 12, "YES_DETERMINISTIC": 8, "NO_REQUIRES_NEW_INFERENCE": 3} (YES_DETERMINISTIC = Schlüssel in verifizierten Eingaben bzw. Regelfehler Bezeichner/Wert; YES_ONLY_AS_UNVERIFIED = korrekte Beiträge vorhanden, aber nur als unverifiziert darstellbar; NO_NO_ARM_INTERNAL_CONTRIBUTION = der Arm hatte keinen eigenen Modellbeitrag, nur der Kontrollarm hatte einen).
**D1c/F3-alt, 12 Aufgaben, 7 nicht vollständig richtig:** INFRASTRUCTURE 7 (X01, X05, X09: Antwort-Worker lieferte **leeren sichtbaren Text** an der Tokengrenze, obwohl der Proposer das Verdikt enthielt; X07: Proposer und Antwort-Worker leer an der Grenze; X10–X12: beide Worker Credential-erschöpft), GATE_BLOCK 0, BUDGET 0, INTEGRATION_LOSS 0, NO_CORRECT_CONTRIBUTION 0, UNKNOWN 0.
Aufgabenweise Zuordnung (alle Fehlschläge):
| Studie | Aufgabe | Endnote | primäre Ursache | beitragende Ursachen | Terminalbedingung | Verlustort (falls Information vorhanden) | wiederherstellbar ohne neue Inferenz |
|---|---|---|---|---|---|---|---|
| D1c | X01 | 0.0 | INFRASTRUCTURE | INTEGRATION_LOSS | COMPLETED | SYNTHESIS_CALL_FAILED | YES_ONLY_AS_UNVERIFIED |
| D1c | X05 | 0.0 | INFRASTRUCTURE | INTEGRATION_LOSS | COMPLETED | SYNTHESIS_CALL_FAILED | YES_ONLY_AS_UNVERIFIED |
| D1c | X07 | 0.0 | INFRASTRUCTURE | – | COMPLETED | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D1c | X09 | 0.0 | INFRASTRUCTURE | INTEGRATION_LOSS | COMPLETED | SYNTHESIS_CALL_FAILED | YES_ONLY_AS_UNVERIFIED |
| D1c | X10 | 0.0 | INFRASTRUCTURE | – | COMPLETED | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D1c | X11 | 0.0 | INFRASTRUCTURE | – | COMPLETED | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D1c | X12 | 0.0 | INFRASTRUCTURE | – | COMPLETED | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-hist-02 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-hist-03 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-hist-04 | 0.0 | INFRASTRUCTURE | GATE_BLOCK | INCOMPLETE | CONTRIBUTION_ADMISSION | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-hist-05 | 0.0 | GATE_BLOCK | INFRASTRUCTURE, BUDGET | QUESTION_BUDGET | VERIFICATION_OR_QUORUM | YES_DETERMINISTIC |
| D2 | inq-hist-07 | 0.5 | INFRASTRUCTURE | GATE_BLOCK, INTEGRATION_LOSS | SUPPORTED | SYNTHESIS_CALL_FAILED | YES_DETERMINISTIC |
| D2 | inq-hist-08 | 0.0 | INFRASTRUCTURE | GATE_BLOCK | INCOMPLETE | VERIFICATION_OR_QUORUM | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-hist-09 | 0.5 | GATE_BLOCK | INFRASTRUCTURE | REFUTED | CONTRIBUTION_ADMISSION | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-hist-10 | 0.5 | INFRASTRUCTURE | GATE_BLOCK, INTEGRATION_LOSS | SUPPORTED | SYNTHESIS_CALL_FAILED | YES_DETERMINISTIC |
| D2 | inq-law-01 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-law-03 | 0.0 | INFRASTRUCTURE | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-law-04 | 0.5 | INFRASTRUCTURE | GATE_BLOCK, INTEGRATION_LOSS | SUPPORTED | SYNTHESIS_CALL_FAILED | YES_DETERMINISTIC |
| D2 | inq-law-05 | 0.0 | GATE_BLOCK | INFRASTRUCTURE | INCOMPLETE | – | NO_REQUIRES_NEW_INFERENCE |
| D2 | inq-law-07 | 0.0 | GATE_BLOCK | INFRASTRUCTURE, BUDGET | QUESTION_BUDGET | CONTRIBUTION_ADMISSION | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-law-08 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-law-10 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-org-01 | 0.0 | INFRASTRUCTURE | GATE_BLOCK | INCOMPLETE | VERIFICATION_OR_QUORUM | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-org-03 | 0.5 | INFRASTRUCTURE | GATE_BLOCK, INTEGRATION_LOSS | REFUTED | SYNTHESIS_CALL_FAILED | YES_DETERMINISTIC |
| D2 | inq-org-04 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-org-05 | 0.5 | INFRASTRUCTURE | GATE_BLOCK, INTEGRATION_LOSS | SUPPORTED | SYNTHESIS_CALL_FAILED | YES_DETERMINISTIC |
| D2 | inq-org-06 | 0.0 | BUDGET | INFRASTRUCTURE, GATE_BLOCK | TIMEOUT | EXECUTION_TERMINATED_BEFORE_FINAL | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-org-07 | 0.5 | INFRASTRUCTURE | GATE_BLOCK, INTEGRATION_LOSS | REFUTED | SYNTHESIS_CALL_FAILED | YES_DETERMINISTIC |
| D2 | inq-org-08 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-org-10 | 0.0 | GATE_BLOCK | INFRASTRUCTURE | INCOMPLETE | – | NO_REQUIRES_NEW_INFERENCE |
| D2 | inq-sci-02 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-sci-03 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-sci-04 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-sci-05 | 0.0 | GATE_BLOCK | – | INCOMPLETE | CONTRIBUTION_ADMISSION | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-sci-06 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-sci-07 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-sci-08 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-sci-09 | 0.0 | GATE_BLOCK | INFRASTRUCTURE, BUDGET | QUESTION_BUDGET | VERIFICATION_OR_QUORUM | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-sci-10 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-tech-01 | 0.0 | INFRASTRUCTURE | GATE_BLOCK | INCOMPLETE | VERIFICATION_OR_QUORUM | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-tech-02 | 0.5 | GATE_BLOCK | INFRASTRUCTURE | REFUTED | CONTRIBUTION_ADMISSION | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-tech-03 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-tech-04 | 0.5 | INFRASTRUCTURE | GATE_BLOCK, INTEGRATION_LOSS | SUPPORTED | SYNTHESIS_CALL_FAILED | YES_DETERMINISTIC |
| D2 | inq-tech-05 | 0.0 | GATE_BLOCK | INFRASTRUCTURE | INCOMPLETE | VERIFICATION_OR_QUORUM | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-tech-06 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-tech-07 | 0.0 | GATE_BLOCK | – | INCOMPLETE | – | NO_NO_ARM_INTERNAL_CONTRIBUTION |
| D2 | inq-tech-08 | 0.0 | GATE_BLOCK | INFRASTRUCTURE, BUDGET | QUESTION_BUDGET | CONTRIBUTION_ADMISSION | YES_ONLY_AS_UNVERIFIED |
| D2 | inq-tech-10 | 0.0 | GATE_BLOCK | INFRASTRUCTURE, BUDGET | QUESTION_BUDGET | – | NO_REQUIRES_NEW_INFERENCE |

### 14.3 Deliverable 2 — Integrationsverlust
Definition: Aufgaben, in denen die eigenen Beiträge des Arms zusammen Verdikt **und** Schlüssel enthielten, das Endergebnis aber nicht voll richtig war, geteilt durch Aufgaben mit ≥ 1 gelieferten Beitrag (die Aufgabe ist „auswertbar“).
- **D2/F3:** **20 von 32 = 62.5%** (Wilson-95 %-KI 45.2%–77.1%); streng (ein *einzelner* Beitrag enthielt beides): 20/32. **Vor der Synthese** 13 (Beitragsaufnahme 6: hist-04, hist-09, law-07, sci-05, tech-02, tech-08; Verifikation/Quorum 6: hist-05, hist-08, org-01, sci-09, tech-01, tech-05; Lauf beendet vor Endergebnis 1: org-06). **An der Synthese** 7, alle als *Syntheseaufruf lieferte nichts* (hist-07, hist-10, law-04, org-03, org-05, org-07, tech-04); **Synthesizer-Schlussfolgerung falsch: 0.**
- **D1c/F3-alt:** 3 von 8 (37.5%, Wilson-95 % 13.7%–69.4%), alle 3 an der Synthese mit unbekannten Eingaben (Syntheseeingaben nicht aufgezeichnet; Aufruffehler ist sicher, was der Worker erhalten hätte nicht).
- Integrationsdelta (Endnote minus beste Einzelbeitragsnote, D2): besser 0, gleich 10, schlechter 22 von 32 auswertbaren; D1c: besser 2, gleich 3, schlechter 3 von 8.
- **Post-hoc-Oberschranke (kein erreichbarer Wert):** D2 Kontrolle ∪ F3 = 41/50 voll richtig (Kontrolle 37, F3 9; Kontrolle richtig, F3 nicht: 32; F3 richtig, Kontrolle nicht: 4; in 8 der 50 Aufgaben lieferte die Kontrolle keine Antwort). Innerhalb von F3: 29/50 Aufgaben, in denen ein einzelner Beitrag beides enthielt oder das Ergebnis schon richtig war. Es wurden keine kontrafaktischen Modellantworten erzeugt.
- Deterministische Komposition (Kontrollen, keine C-Arme): auswertbar D1a 3, D1b 11, D1c 9; Endergebnis = beste Einzelnote in 22 von 23, schlechter in 1 (D1b X10: Halbtreffer eines Modells durch Enthaltung verloren), nie besser. In 13 Aufgaben war genau **ein** Modell voll richtig (Komplementarität auf Modellebene), die Regel bewahrte es in 13.

### 14.4 Deliverable 3 — Synthesizer-Bewertung
1. **Wer synthetisierte?** D2: ein AUTO-Aufruf (`run_worker`, Rolle REASONING, BEST, keine Ausschlüsse) ohne festes oder kompetenzqualifiziertes Synthesemodell; antwortende Modelle (11 Aufrufe): dots-3-note-preview, nemotron-3-ultra/-3-super, gemini-3.1-flash-lite, north-mini-code u. a. (`repro/d14_stats.json` → `D2_synthesis_calls.replies`). D1c: nemotron-3.5-lightning, dann north-mini-code. Eine Kompetenzqualifikation für die Rolle Synthese lag in beiden Fällen nicht vor (UNKNOWN, nicht belegt).
2. **Eingaben:** D2: nur **verifizierte Zitate** (≤ 5000 Zeichen); keine unverifizierten Beiträge, kein Dissens, keine Angabe zur Stärke einzelner Beiträge. Folge: der korrekte, nur unverifizierte Schlüssel (hist-09) war für den Synthesizer nicht verfügbar — das ist ein Verlust *vor* der Synthese, kein Syntheseversagen. D1c: Eingaben nicht aufgezeichnet.
3. **Aufruferfolg:** D2 18 Syntheseaufrufe, 11 mit Text, **7 ohne Antwort** (Ausfallklassen in der Aufrufnachlaufzeit: {"QUOTA_EXHAUSTED": 7, "MODEL_UNAVAILABLE": 2}); es gibt keinen Fallback und keine Wiederholung. Wenn der Synthesizer antwortete und die Information in seinen Eingaben stand, war er **9 von 9** richtig; zwei weitere Antworten betrafen Fälle, in denen der Schlüssel nicht in den Eingaben stand (hist-09: Datum eines anderen Ereignisses aus den verifizierten Zitaten; tech-02: korrekt „UNKNOWN“); die 9 voll richtigen Antworten stammen von dots, nemotron-ultra/-super, gemini-flash-lite, north-mini und glyph. D1c: der **erste** Syntheseworker lieferte in **9 von 9** Aufgaben keinen sichtbaren Text (2048 Ausgabetokens erreicht; PlumMe-Katalog: `reasoning: true`), der zweite in 5 von 9 (512 Tokens), in 3 leer an der Grenze.
4. **Token-/Budgetgrenzen:** D2 Ausgabe 1024 (keine der 11 Antworten war leer oder erkennbar abgeschnitten: Längen 15–182 Zeichen); D1c: Grenzen wurden erreicht (leer bei 2048/512). → modellspezifische Ausfallart (Verbrauch der Ausgabegrenze durch verdecktes Schlussfolgern), nicht Kompetenz.
5. **Anweisungen:** D2 `KEY_PROMPT` verlangt „nur verifizierte Zitate, sonst UNKNOWN, eine Zeile `KEY:`“ — streng, aber im beobachteten Material nicht ursächlich (0 Fälle, in denen der Schlüssel in den Eingaben stand und trotz Antwort UNKNOWN geliefert wurde).
6. **Stark/schwach unterscheiden, Dissens wahren:** nicht möglich — die Eingaben tragen weder Stärke noch Dissens; die Statusableitung (Quorum, Teilbelegregel) wird vor dem Syntheseaufruf deterministisch entschieden. Der Synthesizer trifft in D2 keine Auflösungsentscheidung; die Konsolidierungsentscheidung liegt in den Gates (14.2: 28 Gate-Blockaden, dazu 4 Quorum-Ausfälle durch fehlende Worker).
7. **Einzelner schwacher Ausfallpunkt?** Ja, im Sinn der **Zustellung**: ein einzelner un-wiederholter Aufruf ohne Fallback verursacht in D2 7 von 18 Aufrufen (39 %) den Verlust des Schlüsselpunkts bei bereits vorhandenem Verdikt; in D1c fiel der erste Syntheseworker deterministisch aus. **Nicht** im Sinn der Schlussfolgerungsfähigkeit: dafür gibt es keinen Beleg.
8. **Hypothese „kleineres Modell synthetisiert schlechter“:** mit den vorhandenen Daten nicht gestützt und nicht prüfbar — alle 9 vollständigen Antworten waren korrekt über sehr verschiedene Modelle (inkl. gemini-flash-lite, north-mini); die beobachteten Ausfälle sind Zustellfehler (Quote/Verfügbarkeit, leerer Text an der Tokengrenze). Ein stärkerer Synthesizer wäre bei diesem Befund ohne Zustellsicherheit wirkungslos; und ein Gewinn durch ein stärkeres Modell wäre nicht automatisch Organisationsintelligenz (daher Solo-Kontrolle A1 in der Registrierung).

### 14.5 Modellketten-Zuverlässigkeit und Budgets
Stufen (D2): **obligatorisch seriell** Retrieval → Proposer → Verifier-Quorum (≥ 2 Linien je Quelle) → Statusableitung → **Syntheseaufruf (kein Failover)**; **redundant/parallel** mehrere Quellen und mehrere Verifier-Paare; **Failover** AUTO-Neuwahl bis 8 Zyklen je Aufruf (Proposer und Verifier), nicht für die Synthese; **optional** weitere Fragen der Kette bis zum Budget 4. Beobachtete Übergänge (D2, 50 Aufgaben): nutzbare Quelle 33 → Modellbeitrag 32 → Verifier-Urteil 30 → mindestens eine Quelle promotet 18 → Anspruch entschieden 18 → Syntheseaufruf 18 → Text 11 → voll richtig 9. Die Formel 1-(1-p)^n wird nicht angewandt: die Ausfälle sind korreliert (dieselben Quoten-/Credential-Erschöpfungen treffen mehrere Stufen derselben Aufgabe), die Stufen sind teils redundant. Ein ausgefallener *optionaler* Worker (ein Verifier unter mehreren Quellen) ließ die Aufgabe nicht scheitern, solange eine andere Quelle promotet wurde (18 Aufgaben); der **einzige obligatorische Einzelaufruf ohne Failover** (Synthese) verlor dagegen das Ergebnis in 7 Fällen.
Wirksame Grenzen: D2 Fragenbudget 4 (in 5 fehlgeschlagenen Aufgaben INCOMPLETE bei erschöpftem Budget), Dispatchbudget 14 (nur zu Fragenbeginn geprüft: Obergrenzen wurden überschritten), Median 229 s, Maximum 1051 s, **22 Aufgaben über 300 s**. **Die „300 s“-Grenze war in D1/D2/ROUTE-ARMS-ABC/2 nicht wirksam** (ABC2: 86 400 s gesamt, 400 Versuche, 240 000 Tokens, 1024 Ausgabetokens); sie steht nur im OGI-011-Korrekturbericht (nie abgeschlossen). Das Zeitlimit beendete org-06 (1200 s; vorher 13 richtige Verdiktbeiträge, kein Endergebnis, nichts „verworfen“ → BUDGET primär); das Fragenbudget beendete fünf weitere Aufgaben im Zustand INCOMPLETE (hist-05, law-07, sci-09, tech-08, tech-10) — dort liegen die Hauptursachen davor (Gates, Verifikation) und das Budget ist nur beitragend. Eine ausstehende Synthese wurde in keinem Fall durch ein Budget verhindert.

### 14.6 Deliverable 4 — Lücke der Organisationsarchitektur (RG/2 gegenüber dem Brother-Mode-Beispiel)
Der menschliche Integrator leistet fünf Funktionen. Zustand in CherryMe RG/2 (Code `cc/cognitive-recovery-001` a70fa36) und PeachMe 0.8.4:
| Funktion des Menschen | RG/2 heute | Beleg |
|---|---|---|
| Nützliche Kritik auswählen | **teilweise, strukturell**: Rollen/Verantwortungen (FALSIFY, REVIEWER), Kompetenzgewichte, korrelierte Modelle zählen als eine Stimme; keine inhaltliche Relevanzbeurteilung | `responsibility.py` `consolidate`, `independent_lean` |
| Konkurrierende Vorschläge bewerten | **teilweise**: Quorum-Verifikation gegen Quellauszug, Dissens/Alternativen erhalten (`unresolved_alternatives`); kein Modell, das Vorschläge inhaltlich gegeneinander abwägt | `verification.py`, `contributions.consolidate` |
| Irrelevante Einwände verwerfen | **nicht unterstützt** (Dissens wird bewahrt, nicht nach Relevanz gefiltert) | – |
| Entscheiden, wann genug getan ist | **unterstützt, regelbasiert**: `ResolutionAwareOrchestrator`, Eskalation/Deeskalation nach Grenznutzen, Zero-Call | `orchestrator.py`, Responsibility-Skill |
| Konkurrierende Empfehlungen zu einer Entscheidung integrieren | **deterministisch**: Statusableitung + `present_decision`; **kein** autonomer Modell-Synthesizer in CherryMe. Der einzige Modell-Synthesizer (PeachMe `_synthesize`) formuliert die Antwort *nach* der Entscheidung | `mission.py:139` |
Fehlende autonome Fähigkeiten: inhaltliche Gegenüberstellung widersprüchlicher Beiträge durch einen qualifizierten Synthesizer, Relevanzfilter für Einwände, Zustellsicherheit der Synthese (Fallback), Syntheseeingaben mit Stärke/Dissens, Kompetenzqualifikation der Rolle Synthese. Ein automatisierter Synthesizer ist **nicht** als erfolgreicher Ersatz der menschlichen Integration belegt; ein Mensch-integrierter Vergleichsarm liegt nicht vor.

### 14.7 Deliverable 5 — Registrierte Studie
`PREREG_ORGSYNTH_3_DRAFT.md` (Entwurf, nicht eingefroren, nicht gestartet): Arme A0 (S0 allein), A1 (stärkstes zulässiges Modell allein), B (unorganisiertes Multi-Modell), C0/C1 (RG/2 mit S0/S1 bei identischen Arbeitern), D (Ablation Synthese/Verifikation); Hypothesen H1 (C1 > A1 und B), H2 (Differenz-der-Differenzen trennt Synthesizerstärke von Modellstärke), H3 (C1 > D); Grounding-Richtlinie ohne Vor-Retrieval, aber UNVERIFIED-Kennzeichnung; Fähigkeitsprofile statt Sonderüberschreibungen (Sichtbarkeitsquote bei der Ausgabegrenze); Abstention zählt nicht als richtig; ITT; Annahmekriterien positiv/negativ/inkonklusiv; Stichprobe 170 / 280 / ≈ 550 zur Eigentümerentscheidung.

### 14.8 Deliverable 6 — Eigentümerentscheidung
- **Ursache der beobachteten Fehlschläge:** D2: von 41 Fehlschlägen 28 Gate-Blockaden (17 davon vor jeder Modellfrage), 12 Infrastruktur (7 Syntheseaufruf ohne Antwort, 4 fehlende Verifier-Worker, 1 kein zulässiges Modell), 1 Zeitlimit; **0** falsche Synthese, **0** „kein Modell hatte die Lösung“, 0 unklar. D1c: 7/7 Infrastruktur (4× leerer Syntheseausgang an der Tokengrenze, 3× Credential-Erschöpfung). Mangelnde Modellkompetenz oder fehlendes komplementäres Wissen ist in diesen Daten **nicht** als Ursache nachweisbar.
- **Anteil Synthese/Integration:** *Zustellung der Synthese* verursachte 7 von 41 D2-Fehlschlägen (17 %) und 4 von 7 D1c-Fehlschlägen; die Integrationsverlustrate (Information vorhanden, Ergebnis nicht voll richtig) beträgt in D2 20/32 (62%), davon 13 **vor** der Synthese (Aufnahme/Verifikation) und 7 bei der Synthese (nur Aufruf-Ausfall). Fehler im **Schließen** der Synthese: 0 beobachtet.
- **Nicht messbar:** Komplementarität/Unabhängigkeit der Modelle (G2 unzureichend, 18 D2-Aufgaben ohne eigenen Modellbeitrag), Wirkung eines stärkeren Synthesizers, ein Mensch-integrierter Vergleich, Leistung der RG/2-Organisation (keine realen Missionsdaten), Kompetenz der Synthesemodelle.
- **Durch Evidenz gerechtfertigte begrenzte Korrektur:** (1) Zustellsicherheit der Synthese mit deterministischem Fallback aus verifizierten Zitaten und einmaliger Delegation bei Mehrdeutigkeit (bereits in CherryMe 0.4.2 implementiert, offline an 7/7 Fällen reproduziert, Schlüssel nur aus verifizierter Evidenz); (2) Aufhebung der Quellenpflicht als Vorbedingung der Frage (implementiert); (3) Fähigkeitsprofil-basierte Ausgabegrenze/Eignung für Modelle mit verdecktem Schlussfolgern (Beobachtung D1c) — als Voraussetzung der Registrierung, keine neue Architektur. Kein weiterer Reparaturzyklus ist durch die Daten gerechtfertigt.
- **Erforderliche Forschungsfreigabe als Nächstes:** (a) Freigabe zum Einfrieren von PREREG-ORGSYNTH-3 mit Entscheidung über N (170/280/≈ 550), Marge und Ressourcenobergrenzen; (b) Freigabe einer **Kalibrierungsinferenz** (G2: ≥ 60 Aufrufe je Linie, sichtbare Antwortquote bei der registrierten Ausgabegrenze) zur Festlegung von S0, S1 und der zulässigen Linien; (c) Freigabe der Harness-Anpassung auf einem Entwicklungsbranch (Syntheseaufruf mit Fallback, UNVERIFIED-Kennzeichnung) und von Merge/Installation von CherryMe 0.4.2 für den Lauf. Ohne (b) ist H2 nicht testbar.


---

## 15. OGI-Validierungslücke: ausführbarer Sechs-Arm-Pfad (2026-10-17)

**Ergebnis.** Der Pfad Aufgabe → Agenten → Zusammenarbeit → Konsolidierung → Antwort → unabhängiger Grader ist für die sechs Arme **A0, A1, B, C0, C1, D technisch ausführbar** (scripted Provider, aufgezeichnete Daten, echter PlumMe-Dienst mit gemeinsamem ParentBudget, echte CherryMe-0.4.2-Engine, echter `fse ogi`-Grader). Eine **reale Messung ist nicht möglich**, weil vier Voraussetzungen offen sind (15.5). Es gibt keine Leistungsaussage; Offline-Tests sind technische Abnahme.

**15.1 Pfad und Konfiguration.** Wiederverwendet wird der bestehende OGI-011-Harness (`f2f3_epoch2.py`, `ogi011_arms.py`, Korpus `corpus/ogi011_corpus.py`, Grader `fse ogi grade`, Zeilenbildner/Fehlertaxonomie `ogi011_analyze.row_for`, `ogi_sequential.paired_wald`). Neu sind nur Anschlüsse: `ORG_ARMS`-Registrierung und gepinnte Synthesizer (`cfg["synthesizers"]`), Verifikationsablation D, Synthese-Fallback, Sechs-Arm-Analyse `runners/orgsynth_analyze.py`, Ressourcen-/Paketbauer `runners/orgsynth_plan.py`. Arme: A0 = S0 allein, A1 = S1 allein, B = zwei Entwürfe + festes Review durch S0, C0/C1 = RG/2 mit gepinntem Synthesizer S0/S1 bei identischen Arbeitern, D = RG/2 ohne quotengebundene Verifikation (S1 kombiniert die unverifizierten Beiträge). Reproduktion:
```
PP=/root/SUPPLY-001/wt/CherryMe-recovery:/root/SUPPLY-001/wt/PlumMe-rel/src:/root/SUPPLY-001/wt/AppleMe-rel/src
PYTHONPATH=$PP python runners/orgsynth_plan.py plan --units 171      # Ressourcen/Power, kein Providerruf
python runners/orgsynth_plan.py build PKG SPEC.json                 # SPEC aus ORGSYNTH3_SPEC.template.json; offene Entscheidungen => NOT_EXECUTABLE.json + RUN.sh (exit 41)
bash PKG/RUN.sh                                                      # verify-revisions, init, step-Schleife, grade, orgsynth_analyze -> PKG/ORGSYNTH3_RESULT.json
```
Stand der Revisionen: CherryMe 0.4.2 `cc/cognitive-recovery-001` 7cae4cd, PlumMe 0.1.15 `cc/plumme-0.1.15-release` 12c57fd, AppleMe 0.1.4 (`AppleMe-rel`), PeachMe 0.8.4 712e07f, FruitStack-Eval `cc/fse-rg2-evidence` 47eae94. Die Revisionen werden beim Bauen als `expected_revisions` festgeschrieben und von `verify-revisions` fail-closed geprüft. Die Installation im Host-Venv (CherryMe-006/PlumMe 0.1.14, OGI-012) bleibt unverändert; der neue Stack läuft per `PYTHONPATH`.

**15.2 Behobene Integrationsdefekte** (alle durch Tests belegt): (1) Harness kannte nur Arm „C“ (Dispatch, Admission, Memory-Regel, Zeilenbildner) → `ORG_ARMS`; (2) der Synthesizer wurde per AUTO gewählt, nicht gepinnt → explizite Zuweisung S0/S1, auch in der Unit-Admission; (3) Synthese-Fallback aus CherryMe 0.4.2 war im Harness nicht angeschlossen → angeschlossen (nur aus verifizierten Zitaten, nie erfunden; Schlüsseltyp „Version“ in CherryMe ergänzt; ältere CherryMe-Stände bleiben unverändert); (4) Wissensspeicher wurde zwischen Organisationsarmen derselben Sequenz geteilt (C1 hätte von C0 profitiert) → je Arm getrennt; (5) Arm ohne Verifier brach beim Protokollieren ab (`verifier_log` None); (6) Analyse kannte keine sechs Arme/Hypothesen → `orgsynth_analyze`; (7) `COUNTS["T3"]` des Korpusgenerators leckte global in andere Tests → wiederhergestellt; (8) Test-Hygiene: `test_G1_window_state…` ließ `PLUMME_RATE_LIMITS_FILE=/x/…` in der Umgebung zurück, was unter PlumMe 0.1.15 vier spätere Tests brach → behoben; (9) der Modul-Namenskonflikt (`attribution`) ist behoben (Commit 6432706).

**15.3 Tests (vollständig).** FruitStack-Eval komplette Suite: Standard-Venv **337 passed, 1 skipped** (die Sechs-Arm-Wiring-Datei verlangt CherryMe ≥ 0.4.2), 0.4.2-Stack **342 passed, 0 failed**; die bisherigen 3 Fehlschläge in `test_git_tools.py` (Modulumbenennung) sind behoben. CherryMe 369 passed, PeachMe 241 passed (jeweils mit PlumMe 0.1.15/AppleMe 0.1.4). Neue Tests: `test_orgsynth_arms.py` (Sechs-Arm-Verdrahtung: gepinnte Synthesizer, ein Budget, Pool-Beschränkung, Synthese-Fallback, Schlüssel nie erfunden, getrennte Speicher), `test_orgsynth_rehearsal.py` (init → Ergebnisse → `fse ogi grade` → H1/H2/H3, Negativ-/Null-/Teil-Läufe), `test_orgsynth_plan.py` (Paketbauer verweigert bei offenen Entscheidungen; vollständige Spec → vom Harness akzeptierte Konfiguration, Schedule-Hash).

**15.4 Ressourcen (offline, Planwerte aus den OGI-011-Konstanten; kein Providerruf).** Obergrenzen je Arm-Lauf wie OGI-011: 30 Dispatches, 26 000 Tokens, 300 s; Fehlversuche sind durch das ParentBudget (zählen mit), 3 AUTO-Neuwahlen je Frage und 2 Routenversuche je gepinnter Lease begrenzt. Erwartete Fehlversuche nehmen den historischen Anteil fehlgeschlagener Receipts (392/854 = 46 %, D2) als Planannahme.
| Einheiten | Aufgaben | Arm-Läufe | erwartete Tokens | erwartete Dispatches (Erfolgspfad / inkl. Fehlversuche) | harte Dispatch-Grenze | harte Token-Grenze | harte Laufzeit der Läufe | Laufzeit-Untergrenze bei 4 gemessenen rpm | Power H1 / H3 / H2 (δ=0,15 / 0,10 / 0,10) |
|---|---|---|---|---|---|---|---|---|---|
| 171 | 207 | 1242 | 6.6 M | 6,800 / 12,569 | 37,260 | 32 M | 104 h | ≥ 52.4 h | 0.913 / 0.571 / 0.4 |
| 282 | 318 | 1908 | 10.7 M | 11,012 / 20,356 | 57,240 | 50 M | 159 h | ≥ 84.8 h | 0.987 / 0.78 / 0.556 |
| 552 | 588 | 3528 | 20.5 M | 21,259 / 39,296 | 105,840 | 92 M | 294 h | ≥ 163.7 h | 1.0 / 0.965 / 0.803 |
Pro Arm (171 Einheiten): A0/A1 je 207 Dispatches/209 k Tokens, B 621/820 k, C0 und C1 je 2505/2.27 M, D 756/822 k (Dateien `reports/.../orgsynth3/RESOURCE_PLAN_*.json`). Power: einseitig α = 0,05, gepaart, diskordant 0,35, Designeffekt 1,3 (Annahmen, keine Messwerte). **Stichprobenbegründung:** N = 171 gibt der primären Hypothese H1 die registrierte Power (0,91 je Vergleich bei δ = 0,15; die gemeinsame Power der Schnitt-Vereinigung ist niedriger), H3 (0,57) und H2 (0,40) sind dort **nicht** ausreichend gepowert; N = 282 reicht für H3 (0,78) bei δ = 0,10; erst N = 552 gibt H2 Power 0,80. Eine kleinere Studie würde H1 unterpowern; die Wahl liegt beim Eigentümer. Quotenreserve: **UNBEKANNT** (nur Minutenlimits belegt: Gateway 2 rpm für qwen3.5-397b und gpt-oss-120b, OpenRouter-Konto 50 Anfragen/Tag; für nemotron-3-ultra keine belegte Kappe, 0/5 beantwortet am 16.10.).

**15.5 Tatsächlich fehlende Voraussetzungen für eine valide Studie.** (1) **Keine G2-qualifizierte, unabhängige Linienmenge:** in allen Entwicklungsläufen `TOO_FEW_QUALIFIED_GROUPS` / `NO_INDEPENDENT_SET_OF_REQUIRED_SIZE` (31 Gruppen, 13 mit ≥ 1 Ausführung, 0 qualifiziert; Schwellen 60 Aufrufe/Linie, Ausführungsquote ≥ 0,8, ≥ 40 gemeinsame Aufgaben). Kompetenz aller Pool-Modelle UNKNOWN (0 QUALIFIED). (2) **S0/S1 und Pool nicht festgelegt:** OGI-011-Smoke: gpt-oss-120b stop-Rate 1,0, qwen3.5-397b 0,85 (< 0,95), nemotron-3-ultra-550b 0/2 ausführbar. (3) **Durchsatz:** ≥ 52 h reine Ratenlimit-Zeit bei N = 171 mit den zwei gemessenen Routen. (4) **Offene Eigentümerentscheidungen** (15.6). Kleinster Schritt zu (1)/(2): genau eine **Kalibrierungsinferenz** (Entwurf unten) und eine Pool-/Quotenentscheidung; ohne sie ist H2 nicht testbar und die Mehrmodellaussagen bleiben „Unabhängigkeit ungemessen“.

**15.6 Freigabeentscheidungen, die noch ausstehen.**
1. **Stichprobe:** 171, 282 oder 552 Einheiten (Korpus: T3 = 123 / 234 / 504; erzeugt wird erst nach Freigabe mit neuem Seed).
2. **Kalibrierung:** Freigabe einer G2-Kalibrierung (`runners/g2_supply_calibration.py`): je zu prüfender Linie 60 Aufrufe auf denselben 60 Kalibrieraufgaben (zugleich Messung der sichtbaren Antwortquote bei Ausgabegrenze 700). Beispielumfang für 6 Kandidatenlinien: 360 Aufrufe, begrenzt auf ≈ 665 Versuche (historischer Fehlschlaganteil), ≈ 0,9 M Tokens, ≈ 0,5–3 h je nach Parallelität bei 2 rpm je Route; Lineage-Kandidaten und Quoten vorab ohne Providerruf aus `FREE_COVERAGE`/`GATEWAY_QUOTA_MODEL` festzulegen. Ergebnis legt S0, S1, Pool, B-Entwürfe und `g2_independent_lineages` fest.
3. **Grenzen:** `max_total_tokens`, `max_dispatches`, `max_wall_seconds` (Spec-Felder; Planwerte in 15.4; empfohlen mindestens die erwartete Menge inkl. Fehlversuche, höchstens die harte Grenze).
4. **Registrierung/Start:** Einfrieren von `PREREG_ORGSYNTH_3_DRAFT.md` und `authorization.execution_go`; Merge/Installation von CherryMe 0.4.2 bzw. die Nutzung per `PYTHONPATH` wie oben.
5. **Zwei Festlegungen, die ich nicht still getroffen habe:** (a) **Aufgabenquelle** = bestehender OGI-011-Korpusgenerator mit neuem Seed (ausführbare Orakel statt Webabruf; die im Entwurf genannten Strata „ohne zulässige Primärquelle“ kommen dort nicht vor, die Grounding-Politik wird über die Materialien erfüllt); (b) **Arm D**: der Entwurf nennt eine feste Regel ohne Modell, die für Artefaktaufgaben (SQL/Python) und Versions-/Textschlüssel nicht allgemein existiert. Implementiert ist D als Verifikationsablation (S1 kombiniert die unverifizierten Beiträge); H3 wird auf Schlüsselaufgaben (86% der Einheiten bei N = 171) ausgewertet. Bitte bestätigen oder die Regel vorgeben.
