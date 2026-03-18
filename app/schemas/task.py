from datetime import date, datetime

from pydantic import BaseModel, Field

from app.core.enums import TaskStatus, TaskType
from app.schemas.common import ORMModel
from app.schemas.task_chunk import TaskChunkRead


class TaskCreate(BaseModel):
    user_id: str
    title: str
    description: str | None = None
    type: TaskType = TaskType.PLANNED
    importance_score: int = Field(default=1, ge=1, le=5)
    estimated_minutes_total: int = Field(default=0, ge=0)
    assigned_day: date | None = None
    source_backlog_id: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    importance_score: int | None = Field(default=None, ge=1, le=5)
    estimated_minutes_total: int | None = Field(default=None, ge=0)
    assigned_day: date | None = None


class TaskRead(ORMModel):
    id: str
    user_id: str
    title: str
    description: str | None
    type: TaskType
    importance_score: int
    estimated_minutes_total: int
    assigned_day: date | None
    status: TaskStatus
    completion_percentage: float
    source_backlog_id: str | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    chunks: list[TaskChunkRead] = []


class TaskListResponse(BaseModel):
    items: list[TaskRead]

