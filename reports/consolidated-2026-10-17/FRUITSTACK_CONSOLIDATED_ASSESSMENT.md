# FRUITSTACK — Konsolidiertes Gesamtdossier (2026-10-17)

Autor: Claude Code · Auftrag: P0 FRUITSTACK GLOBAL CONSOLIDATION & SCIENTIFIC EVALUATION · Stand der Daten: 2026-10-17
Reproduktion: `bash /root/fruits/research/FRUITSTACK-CONSOLIDATION-005/run_all.sh` (offline, kein Provider-Aufruf). Eingabe-Hashes: `INPUT_HASHES.sha256`. Ergebnis-JSONs: `repro/*.json`.
Methode: Es wurde **keine** zweite Bewertungsengine gebaut. Alle Noten stammen aus FruitStack-Evals registriertem Grader `fse inquiry grade` (`fse-inquiry/1`, Referenzen nie im System), alle Schätzer aus `fruitstack_eval.pilot.analyze` (FSE `6e2ef14`). Die Skripte zählen Receipts und rufen diese Funktionen auf.
Nicht verändert: OGI-012 (geparkt), alle eingefrorenen Worktrees, alle Rohdaten, alle `main`/`sync/local-truth`-Stände. Keine neuen Provider-Aufrufe.

---

## 0. Kurzurteil

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
