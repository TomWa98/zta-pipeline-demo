import sqlite3              # Standardbibliothek für SQLite-Datenbankzugriff
from pathlib import Path    # Objektorientierte, plattformunabhängige Pfadverwaltung

DB_PATH = Path("data") / "demo.db"    # Zielpfad der SQLite-Datenbankdatei definieren
DB_PATH.parent.mkdir(parents=True, exist_ok=True)    # Sicherstellen, dass das DB-Verzeichnis existiert

def main():
    conn = sqlite3.connect(DB_PATH)   # Verbindung zur SQLite-Datei öffnen (Datei wird ggf. erstellt)
    conn.commit()                     # Transaktion abschließen (hier strukturell vorbereitet)
    conn.close()                      # Verbindung sauber schließen (File-Lock vermeiden)
    print(f"Database initialized at {DB_PATH}")  # Bestätigung der erfolgreichen Initialisierung

if __name__ == "__main__":
    main()                            # main() nur ausführen, wenn das Skript direkt gestartet wird