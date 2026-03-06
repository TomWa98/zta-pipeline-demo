from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException

from src.models import DataObjectCreate
from src.models import DataObjectCreated

app = FastAPI()

@app.post("/objects", response_model= DataObjectCreated)
def create_object(
    data: DataObjectCreate,
    x_actor: str = Header(...),
    x_role: str = Header(...)
    ):
    return DataObjectCreated(
    object_id="test-id",
    status="created"
)
