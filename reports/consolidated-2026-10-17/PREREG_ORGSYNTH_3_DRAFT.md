# PREREG-ORGSYNTH-3 — Registrierungsentwurf (PREPARED, NOT FROZEN, NOT LAUNCHED)

Stand 2026-10-17, nach der C-Arm-Forensik (Assessment §14). **Kein Providerruf, kein Einfrieren, kein Start** ohne gesonderte ausdrückliche Eigentümerfreigabe. OGI-012 bleibt unberührt, nichts hier ändert dessen Protokoll oder Evidenz. Die 50 Entwicklungsaufgaben und alle Aufgaben der Forensik sind **nicht** Teil dieses Tests.

## 1. Frage
Verbessert die vollständige RG/2-Organisation das **endgültige, unabhängig bewertete Aufgabenergebnis** gegenüber fair abgestimmten Kontrollen — und wie viel davon entsteht durch **automatische Synthese/Konsolidierung** statt durch bloß stärkere Einzelmodelle? Die Forensik zeigt, dass frühere Verluste vor allem aus Gate-Blockaden und aus dem Ausfall der Syntheseaufrufe stammen; diese Studie misst erst, ob ohne diese Defekte ein Organisationsvorteil besteht.

## 2. Arme (gleiche Aufgaben, gleicher zugänglicher Modellpool, gleicher Informationszugang, gleiche Budgets je Aufgabe)
| Arm | Inhalt | Zweck |
|---|---|---|
| A0 | **aktuelles Synthesemodell S0 allein** (das Modell, das RG/2 heute als Synthesizer zugewiesen bekäme) | Basis der Modellstärke |
| A1 | **stärkstes zulässiges Einzelmodell S1 allein** (Auswahl nur aus Kalibrierdaten; Fachbereich: das Modell, das als starker Synthesizer eingesetzt wird) | Kontrolle „das stärkere Modell löst es allein“: Gewinne durch allgemein bessere Schlussfolgerung dürfen nicht der Organisation zugeschrieben werden |
| B | nicht organisiertes Multi-Modell (≥ 3 verschiedene Abstammungslinien, feste Regel, keine Verifikation/Konsolidierung) | Modellvielfalt ohne Organisation |
| C0 | RG/2 mit Synthesizer S0 | Organisation, aktueller Synthesizer |
| C1 | RG/2 mit Synthesizer S1 | Organisation, starker Synthesizer; **gleiche Arbeiter** wie C0, nur der Synthesizer wechselt |
| D | Ablation von C1: Beiträge werden erhalten, die Synthese-/Verifikationsstufe ist durch eine feste Regel ersetzt (Vereinigung, deterministische Schlüsselextraktion, kein Modell) | Beitrag der Konsolidierung/Synthese |
Synthesizer-Zuweisung: S0 und S1 sind im Manifest festgelegt; sie dürfen sich in C1 nicht zugleich als Arbeiter von der Pool-Verteilung unterscheiden (Arbeiterpool identisch in C0/C1/B/D).

## 3. Hypothesen und Entscheidungsregeln (einseitig, α = 0,05, Marge m = 0 sofern nicht anders freigegeben)
- **H1 (primär, Schnitt-Vereinigung):** C1 > A1 **und** C1 > B im Aufgabenerfolg. Positiv: beide Vergleiche signifikant mit Effekt ≥ 0. Negativ: C1 signifikant schlechter als A1 **oder** B (einseitig α = 0,05 in die Gegenrichtung). Sonst inkonklusiv.
- **H2 (Synthesizer-Stärke, isoliert von Modellstärke):** Differenz-der-Differenzen (C1 − C0) − (A1 − A0) > 0. Nur wenn dieser Interaktionsterm positiv ist, wird ein Gewinn der Synthese zugeschrieben, nicht bloß der allgemeinen Modellstärke.
- **H3 (Konsolidierungswert):** C1 > D.
- Holm-Korrektur über H2/H3 (H1 ist als Schnitt-Vereinigung eigenständig).

