# 02_flows.md — Flows (Sequenzen) der Demo

## Zweck dieses Dokuments

Dieses Dokument beschreibt die zwei zentralen End-to-End-Flows der Demo.
Die Flows sind normativ: Sie bestimmen Endpoints, Datenbankzugriffe und Audit-Ereignisse.

Die Demo umfasst zwei Sequenzen:

- Flow 1: Erstellung eines Datenobjekts (POST /objects)
- Flow 2: Zugriffsanfrage auf ein Datenobjekt (POST /access)

---

## Gemeinsame Begriffe / Artefakte

### DataObject (Policy-Objekt)

Ein DataObject besteht aus:
- Nutzdaten (payload)
- Pflicht-Metadaten: purpose, policy_version

### Identität / Kontext (Stub)

Identität und Rolle werden über HTTP-Header simuliert:
- X-Actor: eindeutige Kennung (z. B. Nutzer-ID oder Service-Name)
- X-Role: Rolle/Kontext (z. B. "caseworker", "auditor")

### Datenbanktabellen

- data_objects: speichert Datenobjekte inkl. Metadaten
- audit_events: speichert Audit-Ereignisse (append-only)

### Audit-Prinzip

Für jede relevante Aktion wird ein Audit-Ereignis erzeugt.
Das Audit ist append-only: bestehende Einträge werden nicht verändert, sondern nur ergänzt.

---

## Flow 1 — POST /objects (Erstellung eines Datenobjekts)

### Ziel

Erstellt ein neues Datenobjekt (Policy-Objekt) inkl. Pflicht-Metadaten und erzeugt ein Audit-Ereignis.

### Endpoint

- Methode: POST
- Pfad: /objects

### Inputs

Header:
- X-Actor
- X-Role

Request Body (JSON):
- payload
- purpose
- policy_version

### Verarbeitungsschritte (Sequenz)

1) Validate
- Request wird gegen das DataObject-Model validiert
- payload, purpose und policy_version müssen vorhanden sein
- Bei Validierungsfehler: 422

2) Store
- DataObject wird in SQLite in data_objects gespeichert
- Ergebnis: object_id (neu generiert)

3) Audit: OBJECT_CREATED
- Audit-Ereignis wird geschrieben (append-only)
- Event-Typ: OBJECT_CREATED
- Felder (Minimum):
  - request_id
  - actor (aus X-Actor)
  - role (aus X-Role)
  - action = "OBJECT_CREATED"
  - object_id
  - purpose
  - policy_version
  - timestamp

4) Response
- Response enthält object_id

### Output

Response Body (JSON):
- object_id
- status = "created"

### Audit-Zeitpunkt

- Audit wird nach erfolgreichem Speichern geschrieben (store → audit)
- Bei Fehlern vor dem Speichern entsteht kein OBJECT_CREATED Event

---

## Flow 2 — POST /access (Zugriffsanfrage auf ein Datenobjekt)

### Ziel

Simuliert einen Zugriff auf ein gespeichertes Datenobjekt.
Der Zugriff wird anhand von Zweckbindung (purpose) und Rolle (X-Role) entschieden (allow/deny) und revisionsfähig protokolliert.

### Endpoint

- Methode: POST
- Pfad: /access

### Inputs

Header:
- X-Actor
- X-Role

Request Body (JSON):
- object_id
- requested_purpose

### Verarbeitungsschritte (Sequenz)

1) Read Context
- X-Actor und X-Role werden gelesen
- Wenn Header fehlen: 400

2) Load Object
- data_objects wird per object_id geladen
- Wenn object_id nicht existiert: 404

3) Evaluate Policy (PDP)
- policy.py wird aufgerufen mit:
  - role
  - requested_purpose
  - object_purpose (aus data_objects)
  - policy_version (aus data_objects)
- Ergebnis:
  - decision: allow oder deny
  - reason: Begründung
  - policy_version: verwendete Policy-Version

4) Enforce (PEP)
- decision == allow:
  - payload wird zurückgegeben
- decision == deny:
  - payload wird nicht zurückgegeben

5) Audit: ACCESS_REQUESTED
- Audit-Ereignis wird immer geschrieben (allow und deny)
- Event-Typ: ACCESS_REQUESTED
- Felder (Minimum):
  - request_id
  - actor
  - role
  - action = "ACCESS_REQUESTED"
  - object_id
  - requested_purpose
  - decision (allow/deny)
  - reason
  - policy_version
  - timestamp

6) Response
- allow: response enthält decision, object_id, payload
- deny: response enthält decision, object_id, reason

### Output

Allow Response (JSON):
- decision = "allow"
- object_id
- payload

Deny Response (JSON):
- decision = "deny"
- object_id
- reason

### Audit-Zeitpunkt

- Audit wird nach der Policy-Entscheidung geschrieben (evaluate → audit → response)
- Auch denied Zugriffe werden protokolliert (Audit Evidence)

---

## Zusammenfassung: Audit-Events 

- OBJECT_CREATED
  - wird nur bei erfolgreichem Speichern erzeugt

- ACCESS_REQUESTED
  - wird bei jeder Zugriffsanfrage erzeugt (allow und deny)

Dieses Set ist ausreichend, um Zweckbindung (Decision/Enforcement) und Auditierbarkeit (Evidence) im Scope der Demo nachzuweisen.
