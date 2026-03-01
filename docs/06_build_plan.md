# 06_build_plan.md — Build Plan (Instanziierung)

## Zweck dieses Dokuments

Dieses Dokument beschreibt die konkrete Implementierungsreihenfolge der Demo.

Der Build Plan ist vollständig aus Scope, Flows, Datenmodell, Policies und Evaluation abgeleitet.
Er führt keine neuen Konzepte ein.

Ziel ist eine schlanke, kontrollierte Umsetzung des Proof of Concept.

---

# Phase 1 — Dokumentation abgeschlossen

Status: abgeschlossen

Ergebnis:

- 00_scope.md definiert den Rahmen
- 01_architecture.md mappt Referenzmodell auf Demo
- 02_flows.md definiert End-to-End Sequenzen
- 03_data_model.md fixiert Schema
- 04_policies.md definiert Entscheidungslogik
- 05_evaluation.md definiert Nachweisszenarien

Definition of Done Phase 1:

- Alle Dokumente konsistent
- Keine offenen Architekturentscheidungen
- Keine unklaren Felder oder Regeln

Erst danach beginnt Implementierung.

---

# Phase 2 — Ingest + Audit (Flow 1)

Ziel: Implementierung von POST /objects inkl. Audit Evidence.

Umfang:

- src/models.py
  - DataObject Modell
- scripts/init_db.py
  - Erstellung von data_objects und audit_events Tabellen
- src/db.py
  - Insert-Funktion für data_objects
- src/audit.py
  - Funktion: write_audit_event(...)
- src/app.py
  - Endpoint POST /objects
  - Validierung
  - Speicherung
  - Audit: OBJECT_CREATED

Erfolgskriterium Phase 2:

- Ein DataObject kann erstellt werden
- OBJECT_CREATED Audit-Event wird geschrieben
- Evaluation Szenario 1, Schritt 1 funktioniert

---

# Phase 3 — Access + Purpose Enforcement (Flow 2)

Ziel: Implementierung von Policy Enforcement via PDP/PEP.

Umfang:

- src/policy.py
  - Implementierung Policy v1 (analyst/support/guest)
- src/app.py
  - Endpoint POST /access
  - Header-Auswertung (X-Actor, X-Role)
  - Laden des DataObject
  - Aufruf policy.py
  - Entscheidung allow/deny
  - Audit: ACCESS_REQUESTED

Erfolgskriterium Phase 3:

- Szenario 1 ergibt allow
- Szenario 2 ergibt deny (purpose_mismatch)
- Szenario 3 ergibt deny (role_not_allowed)
- ACCESS_REQUESTED Audit-Event wird immer geschrieben

---

# Phase 4 — Evidence Package (Evaluation & Abschluss)

Ziel: Nachweisführung gemäß docs/05_evaluation.md

Umfang:

- Durchführung aller 3 Szenarien
- Prüfung audit_events Tabelle
- Sicherstellen:
  - decision korrekt
  - reason korrekt
  - policy_version korrekt
- Dokumentation der Ergebnisse (Screenshots / Auszüge für Kapitel 5)

Erfolgskriterium Phase 4:

- Alle 3 Szenarien verhalten sich exakt wie definiert
- Audit Evidence vollständig vorhanden
- Artefakt erfüllt Definition of Done

---

# Nicht Teil des Build Plans

Folgende Bestandteile werden bewusst nicht implementiert:

- IAM/SSO
- Externe Policy Engine (z. B. OPA)
- Message Broker
- Verschlüsselung / Key Management
- Skalierung / HA
- UI / Frontend

Diese sind Bestandteil der Referenzarchitektur, jedoch nicht Teil der schlanken Instanziierung.

