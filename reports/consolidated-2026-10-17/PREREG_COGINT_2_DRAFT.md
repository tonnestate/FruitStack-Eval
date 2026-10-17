> **SUPERSEDED 2026-10-17 by `PREREG_ORGSYNTH_3_DRAFT.md`** (adds synthesizer strength as a factor and the strong-model solo control after the C-arm forensics, assessment §14). Kept for history.

# PREREG-COGINT-2 — Registrierungsentwurf (PREPARED, NOT FROZEN, NOT LAUNCHED)

Stand 2026-10-17. Entwurf für den konfirmatorischen Vergleich der integrierten FruitStack-Organisation mit Kontrollen (Auftrag FRUITSTACK-COGNITIVE-INTEGRATION/2, Abschnitt 10). **Es wurde kein Provider aufgerufen. Dieser Entwurf friert nichts ein.** Einfrieren (Manifest-Hashes, Task-Seed, Schedule) und Start erfordern eine gesonderte ausdrückliche Eigentümerfreigabe. OGI-012 bleibt unberührt. Die 50 Entwicklungsaufgaben sind **nicht** Teil dieses Tests.

## 1. Fragen und Hypothesen
- **H1 (primär):** Die vollständige RG/2-Organisation (Arm C) erzielt auf einer frischen Aufgabenmenge eine höhere Aufgabenerfolgsquote als die bessere der beiden Kontrollen A (qualifiziertes Einzelmodell) und B (unorganisiertes Multi-Modell). Entscheidung als Schnitt-Vereinigungs-Test (C > A **und** C > B), je einseitig α = 0,05, Marge m = 0.
- **H2 (sekundär, Ablation):** C > D, wobei D dieselbe Organisation ohne Konsolidierungs-/Verifikationsstufe ist (Beiträge werden gesammelt und nach fester Regel gewählt). Isoliert den Beitrag von Konsolidierung/Verifikation.
- **Beschreibend (vorab festgelegt, keine Hypothese):** marginaler Erkenntnisgewinn je Aktivierung nach FSE-MARGINAL/1 (Delivery, Novelty, Correctness, Complementarity, Preservation, Decision lift, Ressourcen). Ein gemessener Nullgewinn ist ein gültiges Ergebnis; ein Null wegen fehlender Lieferung/Blockade ist NOT_MEASURABLE.

## 2. Arme (gleiche Aufgaben, gleicher zugänglicher Modellpool, gleicher Informationszugang, gleiche Budgets pro Aufgabe)
| Arm | Inhalt |
|---|---|
| A | bestes qualifiziertes Einzelmodell (Auswahl nur nach Kalibrierungsdaten, nie nach Pilot-/Konfirmationsdaten), gleiche Retrieval-Auszüge und gleiche Quellenrichtlinie wie C |
| B | dieselben Modelle (≥ 3 Abstammungslinien), feste Regel (z. B. Mehrheit/erste gültige Antwort), keine Verifikation, keine Organisation; ausdrücklich „Multi-Modell, nicht organisiert“ |
| C | vollständige RG/2-Organisation, CherryMe ≥ 0.4.2 mit Beitragsbuch, Schlüsselkette, ungegründeten Kandidaten (mit Kennzeichnung), dritter Verifier, lineage-bewusster AUTO-Unabhängigkeit |
| D | Ablation von C: Beiträge werden erhalten, aber ohne Verifikations-/Konsolidierungsstufe nach fester Regel kombiniert |
Alle Arme: FREE_ONLY, gemeinsames ParentBudget je Aufgabe (identische Obergrenzen für Aufrufe/Tokens/Zeit), identischer Retriever und identische Allowlist; ungegründete Antworten sind in allen Armen erlaubt und gleich zu kennzeichnen. Unabhängigkeits-Metadaten (`independence_key`, `independence_basis`, kanonische Modell-ID, Route, Fingerprint) werden aus den PlumMe-Receipts jedes Aufrufs gespeichert.

## 3. Aufgabenmenge und Referenzen
Frische Menge, Seed nach Code-Freeze erzeugt, Referenzen unabhängig von zwei Bewertern validiert und vor dem Lauf versiegelt, Strata: Fakt mit Primärquelle / Fakt ohne zulässige Primärquelle / Mehrquellen / widersprüchliche Quellen / Schlüsselwert-Typen (Datum, Jahr, Ganzzahl, Bezeichner, Text). Die Strata „ohne zulässige Primärquelle“ und „Schlüssel in unverifizierter Information“ sind enthalten, weil genau dort die historischen Verluste lagen.

## 4. Ergebnisgrößen (vorab)
Primär: Aufgabenerfolg (fse-inquiry/1, Note 1,0). Zwei Varianten, beide berichtet: **P1** richtig unabhängig vom Kennzeichen, **P2** richtig *und* verifiziert. Sekundär: Abdeckung/Abstention (Schweigen zählt nicht als richtig), Lieferquote, Neuheitsquote, Erhaltungsquote korrekter Beiträge, Komplementaritätsquote, Aufrufe, Tokens, Wandzeit, Kosten (unbekannt bleibt unbekannt). Ausfallklassen (QUOTA, MODEL_UNAVAILABLE, TRUNCATION, TIMEOUT, MALFORMED, RETRIEVAL, INSUFFICIENT_EVIDENCE, DISAGREEMENT) werden getrennt berichtet, nichts wird entfernt (Intention-to-treat).

