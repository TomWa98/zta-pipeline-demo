# 00_scope.md — Scope & Abgrenzung

## Ziel der Instanziierung (Proof of Concept)

Ziel dieser Instanziierung ist die prototypische Demonstration ausgewählter Mechanismen meiner Zero-Trust-Referenzarchitektur. Der Prototyp dient als Proof of Concept im Rahmen einer Bachelorarbeit und stellt kein Produktivsystem dar.

Im Fokus stehen:
- Zweckbindung auf Datensatzebene (Purpose Enforcement)
- revisionsfähige Auditierbarkeit (Audit Evidence)


## Einordnung der Instanziierung in die Referenzarchitektur

Die vorliegende Demo instanziiert bewusst nur einen abgegrenzten Teil der entwickelten Zero-Trust-Referenzarchitektur. Ziel ist die Demonstration der funktionalen Umsetzbarkeit zentraler Zero-Trust-Kontrollmechanismen auf Datenobjektebene, nicht die vollständige technische Umsetzung aller Architekturkomponenten.

### Instanziierte Ebenen und Komponenten

**Control Plane (Zero-Trust-Kontrollschicht)**

- Policy Decision Point (PDP)  
  → kontextbasierte Entscheidungslogik (zweckbasierte Regeln)

- Policy Enforcement Point (PEP)  
  → Durchsetzung von allow/deny-Entscheidungen im Zugriffspfad

- Audit & Evidence Log  
  → revisionsfähige Protokollierung von Zugriffen und Entscheidungen

Diese Komponenten bilden den Kern der Zero-Trust-Kontrolllogik und stehen im Zentrum der Demonstration.

**Data Plane (Datenverarbeitung – reduziert)**

- Speicherung von Datenobjekten inkl. Pflicht-Metadaten  
- Zweckbasierte Zugriffskontrolle auf gespeicherte Daten  
- Nachweis der Policy-Entscheidungen über Audit-Einträge

Die Demo bildet damit einen vertikalen „Control Slice“ über einen reduzierten Datenpfad (Ingestion → Zugriff), ohne die vollständige Datenzonen-Architektur umzusetzen.

---

### Nicht instanziierte Ebenen und Komponenten

Folgende Bestandteile der Referenzarchitektur sind bewusst nicht Teil der Instanziierung:

**Governance Plane**

- Policy Management (zentrale Regelverwaltung)
- Stewardship & Responsibility
- Exception & Approval Handling

Diese Governance-Mechanismen werden konzeptionell berücksichtigt, jedoch nicht als separate organisatorische oder technische Services implementiert.

**Control Plane (erweitert)**

- Identity & Context Provider (IAM/SSO, Token-basierte Authentifizierung)
- Data Classification & Purpose Registry als eigenständiger Service
- Lineage & Provenance Service
- Externe Policy Engine (z. B. OPA) inkl. verteilter Policy-Ausführung

In der Demo werden Identität und Rollen über einen vereinfachten Header-Stub simuliert; Policies sind lokal implementiert.

**Data Plane (erweitert)**

- Mehrzonen-Architektur (Ingestion, Processing, Storage, Usage als getrennte Umgebungen)
- Trust Boundaries T1–T3 als infrastrukturelle Trennung
- Message Broker / Event Streaming

**Querschnittliche Sicherheitsmechanismen**

- Verschlüsselung (at rest / in transit)
- Key Management (z. B. KMS/HSM)
- Confidential Computing

Diese Mechanismen betreffen die infrastrukturelle Absicherung der Datenverarbeitung, nicht jedoch die logische Zweckdurchsetzung auf Datenobjektebene und sind daher nicht Gegenstand der Demonstration.

**Betriebs- und Infrastrukturebene**

- Skalierung, High Availability
- Monitoring & Alerting
- Deployment-Architektur
- Administrative UI

---

### Begründung der Reduktion

Die Instanziierung fokussiert ausschließlich die funktionale Kernthese der Referenzarchitektur:

> Zweckbindung und Zero-Trust-Kontrolllogik können auf Datenobjektebene technisch durchgesetzt und revisionsfähig nachgewiesen werden.

Infrastruktur-, Governance- und kryptographische Absicherungsmechanismen sind Bestandteil der vollständigen Referenzarchitektur, jedoch nicht notwendig, um diese Kernthese im Rahmen einer Bachelorarbeit nachzuweisen.

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