## 4. Aufgaben und Referenzen
Frische Menge, Seed nach dem Code-Freeze erzeugt, Referenzen unabhängig von zwei Bewertern validiert und versiegelt. Strata: Fakt mit Primärquelle / Fakt ohne zulässige Primärquelle / Mehrquellen / widersprüchliche Quellen / Schlüsseltypen (Datum, Jahr, Ganzzahl, Bezeichner, Text). Die Strata „ohne zulässige Primärquelle“ und „Schlüssel nur in unverifizierter Information“ sind enthalten, weil dort die beobachteten Verluste lagen.

## 5. Gleicher Zugang und Ressourcen
Alle Arme: FREE_ONLY, gemeinsames ParentBudget je Aufgabe mit identischen Obergrenzen (Aufrufe, Tokens, Wandzeit), gleicher Retriever und gleiche Quellenrichtlinie, gleiche Ausgabegrenzen **nach Fähigkeitsprofil** (siehe §7). **Grounding-Richtlinie:** interne Hypothesen dürfen ohne vorheriges Retrieval formuliert und beantwortet werden; sie werden als UNVERIFIED gekennzeichnet; unabhängige Verifikation bleibt Pflicht, wo der Aufgaben-/Wissensautoritätsvertrag sie verlangt (C0, C1, D, B nutzen dieselbe Regel). Unbekannte Kosten bleiben unbekannt.

## 6. Ergebnisgrößen
Primär: Aufgabenerfolg (fse-inquiry/1, Note 1,0), in zwei vorab festgelegten Varianten: **P1** richtig unabhängig vom Kennzeichen, **P2** richtig *und* verifiziert. Sekundär (erklärend, ersetzen den Primärbefund nicht): korrekte Einzelbeiträge, Komplementarität, durch Kritik entdeckte Fehler und übernommene Korrekturen, im Konsolidieren verlorene korrekte Antworten (FSE-ATTRIBUTION/1: Integrationsverlustrate mit Ort), Marginalgewinn (FSE-MARGINAL/1), Aufrufe, Tokens, Wandzeit, Kosten, Abdeckung/Abstention. **Abstention zählt als nicht richtig** (und wird gesondert berichtet). Fehlende Antworten und Ausfälle bleiben im Nenner (Intention-to-treat); Ausfallklassen werden getrennt ausgewiesen (INFRASTRUCTURE, BUDGET, GATE_BLOCK, INTEGRATION_LOSS, NO_CORRECT_CONTRIBUTION, UNKNOWN).

## 7. Mindestbedingungen für Provider und Modelle
1. ≥ 3 Abstammungslinien mit je ≥ 60 Kalibrieraufrufen, Ausführungsquote ≥ 0,8, Receipt für jede Ausführung, paarweise INDEPENDENT im G2-Test (phi ≤ 0,5, gleich-falsche-Antwort ≤ 0,5 auf ≥ 40 gemeinsamen Aufgaben); sonst Etikett „Multi-Modell, Unabhängigkeit ungemessen“ oder kein Lauf.
2. **Fähigkeitsprofile statt Sonderregeln:** Vor dem Lauf wird je Modell die sichtbare Antwortquote bei der registrierten Ausgabegrenze auf einer Kalibrierungsmenge gemessen (Beobachtung: nemotron-3.5-lightning, `reasoning: true`, lieferte bei 2048 Ausgabetokens in 9 von 9 Synthesen keinen sichtbaren Text). Modelle mit einer sichtbaren Antwortquote unter einer vorab festgelegten Schwelle (Vorschlag 0,9) oder mit unbrauchbarem Zitatformat sind für die Rolle Synthesizer/Verifier nicht zulässig; das Profil wird im Manifest dokumentiert. Keine undokumentierten Überschreibungen pro Lauf.
3. S1 = stärkstes zulässiges Modell nach Kalibrierung (Verfügbarkeit vorbehalten); ist es nicht ausführbar, entfällt die Synthesizer-Stärke-Aussage (H2 wird als NOT_TESTABLE berichtet), nicht umdeklariert.
4. Kein Modell nur für einen Arm; Fähigkeits-Snapshot des Pools vor dem Lauf gespeichert.
5. Synthese- und Verifier-Aufrufe haben ein registriertes Ausfallverhalten (Wiederholung/Fallback), damit ein einzelner Syntheseausfall nicht ein vollständiges Ergebnis kostet; der Fallback ist Teil des Armes und wird in der ITT-Auswertung mitgemessen.
6. FREE_ONLY, ParentBudget gebunden, Quotenreserve für die gesamte Schedule (Vorab-Zählung); Abbruch bei erschöpfter Versorgung nach der OGI-011-Regel, getrennt von Wirksamkeit.

