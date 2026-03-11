# Szenario 1 — Allow

## Ziel der Evaluation

Die folgenden Szenarien überprüfen die korrekte Durchsetzung der
Policy-Entscheidungen sowie die revisionsfähige Protokollierung
im Audit Log gemäß dem in docs/05_evaluation.md definierten Evidence Plan.

## Request — POST /objects

Header
X-Actor: user_1
X-Role: analyst

Body

```json
{
  "payload": {
    "report_id": "R-001",
    "value": 42
  },
  "purpose": "analytics",
  "policy_version": "v1"
}
```

## Response — POST /objects

```json
{
  "object_id": "3b7ab373-cfe2-49dd-8710-828d60229191",
  "status": "created"
}
```

## Request — POST /access

```json
{
  "object_id": "3b7ab373-cfe2-49dd-8710-828d60229191",
  "requested_purpose": "analytics"
}
```

## Response — POST /access

```json
{
  "decision": "allow",
  "object_id": "3b7ab373-cfe2-49dd-8710-828d60229191",
  "payload": {
    "report_id": "R-001",
    "value": 42
  }
}
```

## Audit Evidence

```sql

SELECT ts, actor, role, action, object_id, decision, reason, purpose, policy_version, details_json
FROM audit_events
WHERE object_id = '3b7ab373-cfe2-49dd-8710-828d60229191' 
ORDER BY ts;
``` 

Ergebnis

ts | actor | role | action | object_id | decision | reason | purpose | policy_version | details_json |
|---|---|---|---|---|---|---|---|---|---|
2026-03-09T18:05:55.886686+00:00|user_1|analyst|OBJECT_CREATED|3b7ab373-cfe2-49dd-8710-828d60229191|||analytics|v1|{"endpoint": "/objects", "method": "POST"} |
2026-03-09T18:08:28.964457+00:00|user_1|analyst|ACCESS_REQUESTED|3b7ab373-cfe2-49dd-8710-828d60229191|allow|role_and_purpose_match|analytics|v1|{"endpoint": "/access", "method": "POST", "requested_purpose": "analytics", "object_purpose": "analytics"} |




