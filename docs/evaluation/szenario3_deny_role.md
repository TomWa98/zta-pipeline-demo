# Szenario 3 — Deny (Role Not Allowed)

## Ziel der Evaluation

Die folgenden Szenarien überprüfen die korrekte Durchsetzung der
Policy-Entscheidungen sowie die revisionsfähige Protokollierung
im Audit Log gemäß dem in docs/05_evaluation.md definierten Evidence Plan.

## Kontext

Rolle: guest  
requested_purpose: analytics  
object_purpose: analytics  

Erwartung: Zugriff wird verweigert, da die Rolle grundsätzlich nicht zugriffsberechtigt ist.

---

## Request — POST /objects

### Header

```text
X-Actor: user_3
X-Role: guest
```

### Body

```json
{
  "payload": {
    "report_id": "R-999",
    "value": 123
  },
  "purpose": "analytics",
  "policy_version": "v1"
}
```

---

## Response — POST /objects

```json
{
  "object_id": "e35e605b-d976-4bcb-af51-7acd141c8ea4",
  "status": "created"
}
```

---

## Request — POST /access

### Header

```text
X-Actor: user_3
X-Role: guest
```

### Body

```json
{
  "object_id": "e35e605b-d976-4bcb-af51-7acd141c8ea4",
  "requested_purpose": "analytics"
}
```

---

## Response — POST /access

```json
{
  "decision": "deny",
  "object_id": "e35e605b-d976-4bcb-af51-7acd141c8ea4",
  "reason": "role_not_allowed"
}
```

Hinweis: Auch bei übereinstimmendem Zweck wird der Zugriff verweigert, da die Rolle `guest` nicht zugriffsberechtigt ist.

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
WHERE object_id = 'e35e605b-d976-4bcb-af51-7acd141c8ea4'
ORDER BY ts;
```

### Ergebnis

ts | actor | role | action | object_id | decision | reason | purpose | policy_version | details_json |
|---|---|---|---|---|---|---|---|---|---|
2026-03-09T20:33:49.726353+00:00 | user_3 | guest | OBJECT_CREATED | e35e605b-d976-4bcb-af51-7acd141c8ea4 |  |  | analytics | v1 | {"endpoint": "/objects", "method": "POST"} |

2026-03-09T20:34:12.220439+00:00 | user_3 | guest | ACCESS_REQUESTED | e35e605b-d976-4bcb-af51-7acd141c8ea4 | deny | role_not_allowed | analytics | v1 | {"endpoint": "/access", "method": "POST", "requested_purpose": "analytics", "object_purpose": "analytics"} |

