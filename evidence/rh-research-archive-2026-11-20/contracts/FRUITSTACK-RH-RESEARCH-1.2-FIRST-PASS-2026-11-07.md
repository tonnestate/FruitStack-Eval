---
title: FruitStack RH Research 1.2 – erster Evidenz- und Forschungsstand
date: 2026-11-07
status: FIRST_PASS; kein RH-Beweis, kein Gegenbeweis, keine End-to-End-Abnahme
source_spec: FRUITSTACK-RH-RESEARCH/1.2 (Nutzereingabe vom 2026-11-07)
---

# Zweck und Prüfgrenze

Dies ist die erste, quellengestützte Arbeitsaufnahme zu `FRUITSTACK-RH-RESEARCH/1.2`. Geprüft wurden ausgewählte lokale Dateien und Primärquellen, keine vollständigen Repositories, keine Live-Dienste, keine 80 Tests. Jede nachfolgende Statusangabe gilt nur für den genannten Prüfgegenstand. Die Riemannsche Vermutung (RH) ist laut [Clay Mathematics Institute](https://www.claymath.org/millennium/Riemann-Hypothesis/) weiterhin offen.

Das mathematische Hauptziel bleibt `∀ ρ, ζ(ρ)=0 ∧ 0<Re(ρ)<1 → Re(ρ)=1/2`; das Gegenbeweisziel verlangt eine **zertifizierte** Nullstelle im Streifen mit `Re(ρ)≠1/2`. Diese Textform ist noch kein semantisch eingefrorenes Lean-Ziel. Weder ein endlicher Nullstellentest noch ein bewiesener Hilfssatz noch eine SHAP-Attribution schließt das Hauptziel.

# 1. Stichprobe zum tatsächlichen Softwarestand

`EXISTS_VERIFIED` bedeutet hier: die genannte Funktion wurde im lokalen Quelltext gefunden. Es bedeutet weder lauffähige Integration noch Produktabnahme. Die Commit-IDs sind die am 2026-11-07 lokal gelesenen Stände.

| Komponente | Lokaler Stand und konkrete Evidenz | Status für RH-Auftrag |
|---|---|---|
| CherryMe | `/root/fruits/sync/CherryMe` `a667256`; `cherryme/models.py` definiert `ClaimStatus`, `DeltaStatus`, Evidenz und Forschungsfragen; `cherryme/inquiry.py` enthält `FALSIFY` und kennzeichnet `PROVOKE` ausdrücklich als Provokation ohne Evidenz. | Generische Inquiry-Bausteine `EXISTS_VERIFIED`; mathematische Beweissuche und RH-Integration `UNKNOWN` nach dieser Stichprobe. |
| PlumMe | `/root/fruits/sync/PlumMe` `122b81b`; `src/plumme/selection.py` implementiert deterministische, `epsilon_floor`- und `pool_spread`-Auswahl auf einer bereits hart zugelassenen Angebotsmenge und speichert Auswahlwahrscheinlichkeiten. | Kontrollierte Routing-Exploration `EXISTS_VERIFIED`; perturbierte Modellparameter und mathematische SHAP-Engine `NOT_EVIDENCED`. |
| AppleMe | `/root/fruits/sync/AppleMe` `8dfc33f`; `src/appleme/engine.py` erzeugt `NO_PROGRESS` nur nach expliziten Meldungen ohne Evidenzgewinn und `LOOP_RISK` bei Wiederholung ohne Gewinn. | Generische Trajektorienbeobachtung `EXISTS_VERIFIED`; mathematisches Fortschrittsurteil `NOT_EVIDENCED`. |
| FruitStack-Eval | `/root/fruits/integration/ogi013-fse` `fd2003f`; `fruitstack_eval/ablation.py` implementiert vollfaktorielle Shapley-Ablation für höchstens sechs **Organisationskomponenten**. | Organisatorische Ablation `EXISTS_VERIFIED`; TreeSHAP für mathematische Features und unabhängiger RH-Gesamtlauf `NOT_EVIDENCED`. |
| CogC | `/root/CogC/src/cogc/fidelity.py` und `tests/test_fidelity.py` vorhanden; keine Funktions- oder Laufzeitprüfung in dieser Aufnahme. | `PARTIAL` (Dateiexistenz, keine RH-Handoff-Abnahme). |
| BananaMe, MangoMe | Diese Aufnahme enthält keine fachliche Quellcode- oder Laufzeitabnahme dieser Systeme. MangoMe wurde nur als verwalteter Arbeitsrahmen für diesen Auftrag verwendet. | `UNKNOWN` für die hier beanspruchten FruitStack-Transferfähigkeiten. |
| DuckDB, Lean, SHAP | Python-Paket `duckdb` lokal importierbar; `shap` und `lean_interact` im Standard-Python nicht gefunden. `lean`, `lake`, `duckdb`, `elan` nicht auf `PATH`. | Kein geprüfter RH-Research-State, Lean-Adapter, TreeSHAP-Experiment oder Lean-Kalibrierungsbeweis. Abwesenheit auf `PATH` beweist keine globale Nichtinstallation. |

Die QA-2D-V2-Closure-Datei `/root/fruits/integration/ogi013-collab-proof/evidence/ogi013-qa2d-v2-closure/QA2D_V2_CLOSURE_REPORT.md` meldet `CLOSED_INFRASTRUCTURE_INFEASIBLE`; die 400-Fragen-Konfirmationsstudie wurde dort nicht abgeschlossen. Ihre 53 explorativen Fragen tragen keine allgemeine Überlegenheitsbehauptung. Dieser Bericht verändert keinen der untersuchten Produktstände.

# 2. Forschungsgraph v0: getrennte Beweis- und Forschungskanten

Jede Zeile ist ein Forschungsbrief mit Ziel, vorhandenem Beleg und expliziter Lücke. `LINK_HYPOTHESIS` ist keine logische Implikation. Ein späteres Inferenzobjekt braucht sämtliche Prämissen, die exakte Schlussregel und einen unabhängigen Prüfnachweis.

| Pfad / ID | Gesicherter Ausgangspunkt oder Kandidat | Offene, prüfbare Beweispflicht | Stand der RH-Verbindung |
|---|---|---|---|
| P / F-01-FK | Für Kurven über endlichen Körpern beschreibt [Milne](https://www.jmilne.org/math/xnotes/pRH.html) Weils RH-Resultat und Delignes spätere Gewichtsresultate. | Exakte Voraussetzungen, Frobenius-/Kohomologie-/Positivitätsrollen im Originaltext isolieren; eine passende Struktur für die klassische `ζ_Q` **definieren** und den Transfersatz separat beweisen. Ein bloßes Analogon reicht nicht. | `LINK_HYPOTHESIS`; keine klassische RH-Folgerung. |
| P / F-02-SPEC | Im [Autoren-PDF, Version arXiv:2511.22755v1](https://alainconnes.org/wp-content/uploads/zeta-spectral-triples-1.pdf) ist Theorem 1.1 zur Selbstadjungiertheit und Determinanten-/Spektralbeziehung **bedingt** durch einen einfachen kleinsten Eigenwert und einen geraden zugehörigen Eigenvektor. Abschnitt 8 nennt ausdrücklich zwei fehlende Schritte für den angestrebten RH-Beweis. | (1) Einfachheit des kleinsten Eigenwerts der eingeschränkten Weil-Quadratform und Geradheit seines Eigenvektors beweisen; (2) die Approximation dieses Eigenvektors durch `k_λ` so stark beweisen, dass die Nullstellen der Fourier-Transformierten zu **allen** nichttrivialen Nullstellen von `ζ(1/2+is)` konvergieren. Danach den genauen globalen RH-Schluss unabhängig prüfen; numerische Indizien aus Abschnitt 6 genügen nicht. | `LINK_HYPOTHESIS`; beide von den Autoren bezeichneten Schlüsselschritte offen. |
| P / F-03-LAMBDA | [Rodgers–Tao](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/de-bruijnnewman-constant-is-nonnegative/D4B85BA067E2D5A71D87E4FFB0D21E46) beweisen `Λ≥0` und nennen `RH ↔ Λ≤0`. | `Λ≤0` beweisen, mit exakter Definition der Konstante und einem formal geprüften Äquivalenzpfad, falls formale RH-Verifikation beansprucht wird. | Literaturgestützte Äquivalenz; formale FruitStack-Verbindung `NOT_VERIFIED`. |
| P / F-03-EQUIV | Die publizierte [FormalConjectures-Datei](https://google-deepmind.github.io/formal-conjectures/src/FormalConjectures/Paper/RiemannHypothesisEquivalents/) enthält Robin-, Lagarias-, Li-, Beurling–Nyman- und Weil-Positivitäts-Statements; die genannten Äquivalenztheoreme enden sichtbar mit `sorry`. Einige Hilfsdefinitionen/Hilfssätze sind separat ausformuliert. | Repo-Commit, Mathlib-Commit und Imports pinnen; pro Kriterium Definition, tatsächliche Axiome, Lean-Beweisstatus und semantische RH-Äquivalenz prüfen. Die Datei beweist ihre `sorry`-Äquivalenzen nicht. | `FORMAL_STATEMENT`, nicht `LINK_PROVED` aus dieser Quelle. |
| P / F-03-WEIL | Die FormalConjectures-Datei formuliert eine additive, reellwertige Weil-Positivitätsbedingung mit Testfunktionsbedingungen. | Geltungsbereich und Testfunktionsraum fachlich prüfen; Äquivalenz zum intendierten RH-Ziel und die Positivitätsaussage **jeweils** beweisen. | `LINK_FORMALIZED` in ungesichertem externem Statement; kein akzeptierter Beweis in der geprüften Ansicht. |
| R / F-05-ZERO | Ein Gegenbeispiel wäre eine nichttriviale `ζ`-Nullstelle in einem isolierten Gebiet `B ⊂ {0<Re(s)<1, Re(s)≠1/2}`. | Existenz einer Nullstelle in `B` durch zertifizierte Nullstellenzählung/Argumentprinzip/Rouché oder gleichwertigen Satz beweisen; Fehlergrenzen und analytische Fortsetzung auditieren. `0∈ζ(B)` als Werteinschluss genügt nicht. | Kein Kandidat und kein Zertifikat aus dieser Arbeit. |
| F-04-ML | CherryMe/PlumMe/FSE bieten einzelne generische Donoren; keine mathematische SHAP-Entdeckung wurde hier ausgeführt. | Exakte, unabhängige formal prüfbare Aufgaben und Modellmerkmale festlegen; Interventionen, Kontrollarme, Checker, Neuheits- und Zielrelevanzprüfung vor Versuch einfrieren. | ML-/SHAP-Ausgabe bleibt Forschungsrelation, niemals Beweiskante. |

**Kleine gesicherte Folgerung aus der Literatur:** Aus `Λ≥0` und `RH ↔ Λ≤0` folgt rein logisch `RH ↔ Λ=0`. In Richtung `RH→Λ=0` liefert RH `Λ≤0`, zusammen mit `Λ≥0` Gleichheit. In Richtung `Λ=0→RH` folgt `Λ≤0`, dann RH. Das ist keine neue mathematische Entdeckung, keine eigene Lean-Prüfung und kein Beweis von `Λ=0`.

## Explizite erste Hyperkanten

| Inferenz | Prämissenmenge | Schluss | Status |
|---|---|---|---|
| `I-LAMBDA` | `Λ≥0` **und** `RH↔Λ≤0` **und** `Λ≤0` | `RH` | Erste zwei Prämissen literaturgestützt; dritte offen; Gesamtbeweis offen. |
| `I-SPECTRAL` | Rigorose Konvergenz **und** exakte Identifikation aller nichttrivialen `ζ`-Nullstellen mit geeignetem reellem Spektrum **und** kontrollierter Grenzübergang | `RH` | Arbeitsentwurf; sogar die genaue hinreichende Schlussregel bedarf fachlicher Prüfung. |
| `I-COUNTERZERO` | Zertifizierte Nullstelle in `B` **und** `B` vollständig im kritischen Streifen **und** `B∩{Re(s)=1/2}=∅` | `¬RH` | Mathematisch naheliegende Schlussregel; sämtliche tatsächlichen Zertifikate offen. |

Der Beweisgraph enthält in dieser Aufnahme **keine** selbst erzeugte `KERNEL_ACCEPTED`-RH-Kante. Literaturtheoreme bleiben als Quellenwissen erhalten; ihre FruitStack-Formalisierung ist separat offen.

# 3. F-04 / FruitStack-Transfer: Vorregistrierungsentwurf, noch kein Versuch

**Zu falsifizierende Kernhypothese:** Bei gleichem Gesamtbudget erzeugen kontrolliert veränderte Priorisierungs-/Featuregewichte mehr neue, unabhängig geprüfte mathematische Aussagen als unveränderte Suche. Der SHAP-Zusatznutzen wird gegen eine `SHUFFLED`-Negativkontrolle getrennt getestet. Cloud-API-Policygewichte sind von unzugänglichen Modellparametern zu unterscheiden.

| Feld | Vorläufige Festlegung |
|---|---|
| Arme | deterministische `BASE`; trainiertes `RF/GBDT`; reproduzierbares `NOISE`; Qualitäts-Diversität `DIVERSITY`; Perturbation plus `SHAP-HYP`; permutierte Attribution `SHUFFLED`. |
| Primärer Endpunkt | Neue, unabhängig formal akzeptierte **nichttriviale** Aussagen pro Gesamtressource. Rekonstruktionen aus Mathlib/Literatur zählen getrennt. |
| Zusätzliche Prüfungen | Falschvorschläge, Neuheit, offene RH-Verbindungen, Diversität nach Beweisstruktur, Kosten, Replays, SHAP-Rang-/Interaktionsstabilität über Seeds und Background Sets. |
| Kontrollierte Voraussetzungen | Gepinnte Aufgabenfamilien, Train-/Test-Trennung, gleiche Taktik- und Verifikationsbudgets, gleiche Checker-Version, blindes mathematisches Review. |
| Offene Parameter vor Konfirmation | Aufgabenbestand, Zahl der Seeds, Stichprobenplanung, Budgethöhe, Nullhypothese/Entscheidungsregel, Toolchain- und Datenhashes. |

**Status `NOT_RUN`:** Weder Daten, SHAP-Erklärungen noch überprüfte Entdeckungen wurden in dieser Aufnahme erzeugt. Dieser Entwurf ist ausdrücklich **keine eingefrorene Vorregistrierung** und darf nicht nachträglich als bestätigter Versuch bezeichnet werden.

# 4. Test- und Review-Status

- T-001 bis T-080: `NOT_RUN` als Produkt-/End-to-End-Tests. Die obige Quellprüfung ist kein Ersatz für Testausführung. T-039 (Repo-Bestandsabgleich) wurde nur als Stichprobe bearbeitet, Ergebnis `PARTIAL`.
- Kein Lean-Proof-Term und kein Nullstellenzertifikat wurde erzeugt. Insbesondere T-005, T-038, T-041 und T-050 bleiben `NOT_RUN`.
- Die vier Ebenen Kernel, semantische Zielgleichheit, nachgewiesene RH-Relevanz und externe wissenschaftliche Einordnung sind für diesen Stand sämtlich **nicht** als Gesamtverfahren abgenommen.
- Ein unabhängiger mathematischer Reviewer und eine zweite numerische Implementierung wurden nicht beauftragt; bis dahin keine RH-Beweis- oder Gegenbeweisbehauptung.

# 5. Nächste ausführbare Arbeit in Abhängigkeitsreihenfolge

1. FormalConjectures- und Mathlib-Commit pinnen; exaktes RH-Ziel inklusive Zeta-Definition, Voraussetzungen und Axiomenliste semantisch zweitprüfen. Ergebnis: Zielhash plus Review-Dossier, keine Erfolgsmeldung.
2. Lean-Toolchain in einem isolierten Forschungszweig nach Repo-Governance verfügbar machen und eine **abstrakte** Zwei-Prämissen-Hyperkante als kleinen echten Proof-Term mit `#print axioms` prüfen. Ergebnis: reproduzierbarer T-005-Receipt.
3. Für F-01 Milnes Darstellung und für F-02 die einzelnen Sätze, Beweise und Voraussetzungen des verfügbaren Connes-Autoren-PDFs satzgenau prüfen; je einen minimalen fehlenden Transfersatz samt Gegenfrage und Quellenstelle formulieren.
4. Eine bekannte analytische **Testfunktion**, nicht `ζ`, mit zertifizierter Nullstellenzählung prüfen und manipulierten Scheintreffer ablehnen. Ergebnis: T-041/T-050-Receipts.
5. Erst nach Aufgaben-, Daten- und Budget-Freeze den F-04-Piloten ausführen; alle Arme und negativen Resultate an FruitStack-Eval exportieren.

**Reale Grenzen dieses Erststands:** Kein Lean-Binary auf `PATH`, kein geprüfter RH-Research-State in DuckDB, kein unabhängiger mathematischer Semantik-Audit, kein F-04-Datensatz oder experimenteller Run. Im verfügbaren Connes-Autoren-PDF wurden Theorem 1.1 und Abschnitt 8, aber nicht sämtliche technischen Beweise und Voraussetzungen geprüft. Die Quellen-Webansicht von FormalConjectures wurde noch nicht auf einen Git-Commit eingefroren.

# Fortsetzung 2026-11-07 – Luna-Quellinventar und ausführbare Basis

Ein unabhängiges read-only Luna-Inventar prüfte aktuelle lokale Git-Stände, relevante Dateien und Status; es änderte keine Produktdateien und führte keine Produkt-Tests aus.

| Repository | Commit | Befund zur Wiederverwendung | Belegpfad |
|---|---|---|---|
| CherryMe | `a667256` | Inquiry, Claim-/Evidenzmodelle und Falsifikationsfragen vorhanden; kein RH-Beweisadapter belegt. | `/root/fruits/sync/CherryMe/cherryme/models.py`, `cherryme/inquiry.py` |
| PlumMe | `122b81b` | Bereits zugelassene Angebotsauswahl unterstützt deterministische, `epsilon_floor`- und `pool_spread`-Policies samt Propensity-Daten; kein Parameterzugriff/SHAP. Working tree mit nicht akzeptierten, ungetrackten Bäumen. | `/root/fruits/sync/PlumMe/src/plumme/selection.py` |
| AppleMe | `8dfc33f` | Trajektorienbeobachtung mit `NO_PROGRESS`/`LOOP_RISK`; kein Mathematik-Fortschrittsprüfer. Working tree mit ungetrackten Bäumen. | `/root/fruits/sync/AppleMe/src/appleme/engine.py` |
| FruitStack-Eval | `fd2003f` | Vollfaktorielle Shapley-Ablation (bis sechs Organisationskomponenten), kein TreeSHAP für mathematische Merkmale. | `/root/fruits/integration/ogi013-fse/fruitstack_eval/ablation.py` |
| CogC | `0934376` | Kontext-Fidelity-Check für Handoffs, keine RH-Abnahme. Ungetrackte Nebenartefakte im Working Tree. | `/root/CogC/src/cogc/fidelity.py` |
| MangoMe (read-only) | `835d8be`, detached, sauber | Generische Work-/Evidence-/Verification-Steuerung; kein mathematischer Beweisprüfer. | `/root/fruits/integration/ogi013-mangome-pinned/src/mangome/work_control.py` |
| BananaMe | nicht gefunden in `/root/fruits` | Status `UNKNOWN`; keine Aussage über andere Orte. | keiner |

Live-Runtimeprobe: Python 3.10.12; DuckDB Python-Paket 1.5.5 verfügbar. `lean`, `lake`, `elan` und DuckDB-CLI fehlen auf `PATH`; geprüfte Lean-/Mathlib-Caches fehlen. `shap`, `lean_interact`, `scipy`, `sympy`, `torch`, `sklearn`, `xgboost` und `lightgbm` waren in diesem Python nicht importierbar. Keine Pakete wurden installiert.

Neue isolierte Basis: `/root/fruits/research/fruitstack-rh-research-v1.2/`. `fruitstack_rh.py` erstellt einen DuckDB-Graphen mit sieben Startbehauptungen/offenen Pflichten, vier Quellenverweisen, getrenntem Inferenz-/Prämissenmodell und intern prüfbarer Hash-Kette im Ereignisjournal. Sechs `WORKS_TOWARD`-Forschungshinweise werden separat von logischen Inferenzen geführt; sie begründen keine Implikation. Quellen stehen bis zu Commit-/Versionspin als unvollständig attestiert. Direkte `LINK_PROVED`- und Kernelstatus-Promotion ist gesperrt. Die Datenbank enthält derzeit keine formale RH-Verifikation und keine logische Inferenzkante. Das ist eine ausführbare Datenbasis, keine Proof Engine.

Ausgeführt: `python3 -m py_compile fruitstack_rh.py`, `python3 fruitstack_rh.py self-check` → `SELF_CHECK_PASS`; danach `seed` zweimal auf denselben persistenten Stand und Integritätsassertion. Der Selbstcheck umfasst außerdem Ablehnung von unbekannten Inferenzstatus. Ergebnis: `claim_count=7`, `inference_count=0`, sechs Forschungshinweise, `verified_rh_claims=[]`, `event_count=22`, `journal_valid=true`; zweites Seed ändert den Stand nicht. Kein Lean-Proof, keine SHAP-Analyse, kein F-04-Lauf und keine T-001–T-080-Produktabnahme ausgeführt.

# 6. Luna-Mathematikrecherche und Ausführungsfortsetzung (2026-11-07)

Ein unabhängiger Rechercheagent sichtete Primär-/Projektquellen für F-01 bis F-04. Das ist Literaturrecherche, keine unabhängige fachliche Abnahme.

- **F-01:** Milnes Funktionenkörperübersicht stützt die Weil-Struktur über Kurven endlicher Körper. Connes–Consani–Marcolli (2007) bieten zusätzlich eine Weil-Formel-/Spurformel-Perspektive, bei der Positivität die zentrale Brücke ist. Für klassische `ζ_Q` fehlt weiterhin ein präziser, bewiesener Transfer. Quellen: [Milne, *The Riemann Hypothesis over Finite Fields*](https://arxiv.org/abs/1509.00797); [Connes–Consani–Marcolli (2007)](https://arxiv.org/abs/math/0703392).
- **F-02:** Für [*Zeta Spectral Triples*, arXiv:2511.22755v1](https://alainconnes.org/wp-content/uploads/zeta-spectral-triples-1.pdf) nennt Abschnitt 8 als offene Hindernisse Einfachheit des kleinsten Eigenwerts, Geradheit des Eigenvektors und eine für die benötigte Nullstellenkonvergenz ausreichende Approximation durch `k_λ`. Die Literaturprüfung umfasste nicht alle technischen Beweise. Numerische Übereinstimmungen bleiben empirisch.
- **F-03:** [Mathlib Riemann-Zeta-Quelle](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/NumberTheory/LSeries/RiemannZeta.lean) und [FormalConjectures-Äquivalenzen](https://google-deepmind.github.io/formal-conjectures/src/FormalConjectures/Paper/RiemannHypothesisEquivalents/) sind noch nicht auf Commits gepinnt. Die sichtbaren Äquivalenz-Statements mit `sorry` sind keine Beweise. Ein nächster valider Schritt ist Commit-Pinning plus transitive Axiomenprüfung in einer tatsächlich installierten Lean-Umgebung.
- **F-04:** Vorgeschlagene kleine Piloten sind (a) kontrollierte Wiederentdeckung einer Robin-/Lagarias-Formulierung unter formalem Checker und Leakage-Kontrolle und (b) eingefrorene Prognose auf zurückgehaltenen endlichen Spektral-/Nullstellendaten mit einfacher Baseline und permutierter Negativkontrolle. Beide bleiben `NOT_RUN`; keine SHAP-Daten und keine Vorregistrierung wurden erzeugt.
- **Teilresultate 2026:** Der Rechercheagent fand OpenAI-Preprints zur Nullstellenfreiheit für `Re(s)>7/8` und `>11/12`; beide Aussagen sind schwächer als RH und wurden hier nicht unabhängig begutachtet. [7/8-Preprint](https://github.com/openai/math/tree/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026); [11/12-Preprint](https://github.com/openai/math/tree/main/preprints/The-Quasi-Riemann-Hypothesis-October-5-2026). Der [Clay-Status](https://www.claymath.org/millennium/Riemann-Hypothesis/) führt RH als ungelöst.

**Korrigierte Reichweite:** Keine dieser Quellenbefunde ist eine neue bewiesene RH-Lemma oder eine Lean-Verifikation. Die laufende Umgebung hat kein `lean`/`lake`/`elan` auf `PATH`; daher ist keine seriöse T-005-Kalibrierung oder formale RH-Karte mit verifizierten Commits möglich. Das Forschungsschema bleibt explorativ und sein Ereignisjournal ist nur lokal hash-konsistent prüfbar, nicht manipulationssicher gegen einen Angreifer mit Datenbank-Schreibzugriff.

# 7. Fortsetzung: lokale Invarianten und Toolchain-Blocker

# 8. F-02 Primärquellenpräzisierung und Forschungsgraph-Fix (2026-11-07)

Ein unabhängiger Luna-Quellenreview sichtete die Primärfassung [Connes–Consani–Moscovici, *Zeta Spectral Triples*, arXiv:2511.22755v1](https://arxiv.org/pdf/2511.22755v1): Theorem 1.1 (PDF S. 2–3) ist an Einfachheit des kleinsten Eigenwerts der restringierten Weil-Form und Geradheit des Eigenvektors gebunden. Abschnitt 8 (PDF S. 32) nennt als fehlende Schritte (a) den Nachweis dieser Eigenpaar-Eigenschaften und (b) eine hinreichend starke Approximation dieses Eigenvektors durch `k_λ`, um die erforderliche Konvergenz der Nullstellen zu begründen. Davon zu unterscheiden ist Lemma 7.3 (PDF S. 30–32), das die Konvergenz der Fourier-/Mellin-Transformierten von `k_λ` gegen Riemanns `Xi` gleichmäßig auf abgeschlossenen Teilstreifen behandelt; es beweist nicht die fehlende Approximation des Eigenvektors. Die Autoren nennen numerische und strukturelle Indizien als Indizien, nicht als Beweise. Dieser Review ist eine gezielte Quellenlektüre, keine vollständige technische Begutachtung des Manuskripts.

Korrektur zur Forschungsstruktur: Der Autoren-Text nennt **zwei** fehlende Schritte. Der gesonderte Prüfschritt, ob deren bewiesener Abschluss tatsächlich die vollständige RH impliziert, ist eine FruitStack-Verifikationspflicht und wird nicht als dritter von den Autoren offengelassener Satz ausgegeben.

Im lokalen Forschungsgraph wurden drei explizite, weiterhin offene Claims für Eigenpaar, Eigenvektor-Approximation und unabhängige RH-Schlussprüfung ergänzt; sie sind quellenverknüpft, aber erzeugen keine Inferenzkante. Die CCM-Quellenkennung wurde auf den versionsspezifischen arXiv-Identifier `2511.22755v1` geändert. Quellenereignisse enthalten jetzt auch den gespeicherten SHA-256-Wert (derzeit `NULL`); der Report stuft abweichende Digests als `SOURCE_UNVERIFIED` ein. Ein nicht vorhandener Digest ist keine Inhaltsauthentisierung. Die Hash-Kette bleibt ohne unabhängigen Anker nicht manipulationssicher gegen einen Datenbank-Schreiber.

**Verifikation dieses Änderungsschnitts:** `python3 -m py_compile fruitstack_rh.py` und `python3 fruitstack_rh.py self-check` bestanden; `python3 -m pytest -q tests/test_research_graph.py` → `69 passed`; vollständige Projekttests `python3 -m pytest -q tests` → `86 passed`. Neue Regressionen decken die drei quellengebundenen F-02-Pflichten ohne logische Kante und Digest-Manipulation ab. Keine Live-/bestehende DuckDB wurde durch diesen Änderungsschnitt aktualisiert. F-02-Claims bleiben `OPEN`; keine RH-Folgerung ist formal geprüft.

Am 2026-11-07 wurde `/root/fruits/research/fruitstack-rh-research-v1.2/tests/test_research_graph.py` ergänzt. `python3 -m pytest -q tests` im Projektverzeichnis ergab zunächst `6 passed`; zusätzlich ergab der CLI-`self-check` `SELF_CHECK_PASS`. Der Testumfang ist eng: Seed-Idempotenz, getrennte Forschungslinks, explizite Mehrfachprämissen, verweigerte unbestätigte Promotionen und Erkennung veränderter Journal-Payloads. Der Stand blieb `7` Aussagen, `0` Inferenzkanten, `22` Journalereignisse, keine verifizierten RH-Behauptungen; Journal lokal konsistent.

Ein unabhängiger Luna-Toolchain-Scan bestätigte read-only: kein Lean/Lake-Projekt oder Toolchain im Forschungsordner, kein Container-Runtime, `elan` fehlt. APT bietet zwar Metadaten für elan, aber die Netzwerkauflösung zu GitHub und geprüften Paketquellen scheiterte. Daher wurde nichts installiert; eine Lean-Kalibrierung ist derzeit nicht ausführbar. Nach wiederhergestelltem Netzwerk ist ein lokal isoliertes, gepinntes Lake-Projekt möglich, aber zunächst nur eine Logik-Kalibrierung – kein RH-Semantiknachweis.

Die neuen Tests und der Datenbank-Selbstcheck sind ausschließlich lokale Softwareinvarianten. T-001–T-080 bleiben insgesamt nicht als Produktabnahme ausgeführt; insbesondere Lean, formal-semantic review, TreeSHAP und rigorose ζ-Nullstellenzertifizierung sind nicht implementiert bzw. nicht gelaufen. Keine RH-Lösung oder Widerlegung wird behauptet.


# 8. Exakte Geometrieprüfung für mögliche Off-Line-Nullstellen

Am 2026-11-07 wurde `rectangle_is_off_critical_line(left, right)` in `fruitstack_rh.py` ergänzt. Sie parst rationale Grenzen mit Python `Fraction` und akzeptiert geometrisch nur Intervalle innerhalb `0 < Re(s) < 1`, die `Re(s)=1/2` vollständig ausschließen. Tests decken linke/rechte Seite, Geradenkontakt, Überschreitung des Streifens und umgekehrte Grenzen ab.

Das ist ausschließlich eine exakte Eingabe-/Geometrieschranke für einen späteren Rechteckkandidaten. Sie berechnet weder `ζ`, noch isoliert oder zählt sie Nullstellen und ist kein zertifizierter Gegenbeweisworkflow. Nach der Ergänzung: `py_compile` bestanden, `13 passed`, CLI-`self-check` `SELF_CHECK_PASS`; Live-Datenbank unverändert bei 7 Aussagen, 0 Inferenzkanten und 22 Ereignissen.


# 9. Verifikationsstatus getrennt und exakte Testfunktionskalibrierung

Die Luna-Implementierungsprüfung fand einen Statusfehler: `report()` zählte eine alleinige Semantikprüfung oder Kernelstatus fälschlich als verifizierte RH-Aussage. Bericht und Regressionstests trennen diese Felder nun. `verified_rh_claims` bleibt explizit leer; `rh_kernel_accepted_claims`, `rh_semantic_review_refs` und `rh_verification_workflow=NOT_IMPLEMENTED` sind separate Felder. Ein unabhängiger Receipt-Workflow ist weiterhin nicht vorhanden.

Zusätzlich prüft `exact_polynomial_zero_certificate()` mit rationaler Gaussian-Arithmetik, ob ein angegebener Punkt exakt Nullstelle eines angegebenen Polynoms ist und außerhalb der kritischen Geraden im offenen Streifen liegt. Damit ist ein kleiner positiver/negativer Testfunktionsfall ausführbar; dies prüft weder `ζ` noch eine RH-Widerlegung. `real_interval_is_off_critical_line()` wurde dem Umfang entsprechend benannt.

Aktuelle Verifikation am 2026-11-07: `python3 -m py_compile fruitstack_rh.py`, `python3 -m pytest -q tests` → `17 passed`, CLI `self-check` → `SELF_CHECK_PASS`. Live-Datenbank unverändert: 7 Aussagen, 0 Inferenzkanten, 22 Events, keine verifizierten RH-Claims, Journal konsistent.

# 10. Zertifikatskandidaten und CLI-Integritätslauf

Der Forschungsgraph enthält nun einen getrennten `zero_candidates`-Datensatz für rationale Rechteckgrenzen und ein referenziertes lokales Artefakt. `add-zero-candidate` verlangt, dass das Realteilintervall vollständig im offenen kritischen Streifen liegt und `1/2` ausschließt, die Imaginärgrenzen steigen und eine Artefaktdatei existiert. Das Artefakt erhält einen SHA-256-Digest; `report` meldet später `MATCH`, `MISMATCH` oder `MISSING`. Der Status bleibt immer `CANDIDATE_ONLY`: weder Rechteckgeometrie noch Hash noch beliebiger Artefakttext weist eine Nullstelle nach.

Am 2026-11-07 lief die CLI mit einem frischen temporären DuckDB-Pfad durch: Kandidat angelegt, Report geprüft (`CANDIDATE_ONLY`, `MATCH`, leere `verified_rh_claims`), Datei anschließend verändert und Report erneut geprüft (`MISMATCH`, weiterhin leere `verified_rh_claims`). Beide Pfade bestanden (`CLI_SMOKE_PASS`, `TAMPER_SMOKE_PASS`). Ein erster Aufruf mit falschen, nicht unterstützten Flag-Namen wurde verworfen; nach Anpassung an das dokumentierte Interface bestand der Lauf. Keine produktive Forschungsdatenbank wurde geändert.

Die Rechteckprüfung verlangt positive Breite; ein degeneriertes Realteilintervall wird verworfen. Regressionstest deckt diesen Randfall ab. Der aktuelle Testbestand umfasst 24 Tests; `python3 -m pytest -q tests` ergab `24 passed`, `py_compile` und CLI-`self-check` bestanden. Der frische CLI-Smoke- und Tamper-Lauf besteht wie oben beschrieben. Lean-Kernel, zertifizierte ζ-Nullstellenexistenz, semantische RH-Abnahme, SHAP und T-001–T-080-Produktabnahme bleiben nicht implementiert bzw. nicht ausgeführt.


# 11. Exakter Testfunktions-Zertifikatspfad

Am 2026-11-07 wurde `certify_test_function_zero()` ergänzt. Die Funktion verbindet die rationale Gaussian-Polynomprüfung mit einem nichtdegenerierten rationalen Rechteck, verlangt den exakten Nullstellenpunkt strikt innerhalb des Rechtecks und gibt einen typisierten `TEST_FUNCTION_ONLY`-Datensatz zurück. Manipulierte Polynomkoeffizienten und außerhalb liegende Randpunkte werden abgewiesen. Der Datensatz bleibt in-memory; er ist weder persistenter Verifier-Receipt noch Aussage über ζ oder RH.

Verifikation: `python3 -m py_compile fruitstack_rh.py`, `python3 -m pytest -q tests` → `27 passed`, CLI `self-check` → `SELF_CHECK_PASS`. Das ist eine exakte Testfunktions-Kalibrierung für T-041, keine Argumentprinzip-/Rouché-Nullstellenzählung (T-050 bleibt `NOT_RUN`) und kein zertifizierter ζ-Gegenbeweis. Keine Lean- oder SHAP-Fähigkeit wurde hinzugefügt; Forschungsdatenbank und kanonische FruitStack-Repositories blieben unverändert.


# 12. Statement-/Journal-Konsistenz und aktuelle Regressionen

Nach der Luna-Integritätsprüfung wurde ein konkreter Vertrauensfehler geschlossen: `report()` verglich die materialisierten Statement-Felder zuvor nicht mit dem letzten `STATEMENT_CREATED`-Ereignis. Neue Seed- und Statement-Ereignisse binden nun Text, Version, Gültigkeitsstatus, `formal_ref` und `semantic_review_ref`. Der Report markiert Abweichungen als `MISMATCH`, zeigt den Status dann als `OPEN` und klassifiziert Ereignisse mit fehlenden historischen Feldern als `LEGACY_PARTIAL`, ohne den Bestand umzuschreiben. `rh_kernel_accepted_claims` bleibt leer, solange kein unabhängiger Receipt-Workflow existiert. `journal_valid` weist nur die Hashketten-Konsistenz nach, keine kryptografische Manipulationssicherheit.

Zusätzliche Regressionen prüfen materialisierte Zeilenmanipulation, manipuliertes und nicht mehr gültiges Eventjournal, rückwärtskompatible Teilereignisse, neue vollständige Events sowie den komplexen Restfehler `i` bei Polynomprüfung. Aktueller lokaler Stand: `python3 -m py_compile fruitstack_rh.py` bestanden, `python3 -m pytest -q tests` → `32 passed`, CLI `self-check` → `SELF_CHECK_PASS`. Die vorhandene DB bleibt bei 7 Aussagen und 22 Ereignissen; Report: `journal_valid=true`, `verified_rh_claims=[]`, Statement-Events `LEGACY_PARTIAL`. Keine DB-Migration, kein Lean-Receipt, keine SHAP- oder ζ-Zertifizierung wurde implementiert.

# 13. Gegenprüfung materialisierter Nullstellenkandidaten

`report()` bindet nun auch jede gespeicherte Nullstellenkandidaten-Zeile an ihr letztes `ZERO_CANDIDATE_RECORDED`-Ereignis und gibt `record_integrity` (`MATCH`, `MISMATCH` oder `UNJOURNALED`) aus. Ein manipuliertes Rechteck im materialisierten Datensatz wird so sichtbar; der Status bleibt unabhängig davon stets `CANDIDATE_ONLY`. Der Regressionstest prüft die Zeilenmanipulation und verhindert eine implizite Hochstufung. Der Ereignis-Hash ist weiterhin unkeyed und kein manipulationssicherer Receipt.

# 14. Inferenz-Regel an Erstellungsereignis gebunden

## 14.1 Provenienzprüfung für Quellen, Forschungsleads und Semantik-Referenzen

Bei der Fortsetzung am 2026-11-07 wurde ein weiterer Report-Integritätsfehler geschlossen: `report()` gab Quellen- und Forschungslead-Status direkt aus materialisierten DuckDB-Zeilen aus. Direkte SQL-Änderungen konnten diese Werte verändern, obwohl die Ereigniskette unverändert blieb. Der Report vergleicht jetzt Quellenfelder und Forschungslead-Kanten mit `EVIDENCE_REGISTERED` beziehungsweise `RESEARCH_DEPENDENCY_CREATED`. Abweichende Quellen erscheinen als `SOURCE_UNVERIFIED`, abweichende Leads bleiben höchstens `RESEARCH_LEAD`; beide erhalten `MISMATCH`. Ein ungültiges Journal deaktiviert die event-abgeleiteten Status. Die ausgegebene RH-Semantik-Review-Referenz wird nur noch für eine passende, intakte Statement-Zeile mit Review-Status ausgegeben.

Regressionen decken manipulierten Forschungslead-Status und manipulierte Quellen-URI ab; der frühere Semantik-Referenz-Test erwartet nun keine ungeprüfte Referenz. Verifikation am 2026-11-07: `python3 -m pytest -q tests` → `39 passed`; `python3 fruitstack_rh.py self-check` → `SELF_CHECK_PASS`; Start auf frischer temporärer DB und Report → `FRESH_DB_REPORT_PASS`. Danach wurde die bereits vorhandene lokale `state/research.duckdb` vor Änderung nach `/tmp/fruitstack-rh-research-before-20261107.duckdb` kopiert, idempotent geseeded und per CLI ausgelesen: 7 Aussagen, 0 Inferenzkanten, 22 Events, intakte Ereigniskette, vier Quellen und sechs Leads mit passender Event-Provenienz, keine verifizierten RH-Claims. Das additive Schema ergänzte die fehlende `zero_candidates`-Tabelle; bestehende Aussage-/Eventzahlen blieben unverändert.

Grenze: Der unkeyed Ereignishash ist kein kryptografisch authentifizierter Nachweis. Lean-Receipt-Workflow, ζ-Nullstellenzertifizierung, RH-Beweis/Widerlegung sowie T-001–T-080-Produktabnahme sind weiterhin nicht implementiert oder nicht ausgeführt.

`INFERENCE_CREATED` bindet jetzt zusätzlich das materialisierte Regel-Feld (`user-supplied`) an den Ereignispayload. `report()` prüft damit Schlussfolgerung, vollständige Prämissenliste, Regel, Status und Proof-Referenz gemeinsam. Eine nachträgliche SQL-Änderung der Regel wird als `MISMATCH` gemeldet; ein verdächtiger `LINK_PROVED`-Status bleibt `LINK_HYPOTHESIS`. Regressionstest: `test_inference_rule_is_bound_to_creation_event`.

Verifikation am 2026-11-07: `python3 -m py_compile fruitstack_rh.py`, `python3 -m pytest -q tests` → `36 passed`; `python3 fruitstack_rh.py self-check` → `SELF_CHECK_PASS`. Die Produktions-/Forschungsdatenbank wurde durch diese Tests nicht verändert. Die Prüfung bleibt eine lokale Konsistenzkontrolle, kein authentifizierter Receipt und kein mathematischer Beweis.

# 15. Luna-Schwarm-Fortsetzung: Inferenzprojektion und Order-Kalibrierung

Auf Nutzerauftrag wurden vier read-only Luna-Prüfungen aufgeteilt: Inferenzdatenintegrität, ML-Versuchsdesign, mathematische Forschungsbehauptungen/Quellen sowie lokaler Funktionsumfang. Zwei unabhängige Reviewer fanden denselben Fehler in `report()`: Ein `INNER JOIN` ließ eine Inferenz vollständig verschwinden, wenn alle Zeilen in `inference_premises` gelöscht wurden. Das wurde durch `LEFT JOIN` plus leere Prämissenliste behoben; der vorhandene Eventpayload macht den Datensatz nun sichtbar als `MISMATCH` und stuft den Status auf `LINK_HYPOTHESIS` herab. Ein Regressionstest deckt vollständiges Löschen der Prämissen ab.

Der ML-Reviewer stellte fest, dass die alten Versuchsarme unterschiedliche Kandidatenmengen statt derselben Kandidaten in verschiedener Reihenfolge prüften; die Arm-Unterschiede waren daher kein isolierter Order-Effekt. Der Harness verwendet nun einen eingefrorenen gemeinsamen Vier-Kandidaten-Pool, drei dokumentierte Permutationen und ein identisches Budget von zwei Verifikationen je Arm. Dies ist nur eine deterministische, synthetische Order-Kalibrierung: kein gelerntes Ranking, keine Gewichtsstörung, kein SHAP, keine ζ-Auswertung und kein statistischer Nachweis eines ML-Vorteils. Der Rodgers–Tao DOI-Seedsatz wurde von `10.1017/fmp.2020.26` auf `10.1017/fmp.2020.6` korrigiert.

Verifikation nach Änderungen am 2026-11-07: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider` → `76 passed`; `python3 fruitstack_rh.py self-check` → `SELF_CHECK_PASS`. Beim ersten Testlauf traten zwei Regressionen auf (DuckDB gab die aggregierte leere Liste als `NULL` zurück; die neue Kontrollpermutation begann mit zwei Negativfällen); beides wurde korrigiert und der vollständige Lauf danach bestanden.

Der Luna-Quellenreview konnte keine Webprüfung durchführen, weil das vorgeschriebene lokale `agent-reach`-Skillfile nicht auffindbar war; daher wurden keine neuen externen Quellenbehauptungen daraus übernommen. Seine statische Empfehlung bleibt: CCM-Einzelaufgaben im Forschungsgraph als Hypothesen bzw. aus Manuskript abgeleitete offene Beweispflichten beschreiben, nicht als bereits quellenverifizierte Theoreme. Die Repository-Prüfung bestätigt weiterhin: kein Lean/Mathlib-Verifikationsworkflow, keine RH-Beweissuche, keine zertifizierte ζ-Nullstellenisolierung und keine TreeSHAP-/Gewichtsperturbationspipeline in diesem isolierten Projektstand.
