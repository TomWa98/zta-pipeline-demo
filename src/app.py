from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException

from uuid import uuid4 
from src.db import insert_data_object
from src.audit import write_audit_event

from src.models import DataObjectCreate
from src.models import DataObjectCreated

app = FastAPI()

@app.post("/objects", response_model=DataObjectCreated)
def create_object(
    data: DataObjectCreate,
    x_actor: str = Header(...),
    x_role: str = Header(...)
    ):
    request_id = str(uuid4())
    object_id = str(uuid4())

    insert_data_object(object_id, data)
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

    return DataObjectCreated(
        object_id = object_id,
        status= "created"
    )
