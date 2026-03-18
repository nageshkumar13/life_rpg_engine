from datetime import datetime

from pydantic import BaseModel

from app.core.enums import ChunkStatus
from app.schemas.common import ORMModel


class TaskChunkCreate(BaseModel):
    title: str
    estimated_minutes: int = 0
    order_index: int = 0


class TaskChunkUpdate(BaseModel):
    title: str | None = None
    estimated_minutes: int | None = None
    actual_minutes: int | None = None
    order_index: int | None = None


class TaskChunkRead(ORMModel):
    id: str
    task_id: str
    title: str
    estimated_minutes: int
    actual_minutes: int | None
    xp_earned: int
    status: ChunkStatus
    order_index: int
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

