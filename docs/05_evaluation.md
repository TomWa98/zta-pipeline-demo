evaluation_md = """
# 05_evaluation.md — Evaluation (Evidence Plan)

## Zweck dieses Dokuments

Dieses Dokument definiert die Evaluationsszenarien der Demo.

Ziel ist der formale Nachweis, dass:

- Zweckbindung technisch durchgesetzt wird (Policy Enforcement)
- jede relevante Aktion revisionsfähig protokolliert wird (Audit Evidence)

Die Evaluation erfolgt anhand von drei definierten Szenarien.

---

# Szenario 1 — Allow

## Kontext

Rolle: analyst  
requested_purpose: analytics  
object_purpose: analytics  

Erwartung: Zugriff wird erlaubt.

---

## Schritt 1 — Objekt erstellen

Request:

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

Erwartete HTTP Response (201 oder 200):

```json
{
  "object_id": "<generated_id>",
  "status": "created"
}
```

Erwartetes Audit Event:

- action = OBJECT_CREATED
- object_id gesetzt
- purpose = analytics
- policy_version = v1

---

## Schritt 2 — Zugriff anfragen

Header:
- X-Actor: user_1
- X-Role: analyst

Request:

```json
{
  "object_id": "<generated_id>",
  "requested_purpose": "analytics"
}
```

Erwartete HTTP Response:

```json
{
  "decision": "allow",
  "object_id": "<generated_id>",
  "payload": {
    "report_id": "R-001",
    "value": 42
  }
}
```

Erwartetes Audit Event:

- action = ACCESS_REQUESTED
- decision = allow
- reason = role_and_purpose_match
- actor = user_1
- role = analyst
- object_id gesetzt
- policy_version = v1

---

# Szenario 2 — Deny (Purpose Mismatch)

## Kontext

Rolle: analyst  
requested_purpose: billing  
object_purpose: analytics  

Erwartung: Zugriff wird verweigert.

---

## Schritt 1 — Objekt erstellen

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

Erwartetes Audit Event:
- action = OBJECT_CREATED
- purpose = analytics

---

## Schritt 2 — Zugriff anfragen

Header:
- X-Actor: user_2
- X-Role: analyst

```json
{
  "object_id": "<generated_id>",
  "requested_purpose": "billing"
}
```

Erwartete HTTP Response:

```json
{
  "decision": "deny",
  "object_id": "<generated_id>",
  "reason": "purpose_mismatch"
}
```

Erwartetes Audit Event:

- action = ACCESS_REQUESTED
- decision = deny
- reason = purpose_mismatch
- actor = user_2
- role = analyst
- policy_version = v1

Kein payload darf im Response enthalten sein.

---

# Szenario 3 — Deny (Role Not Allowed)

## Kontext

Rolle: guest  
requested_purpose: analytics  
object_purpose: analytics  

Erwartung: Zugriff wird grundsätzlich verweigert.

---

## Schritt 1 — Objekt erstellen

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

## Schritt 2 — Zugriff anfragen

Header:
- X-Actor: user_3
- X-Role: guest

```json
{
  "object_id": "<generated_id>",
  "requested_purpose": "analytics"
}
```

Erwartete HTTP Response:

```json
{
  "decision": "deny",
  "object_id": "<generated_id>",
  "reason": "role_not_allowed"
}
```

Erwartetes Audit Event:

- action = ACCESS_REQUESTED
- decision = deny
- reason = role_not_allowed
- actor = user_3
- role = guest
- policy_version = v1

---

# Erfolgskriterien (Definition of Done)

Die Demonstration gilt als erfolgreich, wenn:

1. Szenario 1 ergibt allow.
2. Szenario 2 ergibt deny (purpose_mismatch).
3. Szenario 3 ergibt deny (role_not_allowed).
4. Für jede Aktion existiert ein Audit-Event.
5. decision, reason und policy_version sind korrekt in audit_events gespeichert.

Damit ist Zweckbindung und Auditierbarkeit technisch nachgewiesen.
"""