import sqlite3
import json

from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

# SQLite-Datei für Data Store und Audit Log
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
    
    # Eindeutige Event-ID für das Audit-Event
    event_id = str(uuid4())

    # Zeitpunkt des Ereignisses (UTC)
    ts = datetime.now(timezone.utc).isoformat()

    # Zusatzinformationen werden als JSON gespeichert
    details_json = json.dumps(details)

    # Verbindung zur Audit-Tabelle
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Append-only Audit Log
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
    
    # Event dauerhaft speichern und Verbindung schließen
    conn.commit()
    conn.close()