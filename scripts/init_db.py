import sqlite3              # Standardbibliothek für SQLite-Datenbankzugriff
from pathlib import Path    # Objektorientierte, plattformunabhängige Pfadverwaltung

DB_PATH = Path("data") / "demo.db"    # Zielpfad der SQLite-Datenbankdatei definieren
DB_PATH.parent.mkdir(parents=True, exist_ok=True)    # Sicherstellen, dass das DB-Verzeichnis existiert

def main():
    conn = sqlite3.connect(DB_PATH)   # Verbindung zur SQLite-Datei öffnen (Datei wird ggf. erstellt)
    cursor = conn.cursor()            # Objekt, das SQL ausführt
    cursor.execute("""CREATE TABLE IF NOT EXISTS data_objects (
                  object_id TEXT PRIMARY KEY,
                  payload_json TEXT NOT NULL,
                  purpose TEXT NOT NULL,
                  policy_version TEXT NOT NULL,
                  classification TEXT,
                  owner TEXT,
                  lineage_ref TEXT,
                  created_at TEXT NOT NULL); 
                  """)                # data_objects Tabelle erstellen
    cursor.execute("""CREATE TABLE IF NOT EXISTS audit_events (
                   event_id TEXT PRIMARY KEY,
                   ts TEXT NOT NULL,
                   request_id TEXT NOT NULL,
                   actor TEXT NOT NULL,
                   role TEXT NOT NULL,
                   action TEXT NOT NULL,
                   object_id TEXT,
                   decision TEXT,
                   reason TEXT,
                   purpose TEXT,
                   policy_version TEXT,
                   details_json TEXT NOT NULL
                   );
                   """)
    conn.commit()                     # Transaktion abschließen (hier strukturell vorbereitet)
    conn.close()                      # Verbindung sauber schließen (File-Lock vermeiden)
    print(f"Database initialized at {DB_PATH}")  # Bestätigung der erfolgreichen Initialisierung

if __name__ == "__main__":
    main()                            # main() nur ausführen, wenn das Skript direkt gestartet wird