## 8. Auswertung
Gepaarter exakter Test / clusterrobuster Schnitt-Vereinigungs-Test (Cluster = Subfamilie), exakter Vorzeichentest als Sensitivität, Konfidenzintervalle in Prozentpunkten, Ressourcenunterschiede neben jedem Effekt. Zusätzlich vorab festgelegt: Sensitivität ohne Aufgaben mit versorgungsbedingtem Ausfall in irgendeinem Arm (getrennt berichtet, nicht ersetzend). Ein gemessener Nullgewinn oder eine Regression wird mit gleichem Gewicht berichtet.

## 9. Stichprobe und Power (Formel offen gelegt)
Gepaarte Binärdaten: n = (z_α + z_β)² · (p_disc − δ²) / δ², einseitig α = 0,05, Designeffekt 1,3. Für p_disc = 0,35: δ = 0,15 → N = 117 (Power 0,80) bzw. 163 (0,90); δ = 0,10 → 274 bzw. 379. H2 ist ein Differenz-der-Differenzen-Test mit etwa doppelter Varianz; für δ = 0,10 ergäbe sich grob 2 × 274 ≈ 550 (Power 0,80, Annahmen wie oben). **Eigentümerentscheidung:** N = 170 (H1 mit δ = 0,15, Power ≈ 0,90) oder N = 280 (H3 mit δ = 0,10 bei 0,80) oder N ≈ 550 (H2). Annahmen (p_disc, δ) sind keine Messwerte; die 50 Entwicklungsaufgaben liefern wegen der Ausfälle keine belastbare Schätzung. Aufwand nur als Größenordnung aus historischen Verbräuchen (F3-alt: ≈ 17 Dispatches und 16,4 k Tokens je Aufgabe, Einzelaufruf ≈ 0,7 k): drei organisierte Arme (C0, C1, D) ≈ 51 Dispatches, B ≈ 3, A0/A1 ≈ 2 → ≈ 56 Dispatches und ≈ 55 k Tokens je Aufgabe, bei N = 280 etwa 16 000 Dispatches und 15 M Tokens. RG/2 ist nicht gemessen; die Obergrenzen sind eine Eigentümerentscheidung.

## 10. Software-Voraussetzungen vor Freigabe
CherryMe ≥ 0.4.2 nach Eigentümerentscheid gemergt/installiert; Harness-Anpassung, die Schlüsselkette und Beitragsbuch nutzt, UNVERIFIED-Kandidaten gekennzeichnet ausgibt und für den Syntheseaufruf Wiederholung/Fallback registriert; Manifest mit Commit-Hashes und Hashes der vollständigen Testläufe; der eingefrorene Harness `runners/f2f3_epoch2.py` bleibt unverändert (Entwicklungsevidenz).

## 11. Was die Studie nicht behauptet
Kein Befund aus Entwicklungsdaten gilt als Bestätigung. Ein Vorteil von C1 gegenüber A1 und B ist ein Organisationsvorteil nur, soweit H2/H3 und der Ablationsarm ihn von Modellstärke und Modellvielfalt trennen. Ein Null- oder negatives Ergebnis ist ein gültiges Ergebnis.
