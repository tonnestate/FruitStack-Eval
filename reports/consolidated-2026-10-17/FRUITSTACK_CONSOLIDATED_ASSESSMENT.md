# FRUITSTACK — Konsolidiertes Gesamtdossier (2026-10-17)

Autor: Claude Code · Auftrag: P0 FRUITSTACK GLOBAL CONSOLIDATION & SCIENTIFIC EVALUATION · Stand der Daten: 2026-10-17
Reproduktion: `bash /root/fruits/research/FRUITSTACK-CONSOLIDATION-005/run_all.sh` (offline, kein Provider-Aufruf). Eingabe-Hashes: `INPUT_HASHES.sha256`. Ergebnis-JSONs: `repro/*.json`.
Methode: Es wurde **keine** zweite Bewertungsengine gebaut. Alle Noten stammen aus FruitStack-Evals registriertem Grader `fse inquiry grade` (`fse-inquiry/1`, Referenzen nie im System), alle Schätzer aus `fruitstack_eval.pilot.analyze` (FSE `6e2ef14`). Die Skripte zählen Receipts und rufen diese Funktionen auf.
Nicht verändert: OGI-012 (geparkt), alle eingefrorenen Worktrees, alle Rohdaten, alle `main`/`sync/local-truth`-Stände. Keine neuen Provider-Aufrufe.

---

## 0. Kurzurteil

> **Ergänzung 2026-10-17 (§11, FRUITSTACK-SCIENCE-100):** Das 9/50-Defizit entsteht überwiegend vor/nach den Modellen (17 Aufgaben: Quellenpflicht-Gate stellt gar keine Modellfrage; 9: Schlüsselstufe; 6: Verifikationsregeln), nicht durch schwache Modelle; beobachtete Auswahl-Obergrenze 41/50.

> **Ergänzung 2026-10-17 (§12, FRUITSTACK-COGNITIVE-RECOVERY/1):** CherryMe 0.4.1 (`cc/cognitive-recovery-001`, 5a6adad, nicht gemergt/installiert) behebt die vier nachgewiesenen Verlustmechanismen; Offline-Replay fallweise in §12.1 (17/17 Vorab-Blockaden, 4/9 Schlüsselverluste, 1/6 Verifikationsfehler beseitigt, Rest teils nur mit neuen Modellantworten prüfbar). Keine Erfolgsquote behauptet.

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
