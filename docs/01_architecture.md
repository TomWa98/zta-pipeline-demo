# 01_architecture.md — Architektur-Mapping (Referenzmodell → Instanziierung)

## Zweck dieses Dokuments

Dieses Dokument beschreibt die strukturelle Abbildung der Zero-Trust-Referenzarchitektur auf die konkrete Demo-Implementierung.

Ziel ist eine eindeutige Zuordnung:
Jede Code-Komponente besitzt eine klar definierte Rolle im Referenzmodell (PDP, PEP, Audit etc.).

Dieses Dokument ist normativ für die weitere Implementierung.

---

## Logische Architektur der Demo
```text
+----------------------------+
| Client / Fachanwendung     |
| Header: X-Actor, X-Role    |
+-------------+--------------+
              |
              v
+--------------------------------------+
| FastAPI Anwendung (PEP)             |
| - POST /objects                     |
| - POST /access                      |
| - setzt Policy-Entscheidung durch   |
| - schreibt Audit-Ereignisse         |
+---------------+----------------------+
                |
                v
        +----------------------+
        | policy.py (PDP)      |
        | - zweckbasierte      |
        |   Entscheidungslogik |
        +-----------+----------+
                    |
                    v
+--------------------------------------+
| SQLite                              |
| - data_objects                      |
| - audit_events (append-only)        |
+--------------------------------------+
```

Hinweis:
Die Demo instanziiert die zentrale Kontrolllogik (PDP/PEP/Audit), jedoch nicht die vollständigen Governance-, Infrastruktur- oder Kryptographie-Mechanismen der Referenzarchitektur.

---

## Mapping: Referenzarchitektur → Demo-Komponenten

| Ebene (Referenzmodell) | Komponente (Referenzarchitektur) | Demo-Entsprechung | Code / Artefakt |
|------------------------|----------------------------------|-------------------|-----------------|
| Governance Plane | Policy Management | nicht instanziiert (konzeptionell beschrieben) | docs/04_policies.md |
| Governance Plane | Stewardship & Responsibility | nicht instanziiert | docs/00_scope.md |
| Governance Plane | Exception & Approval Handling | nicht instanziiert | docs/00_scope.md |
| Control Plane | Policy Decision Point (PDP) | lokales Policy-Modul | src/policy.py |
| Control Plane | Policy Enforcement Point (PEP) | API-Durchsetzung im Zugriffspfad | src/app.py |
| Control Plane | Audit & Evidence Log | append-only Audit-Tabelle | src/audit.py + SQLite |
| Control Plane | Identity & Context Provider | Header-Stub (X-Actor, X-Role) | src/app.py |
| Control Plane | Data Classification & Purpose Registry | Pflicht-Metadaten im DataObject | src/models.py |
| Control Plane | Lineage & Provenance Service | nicht instanziiert (optional als Feld) | docs/03_data_model.md |
| Data Plane | Ingestion Zone | Erstellung eines Datenobjekts | POST /objects |
| Data Plane | Storage Zone | SQLite Persistenz | src/db.py |
| Data Plane | Usage Zone | Zugriff auf Datenobjekt | POST /access |
| Data Plane | Trust Boundaries T1–T3 | nicht instanziiert | docs/00_scope.md |

---

## Architekturentscheidungen

SQLite als Persistenz- und Audit-Speicher
→ Minimiert Setup-Komplexität und ermöglicht reproduzierbare lokale Ausführung.

PDP als lokales Python-Modul
→ Keine externe Policy Engine (z. B. OPA), um Komplexität zu reduzieren.

Identitätskontext über Header-Stub
→ IAM/SSO ist nicht Teil der Instanziierung.

Audit als append-only Tabelle
→ Revisionsfähigkeit wird technisch erzwungen.

Kein Message Broker / kein Event Streaming
→ Synchrone Flows sind ausreichend für den Proof of Concept.

---

## Konsequenz für die Code-Struktur

src/app.py → PEP + API-Flows

src/policy.py → PDP (Entscheidungslogik)

src/models.py → DataObject + Pflicht-Metadaten

src/db.py → Persistenz

src/audit.py → Audit-Logik

scripts/init_db.py → reproduzierbares Datenbankschema