from fastapi import FastAPI, Header, HTTPException
from uuid import uuid4

# Persistenz- und Audit-Layer
from src.db import insert_data_object, load_data_object
from src.audit import write_audit_event
from src.policy import evaluate_policy

# Pydantic-Modelle für Request/Response
from src.models import DataObjectCreate, DataObjectCreated, AccessRequest, AccessAllowedResponse, AccessDeniedResponse

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


@app.post("/access", response_model = AccessAllowedResponse | AccessDeniedResponse)
def access_request( 
    data: AccessRequest,
    x_actor: str = Header(...),
    x_role: str = Header(...)
    ):
    request_id = str(uuid4())
    obj = load_data_object(data.object_id)
    if obj is None:
        raise HTTPException(status_code = 404, detail = "Object not found")
    decision = evaluate_policy(
        role = x_role,
        requested_purpose = data.requested_purpose,
        object_purpose = obj["purpose"],
        policy_version = obj["policy_version"]
    )
    write_audit_event(
        request_id = request_id,
        actor = x_actor,
        role = x_role,
        action = "ACCESS_REQUESTED",
        details = {
            "endpoint": "/access",
            "method": "POST",
            "requested_purpose": data.requested_purpose,
            "object_purpose": obj["purpose"]
        },
        object_id = obj["object_id"],
        decision = decision["decision"],
        reason = decision["reason"],
        purpose = obj["purpose"],
        policy_version = decision["policy_version"]
    )
    if decision["decision"] == "allow":
        return {
            "decision": "allow",
            "object_id": obj["object_id"],
            "payload": obj["payload"]
        }
    else:
        return {
            "decision": "deny",
            "object_id": obj["object_id"],
            "reason": decision["reason"]
        }