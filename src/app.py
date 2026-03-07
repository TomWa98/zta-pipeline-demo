from fastapi import FastAPI, Header
from uuid import uuid4

# Persistenz- und Audit-Layer
from src.db import insert_data_object
from src.audit import write_audit_event

# Pydantic-Modelle für Request/Response
from src.models import DataObjectCreate, DataObjectCreated

app = FastAPI()


# Endpoint für Flow 1: Erstellung eines DataObjects
@app.post("/objects", response_model=DataObjectCreated)
def create_object(
    data: DataObjectCreate,
    x_actor: str = Header(...),
    x_role: str = Header(...)
):
    # Jede API-Aktion bekommt eine eigene request_id für Audit-Zuordnung
    request_id = str(uuid4())

    # Systemgenerierte ID des DataObjects
    object_id = str(uuid4())

    # Persistenz des Objekts im Data Store
    insert_data_object(object_id, data)

    # Audit Evidence: Nachweis, dass ein Objekt erstellt wurde
    write_audit_event(
        request_id= request_id,
        actor= x_actor,
        role= x_role,
        action= "OBJECT_CREATED",
        details= {
            "endpoint": "/objects",
            "method": "POST"
        },
        object_id= object_id,
        purpose= data.purpose,
        policy_version= data.policy_version
    )

    # API Response an den Client
    return DataObjectCreated(
        object_id= object_id,
        status= "created"
    )