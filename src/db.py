import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

from src.models import DataObjectCreate

# Zentrale SQLite-Datei der Demo
DB_PATH = Path("data") / "demo.db"

def insert_data_object(object_id: str, data: DataObjectCreate) -> None:
    # Verbindung zur SQLite-Datenbank öffnen
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Payload wird als JSON-String gespeichert
    payload_json = json.dumps(data.payload)

    # Systemseitiger Zeitstempel der Erstellung
    created_at = datetime.now(timezone.utc).isoformat()

    # Persistenz des DataObjects im data_objects Store
    cursor.execute(""" INSERT INTO data_objects (
                   object_id, 
                   payload_json,
                   purpose,
                   policy_version,
                   classification,
                   owner,
                   lineage_ref,
                   created_at
                   ) 
                   VALUES
                   (?,?,?,?,?,?,?,?)
                   """,
                   (object_id,
                    payload_json,
                    data.purpose,
                    data.policy_version,
                    data.classification,
                    data.owner,
                    data.lineage_ref,
                    created_at))
    
    # Transaktion abschließen und Verbindung schließen
    conn.commit()
    conn.close()


# Lädt ein Datenobjekt anhand der objet_id aus der SQLite-Datenbank
def load_data_object(object_id: str):
    # Verbindung zur SQLite-Datenbank öffnen
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # SQL-Abfrage: DataObject anhand der object_id laden
    cursor.execute("""SELECT object_id, payload_json, purpose, policy_version
                   FROM data_objects
                   WHERE object_id = ?
                   """, (object_id,))
    
    # Erstes Objekt der Abfrage lesen (Primary Key -> max. eine Zeile)
    row = cursor.fetchone()

    # Wenn kein Datenobjekt gefunden wurde -> None zurückgeben
    if row is None:
        conn.close()
        return None
    
    # JSON-String aus der DB wieder in ein Python-Objekt umwandeln
    payload = json.loads(row[1])

    # Python-Dict für den Rückgabewert der Funktion bauen
    result = {
        "object_id": row[0],
        "payload": payload,
        "purpose": row[2],
        "policy_version": row[3]
    }

    # Verbindung schließen und Ergebnisobjekt zurückgeben
    conn.close()
    return result