# 03_data_model.md — Datenmodell (DataObject + Audit Evidence)

## Zweck dieses Dokuments

Dieses Dokument fixiert das Datenmodell der Demo.  
Es ist normativ für:

- src/models.py (Pydantic-Modelle)
- src/db.py (SQLite-Schema + Queries)
- src/audit.py (Audit-Event-Struktur)

Die Demo implementiert ein schlankes Datenmodell, das Zweckbindung (purpose) und Nachweisbarkeit (Audit Evidence) technisch abbildet.

---

## 1) DataObject (Policy-Objekt)

### 1.1 Pflichtfelder (API)

Ein DataObject MUSS folgende Felder enthalten:

- purpose (string, required)
- policy_version (string, required)
- payload (object/dict, required)

### 1.2 Erweiterte Metadaten (API, nullable)

Zusätzlich werden folgende Metadaten als Felder im Modell geführt, sind aber nicht verpflichtend:

- classification (string, nullable)
- owner (string, nullable)
- lineage_ref (string, nullable)

Begründung:
Diese Felder existieren im Referenzmodell (Classification/Purpose Registry, Stewardship, Lineage/Provenance), werden in der Demo jedoch nicht als eigene Services instanziiert. Die Felder erlauben eine spätere Erweiterung, ohne das Schema zu brechen.

---

## 2) Persistenzmodell (SQLite)

### 2.1 Tabelle: data_objects

Zweck:
Persistenz von Datenobjekten inkl. Metadaten.

Spaltenliste:

- object_id (TEXT, Primary Key)
- payload_json (TEXT, NOT NULL)        -- JSON serialisiert
- purpose (TEXT, NOT NULL)
- policy_version (TEXT, NOT NULL)
- classification (TEXT, NULL)
- owner (TEXT, NULL)
- lineage_ref (TEXT, NULL)
- created_at (TEXT, NOT NULL)          -- ISO-8601 Timestamp

Hinweis:
payload wird als JSON-String gespeichert (payload_json), um SQLite einfach zu halten.

---

### 2.2 Tabelle: audit_events (append-only)

Zweck:
Audit Evidence Log zur Nachweisführung von Aktionen und Entscheidungen.

Append-only Prinzip:
Einträge werden nur hinzugefügt (INSERT). Es gibt keine Updates/Deletes in der Demo-Logik.

Spaltenliste:

- event_id (TEXT, Primary Key)
- ts (TEXT, NOT NULL)                  -- ISO-8601 Timestamp
- request_id (TEXT, NOT NULL)
- actor (TEXT, NOT NULL)
- role (TEXT, NOT NULL)
- action (TEXT, NOT NULL)              -- z.B. OBJECT_CREATED, ACCESS_REQUESTED
- object_id (TEXT, NULL)               -- bei objektbezogenen Events gesetzt
- decision (TEXT, NULL)                -- allow/deny nur bei Zugriff
- reason (TEXT, NULL)                  -- Begründung nur bei Zugriff/Fehler
- purpose (TEXT, NULL)                 -- Kontext: object purpose oder requested purpose (Details in details_json)
- policy_version (TEXT, NULL)
- details_json (TEXT, NOT NULL)        -- JSON: zusätzliche Felder (z.B. requested_purpose)

Hinweis:
purpose wird zusätzlich in details_json präzisiert, um eindeutig zwischen object_purpose und requested_purpose unterscheiden zu können.

---

## 3) Beispiel: DataObject JSON (API Request)

Beispiel für POST /objects:

```json
{
  "payload": {
    "antrag_id": "BG-2026-000123",
    "betrag": 563.20,
    "leistung": "Buergergeld"
  },
  "purpose": "case_processing",
  "policy_version": "v1",
  "classification": null,
  "owner": null,
  "lineage_ref": null
}
```

---

## 4) Beispiel: Audit Events (Evidence)

### 4.1 OBJECT_CREATED

Beispiel-Eintrag (audit_events):

```json
{
  "event_id": "evt_01HXYZ...",
  "ts": "2026-03-01T14:30:12Z",
  "request_id": "req_01HXYZ...",
  "actor": "user_123",
  "role": "caseworker",
  "action": "OBJECT_CREATED",
  "object_id": "obj_01HXYZ...",
  "decision": null,
  "reason": null,
  "purpose": "case_processing",
  "policy_version": "v1",
  "details_json": {
    "endpoint": "/objects",
    "method": "POST"
  }
}
```

---

### 4.2 ACCESS_REQUESTED (allow)

Beispiel-Eintrag (audit_events):

```json
{
  "event_id": "evt_01HABC...",
  "ts": "2026-03-01T14:32:05Z",
  "request_id": "req_01HABC...",
  "actor": "user_123",
  "role": "caseworker",
  "action": "ACCESS_REQUESTED",
  "object_id": "obj_01HXYZ...",
  "decision": "allow",
  "reason": "role_and_purpose_match",
  "purpose": "case_processing",
  "policy_version": "v1",
  "details_json": {
    "endpoint": "/access",
    "method": "POST",
    "requested_purpose": "case_processing",
    "object_purpose": "case_processing"
  }
}
```

---

### 4.3 ACCESS_REQUESTED (deny)

Beispiel-Eintrag (audit_events):

```json
{
  "event_id": "evt_01HDEF...",
  "ts": "2026-03-01T14:33:40Z",
  "request_id": "req_01HDEF...",
  "actor": "user_987",
  "role": "auditor",
  "action": "ACCESS_REQUESTED",
  "object_id": "obj_01HXYZ...",
  "decision": "deny",
  "reason": "purpose_mismatch",
  "purpose": "case_processing",
  "policy_version": "v1",
  "details_json": {
    "endpoint": "/access",
    "method": "POST",
    "requested_purpose": "audit_review",
    "object_purpose": "case_processing"
  }
}
```

---

## 5) Konsistenz zu den Flows

- Flow 1 (POST /objects):
  - schreibt data_objects
  - erzeugt OBJECT_CREATED Audit-Event

- Flow 2 (POST /access):
  - liest data_objects
  - erzwingt allow/deny via PDP/PEP
  - erzeugt ACCESS_REQUESTED Audit-Event (immer)

Dieses Datenmodell ist das Minimum, um Zweckbindung und Audit Evidence im Scope der Demo nachzuweisen.
