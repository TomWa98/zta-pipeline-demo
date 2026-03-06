import sqlite3              # Standardbibliothek zur Nutzung der SQLite-DB-API (PEP 249 kompatibel)
from pathlib import Path    # Plattformunabhängige, objektorientierte Repräsentation von Dateisystempfaden

# ---------------------------------------------------------
# Physische Persistenzdefinition
# ---------------------------------------------------------

DB_PATH = Path("data") / "demo.db"    # Speicherort der SQLite-Datei (repräsentiert die gesamte Datenbank)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)  
# Sicherstellen, dass das Verzeichnis existiert, bevor eine Verbindung aufgebaut wird
# (verhindert Laufzeitfehler bei nicht vorhandenem Ordner)

# ---------------------------------------------------------
# Initialisierungsskript für das Datenbankschema
# ---------------------------------------------------------

def main():
    # Verbindung zur SQLite-Datei herstellen
    # Falls die Datei nicht existiert, wird sie automatisch erzeugt
    conn = sqlite3.connect(DB_PATH)

    # Cursor-Objekt erzeugen, über das SQL-Befehle ausgeführt werden
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Tabelle: data_objects
    # Persistiert Policy-gebundene Datenobjekte (Flow 1)
    # ---------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_objects (
            object_id TEXT PRIMARY KEY,         -- eindeutige Objekt-ID (UUID)
            payload_json TEXT NOT NULL,         -- serialisierte Nutzdaten (JSON-String)
            purpose TEXT NOT NULL,              -- Zweckbindung des Objekts
            policy_version TEXT NOT NULL,       -- angewendete Policy-Version
            classification TEXT,                -- optionale Schutzbedarfsklassifikation
            owner TEXT,                         -- optionaler Verantwortlicher/Steward
            lineage_ref TEXT,                   -- optionale Referenz zur Herkunft
            created_at TEXT NOT NULL            -- ISO-8601 Timestamp der Erstellung
        );
    """)

    # ---------------------------------------------------------
    # Tabelle: audit_events (append-only)
    # Persistiert revisionsfähige Audit-Evidence (Flow 1 & 2)
    # ---------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_events (
            event_id TEXT PRIMARY KEY,          -- eindeutige Event-ID (UUID)
            ts TEXT NOT NULL,                   -- Zeitstempel des Ereignisses (ISO-8601)
            request_id TEXT NOT NULL,           -- korrelierende Request-ID
            actor TEXT NOT NULL,                -- aufrufende Identität (X-Actor)
            role TEXT NOT NULL,                 -- Rolle/Kontext (X-Role)
            action TEXT NOT NULL,               -- Aktionstyp (OBJECT_CREATED, ACCESS_REQUESTED)
            object_id TEXT,                     -- referenziertes Datenobjekt
            decision TEXT,                      -- allow/deny (nur bei Zugriff)
            reason TEXT,                        -- Begründung der Entscheidung
            purpose TEXT,                       -- Kontextzweck (object/requested purpose)
            policy_version TEXT,                -- verwendete Policy-Version
            details_json TEXT NOT NULL          -- zusätzliche strukturierte Kontextinformationen
        );
    """)

    # Änderungen dauerhaft in der SQLite-Datei speichern
    conn.commit()

    # Verbindung sauber schließen (verhindert File-Locks)
    conn.close()

    print(f"Database schema initialized at {DB_PATH}")  
    # Bestätigung, dass Persistenz und Schema erfolgreich angelegt wurden


# Entry-Point-Schutz:
# main() wird nur ausgeführt, wenn dieses Skript direkt gestartet wird.
# Beim Import als Modul erfolgt keine automatische Initialisierung.
if __name__ == "__main__":
    main()