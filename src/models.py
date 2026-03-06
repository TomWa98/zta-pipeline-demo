from pydantic import BaseModel
from typing import Optional    # erlaubt einen Typ oder None



# Request-Modell für POST /objects
# Repräsentiert ein DataObject gemäß Domänenmodell
class DataObjectCreate(BaseModel):
    payload: dict
    purpose: str
    policy_version: str
    classification: Optional[str] = None
    owner: Optional[str] = None
    lineage_ref: Optional[str] = None


# Output-Model für POST /objects
class DataObjectCreated(BaseModel):
    object_id: str
    status: str = "created"
