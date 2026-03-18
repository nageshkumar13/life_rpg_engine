from datetime import datetime

from pydantic import BaseModel

from app.core.enums import XPSourceType
from app.schemas.common import ORMModel


class XPLogRead(ORMModel):
    id: str
    user_id: str
    source_type: XPSourceType
    source_id: str
    xp_delta: int
    reason: str
    created_at: datetime


class XPLogListResponse(BaseModel):
    items: list[XPLogRead]