## 5. Auswertung
Schnitt-Vereinigungs-Test einseitig α = 0,05 je Vergleich, familien-/Subfamilien-clusterrobuster Standardfehler, exakter Vorzeichentest als Sensitivität, Holm für sekundäre Vergleiche, Konfidenzintervalle in Prozentpunkten, Ressourcenunterschiede neben jedem Effekt. Marginalgewinn nach FSE-MARGINAL/1 mit den eingefrorenen G2-Schwellen (`config/g2_thresholds.toml`); Unabhängigkeit gilt nur bei bestandenem G2-Paartest, sonst `INDEPENDENCE_UNMEASURED`. Eine Pipeline-bedingte Verlustklasse (korrekter Beitrag nicht im Endergebnis) wird als technischer Defekt gemeldet und **nicht** in den Marginalgewinn der Modelle eingerechnet.

## 6. Stichprobe und Power (aus Formel, Annahmen offen gelegt)
Gepaarte Binärdaten, n = (z_α + z_β)² · (p_disc − δ²) / δ², einseitig α = 0,05, Designeffekt 1,3 (Cluster). Rechenwerte (`p_disc` = Anteil diskordanter Paare):

| δ (Effekt) | p_disc | Power 0,80 | Power 0,90 je Vergleich |
|---|---|---|---|
| 0,20 | 0,35 | 63 | 87 |
| 0,15 | 0,35 | 117 | 163 |
| 0,15 | 0,45 | 153 | 212 |
| 0,10 | 0,35 | 274 | 379 |
**Empfehlung zur Entscheidung des Eigentümers:** N = 170 (H1 mit δ = 0,15, p_disc = 0,35, Power ≈ 0,90 je Vergleich) oder N = 280 (zusätzlich H2 mit δ = 0,10 bei 0,80). p_disc und δ sind Annahmen, keine Messungen; die 50 Entwicklungsaufgaben liefern wegen Ausfällen keine belastbare Schätzung. Historischer Aufwand zur Orientierung (F3 alt: 854 Receipts / 818 165 Tokens für 50 Aufgaben ≈ 17 Dispatches, 16,4 k Tokens je Aufgabe; Kontrolle ≈ 0,7 k Tokens): bei N = 280 und vier Armen ist mit einer Größenordnung von 8–9 k Dispatches und ≈ 9 M Tokens zu rechnen — die Obergrenzen sind eine Eigentümerentscheidung.

## 7. Mindestbedingungen für Provider (Eignung)
1. ≥ 3 Abstammungslinien mit je ≥ 60 Kalibrieraufrufen, Ausführungsquote ≥ 0,8 und Receipt für jede Ausführung (G2).
2. Paarweise INDEPENDENT im G2-Test (phi ≤ 0,5, gleich-falsche-Antwort-Anteil ≤ 0,5 auf ≥ 40 gemeinsamen Aufgaben). Sonst werden B/C/D nur als „Multi-Modell, Unabhängigkeit ungemessen“ bezeichnet, oder der Lauf unterbleibt (Eigentümerentscheidung).
3. Kein Modell nur für einen Arm; Pool vor dem Lauf eingefroren (Fähigkeits-Snapshot gespeichert, was in den Entwicklungsläufen fehlte).
4. FREE_ONLY durchgesetzt, ParentBudget gebunden, Suche und Abruf paritätisch; Quoten ausreichend für die gesamte Schedule (Vorab-Zählung, Abbruch bei erschöpfter Versorgung nach der OGI-011-Regel, getrennt von Wirksamkeit gemeldet).
5. Retrieval-Ausfälle werden pro Frage persistiert (Ursache, Schritt) und zwischen Armen verglichen.

## 8. Software-Voraussetzungen (vor jeder Freigabe zu erfüllen)
CherryMe 0.4.2 (`cc/cognitive-recovery-001`) gemergt bzw. installiert nach Eigentümerentscheid; Harness-Anpassung, die Schlüsselkette und Beitragsbuch nutzt und unverifizierte Kandidaten gekennzeichnet ausgibt; PlumMe 0.1.15 / PeachMe 0.8.4 wie freigegeben; Manifest mit Commit-Hashes und Hashes der Testdateien (volle Suiten). Der Harness `runners/f2f3_epoch2.py` bleibt unverändert eingefroren (Dev-Evidenz).

## 9. Was der Test nicht behauptet
Kein Befund aus den 50 Entwicklungsaufgaben wird als Bestätigung gezählt. Ein Vorteil von C beweist nicht, dass „mehr Modelle klüger machen“; der Ablationsarm D und die Marginalgewinn-Analyse trennen Modellvielfalt von Organisation. Ein Nullgewinn oder eine Regression wird mit gleicher Gewichtung berichtet.
