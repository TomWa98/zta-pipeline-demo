from pydantic import BaseModel
from typing import Optional, Literal    # erlaubt einen Typ oder None




# Request-Modell für POST /objects
# Repräsentiert ein DataObject gemäß Domänenmodell
class DataObjectCreate(BaseModel):
    payload: dict
    purpose: str
    policy_version: str
    classification: Optional[str] = None
    owner: Optional[str] = None
    lineage_ref: Optional[str] = None


# Response-Modell für POST /objects
class DataObjectCreated(BaseModel):
    object_id: str
    status: str = "created"


# Request-Modell für POST /access
class AccessRequest(BaseModel):
    object_id: str
    requested_purpose: str

# Response-Modell für POST /access
class AccessAllowedResponse(BaseModel):
    decision: Literal["allow"]
    object_id: str
    payload: dict


# Response-Modell für POST /access
class AccessDeniedResponse(BaseModel):
    decision: Literal["deny"]
    object_id: str
    reason: str