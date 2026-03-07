import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

from src.models import DataObjectCreate

DB_PATH = Path("data") / "demo.db"

def insert_data_object(object_id: str, data: DataObjectCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    payload_json = json.dumps(data.payload)
    created_at = datetime.now(timezone.utc).isoformat()
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
    conn.commit()
    conn.close()