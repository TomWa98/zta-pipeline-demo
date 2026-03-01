# 00_scope.md — Scope & Abgrenzung

## Ziel der Instanziierung (Proof of Concept)

Ziel dieser Instanziierung ist die prototypische Demonstration ausgewählter Mechanismen meiner Zero-Trust-Referenzarchitektur. Der Prototyp dient als Proof of Concept im Rahmen einer Bachelorarbeit und stellt kein Produktivsystem dar.

Im Fokus stehen:
- Zweckbindung auf Datensatzebene (Purpose Enforcement)
- revisionsfähige Auditierbarkeit (Audit Evidence)

## Instanziierte Mechanismen (Was wird umgesetzt?)

Die Demo instanziiert folgende Bestandteile der Referenzarchitektur:

- DataObject als „Policy-Objekt“ mit Pflicht-Metadaten (u. a. purpose, policy_version)
- PEP (Policy Enforcement Point): Durchsetzung von Entscheidungen im API-Zugriffspfad
- PDP (Policy Decision Point): zweckbasierte Policy-Entscheidung (allow/deny + reason)
- Persistenz: Speicherung von Datenobjekten und Metadaten in SQLite
- Audit Store: Append-only Audit-Events zur Nachvollziehbarkeit von Zugriffen und Entscheidungen

## Nicht instanziierte Mechanismen (Out of Scope)

Folgende Bestandteile sind Teil der Referenzarchitektur, werden in dieser Demo jedoch bewusst nicht umgesetzt, um den Scope einer Bachelorarbeit nicht zu sprengen und die Nachweisführung zu fokussieren:

- Vollständiges Identity- und Access-Management (IAM/SSO), z. B. zentrale Authentifizierung/Autorisierung
- Externe Policy Engine als Service (z. B. OPA) und Policy-Verteilung über separate Komponenten
- Message Broker / Event Streaming (z. B. Kafka/NATS)
- Verschlüsselung, Key Management, Confidential Computing
- Skalierung/Deployment/High Availability, Monitoring/Alerting
- UI/Frontend (z. B. Admin-GUI)

## Annahmen

Für die Demo gelten folgende Annahmen, um die Implementierung schlank und reproduzierbar zu halten:

- Identität/Rollen werden als Header-Stub übermittelt (z. B. X-Actor, X-Role)
- SQLite wird als lokaler Speicher für Datenobjekte und Audit-Events verwendet
- Policies sind versionsgeführt (policy_version) und werden im Prototyp als Code/konfigurierbare Regeln abgebildet
- Der Prototyp wird lokal ausgeführt; Bedrohungsmodelle/Produktiv-Betrieb sind nicht Gegenstand der Demo

## Definition of Done (DoD)

Die Instanziierung gilt als erfolgreich, wenn folgende Kriterien erfüllt sind:

1. Ein Datenobjekt kann nur erstellt werden, wenn die Pflicht-Metadaten vollständig sind (mindestens purpose, policy_version).
2. Ein Zugriff auf ein Datenobjekt wird nur nach PDP-Entscheidung durch den PEP erlaubt oder verweigert (allow/deny).
3. Für Erstellen und Zugriffsanfragen werden Audit-Events geschrieben (append-only) und enthalten mindestens request_id, actor/role, action, object_id, decision, reason, policy_version.
4. Drei Validierungsszenarien sind dokumentiert und ausführbar:
   - Allow (Role + Purpose passend)
   - Deny (Purpose mismatch)
   - Deny (Role nicht berechtigt)
5. Die Nachweisführung ist möglich, indem die zugehörigen Audit-Events in der Datenbank sichtbar sind (Audit Evidence).