from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException

from uuid import uuid4 

from src.models import DataObjectCreate
from src.models import DataObjectCreated

app = FastAPI()

@app.post("/objects", response_model= DataObjectCreated)
def create_object(
    data: DataObjectCreate,
    x_actor: str = Header(...),
    x_role: str = Header(...)
    ):
    
    object_id = str(uuid4())

    return DataObjectCreated(
        object_id = object_id,
        status= "created"
    )
