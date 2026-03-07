import sqlite3
import json

from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

DB_PATH = Path("data") / "demo.db"

def write_audit_event(request_id: str, 
                      actor: str,
                      role: str,
                      action: str,
                      details: dict,
                      object_id: str | None = None,
                      decision: str | None = None,
                      reason: str | None = None,
                      purpose: str | None = None,
                      policy_version: str | None = None
                      ) -> None:
    event_id = str(uuid4())
    ts = datetime.now(timezone.utc).isoformat()
    details_json = json.dumps(details)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO audit_events (
                   event_id,
                   ts,
                   request_id,
                   actor,
                   role,
                   action,
                   object_id,
                   decision,
                   reason,
                   purpose,
                   policy_version,
                   details_json
                   ) VALUES (
                   ?,?,?,?,?,?,?,?,?,?,?,?)
                   """,
                   (
                       event_id,
                       ts,
                       request_id,
                       actor,
                       role,
                       action,
                       object_id,
                       decision,
                       reason,
                       purpose,
                       policy_version,
                       details_json
                   ))
    conn.commit()
    conn.close()