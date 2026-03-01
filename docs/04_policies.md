# 04_policies.md — Policy-Definition (PDP-Regeln)

## Zweck dieses Dokuments

Dieses Dokument definiert die formalen Entscheidungsregeln (Policies) der Demo.
Die Regeln werden im Policy Decision Point (PDP) umgesetzt (src/policy.py).

Ziel ist eine deterministische Entscheidungslogik.

---

## 1) Policy-Version

Aktive Policy-Version:

policy_version = "v1"

Die Policy-Version wird:

- im DataObject gespeichert
- bei jeder Policy-Entscheidung zurückgegeben
- in jedem Audit-Event persistiert

---

## 2) Unterstützte Action

In der Demo existiert genau eine Action:

- read

Die Action "read" wird implizit bei POST /access verwendet.
Weitere Actions (z. B. share, delete) sind nicht Teil des Scopes.

---

## 3) Entscheidungsinput (PDP-Input)

Die Policy-Entscheidung basiert auf:

- role (aus X-Role Header)
- requested_purpose (aus Request Body)
- object_purpose (aus data_objects.purpose)
- policy_version (aus data_objects.policy_version)

---

## 4) Entscheidungsregeln (Policy v1)

Regel 1 — Analyst

Wenn:
- role == "analyst"
- requested_purpose == "analytics"
- object_purpose == "analytics"

Dann:
- decision = "allow"
- reason = "role_and_purpose_match"

Andernfalls:
- decision = "deny"
- reason = "purpose_mismatch"

---

Regel 2 — Support

Wenn:
- role == "support"
- requested_purpose == "support"
- object_purpose == "support"

Dann:
- decision = "allow"
- reason = "role_and_purpose_match"

Andernfalls:
- decision = "deny"
- reason = "purpose_mismatch"

---

Regel 3 — Guest

Wenn:
- role == "guest"

Dann:
- decision = "deny"
- reason = "role_not_allowed"

Unabhängig vom Purpose.

---

Regel 4 — Unbekannte Rolle

Wenn:
- role nicht in ["analyst", "support", "guest"]

Dann:
- decision = "deny"
- reason = "role_not_allowed"

---

## 5) Entscheidungsoutput (Standard)

Jede Policy-Entscheidung liefert exakt folgende Struktur zurück:

```json
{
  "decision": "allow" | "deny",
  "reason": "role_and_purpose_match" | "purpose_mismatch" | "role_not_allowed",
  "policy_version": "v1"
}
```

Diese Struktur wird:

- vom PEP (src/app.py) ausgewertet
- in audit_events gespeichert
- an den Client zurückgegeben

---

## 6) Konsistenz mit anderen Dokumenten

- Flow 2 (POST /access) ruft diese Policy auf.
- decision, reason und policy_version werden in audit_events gespeichert.
- Bei decision == "deny" wird kein payload zurückgegeben.
- Auch denied Zugriffe erzeugen ein ACCESS_REQUESTED Audit-Event.

---

## 7) Nicht Teil der Policy

Nicht implementiert in v1:

- Feld-basierte Maskierung
- Attribut-basierte Zugriffskontrolle (ABAC)
- Zeitbasierte Regeln
- Ausnahme-/Freigabeprozesse
- Policy-Verteilung über externe Services (z. B. OPA)

Die Policy ist bewusst minimal gehalten, um Zweckbindung technisch nachzuweisen.
