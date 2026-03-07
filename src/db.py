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

def load_data_object(object_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT object_id, payload_json, purpose, policy_version
                   FROM data_objects
                   WHERE object_id = ?
                   """, (object_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return None
    payload = json.loads(row[1])
    result = {
        "object_id": row[0],
        "payload": payload,
        "purpose": row[2],
        "policy_version": row[3]
    }
    conn.close()
    return result