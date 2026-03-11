# Szenario 2 — Deny (Purpose Mismatch)

## Ziel der Evaluation

Die folgenden Szenarien überprüfen die korrekte Durchsetzung der
Policy-Entscheidungen sowie die revisionsfähige Protokollierung
im Audit Log gemäß dem in docs/05_evaluation.md definierten Evidence Plan.

## Kontext

Rolle: analyst  
requested_purpose: billing  
object_purpose: analytics  

Erwartung: Zugriff wird verweigert.

---

## Request — POST /objects

### Header

```text
X-Actor: user_2
X-Role: analyst
```

### Body

```json
{
  "payload": {
    "invoice_id": "INV-777",
    "amount": 999
  },
  "purpose": "analytics",
  "policy_version": "v1"
}
```

---

## Response — POST /objects

```json
{
  "object_id": "84502981-302e-415b-be52-e221edf1ffc5",
  "status": "created"
}
```

---

## Request — POST /access

### Header

text
X-Actor: user_2
X-Role: analyst

### Body

```json
{
  "object_id": "84502981-302e-415b-be52-e221edf1ffc5",
  "requested_purpose": "billing"
}
```

---

## Response — POST /access

```json
{
  "decision": "deny",
  "object_id": "84502981-302e-415b-be52-e221edf1ffc5",
  "reason": "purpose_mismatch"
}
```

Hinweis: Bei `deny` wird kein `payload` zurückgegeben.

---

## Audit Evidence

### SQL-Abfrage

```sql
SELECT
  ts,
  actor,
  role,
  action,
  object_id,
  decision,
  reason,
  purpose,
  policy_version,
  details_json
FROM audit_events
WHERE object_id = '84502981-302e-415b-be52-e221edf1ffc5'
ORDER BY ts;
```

### Ergebnis

ts | actor | role | action | object_id | decision | reason | purpose | policy_version | details_json |
|---|---|---|---|---|---|---|---|---|---|
2026-03-09T18:56:15.094109+00:00 | user_2 | analyst | OBJECT_CREATED | 84502981-302e-415b-be52-e221edf1ffc5 |  |  | analytics | v1 | {"endpoint": "/objects", "method": "POST"} |

2026-03-09T18:57:12.914761+00:00 | user_2 | analyst | ACCESS_REQUESTED | 84502981-302e-415b-be52-e221edf1ffc5 | deny | purpose_mismatch | analytics | v1 | {"endpoint": "/access", "method": "POST", "requested_purpose": "billing", "object_purpose": "analytics"} |


---