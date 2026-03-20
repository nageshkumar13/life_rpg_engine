from datetime import date, datetime

from pydantic import BaseModel, Field

from app.core.enums import BacklogStatus
from app.schemas.common import ORMModel
from app.schemas.task import TaskRead


class BacklogCreate(BaseModel):
    user_id: str | None = None
    title: str
    description: str | None = None
    importance_score: int = Field(default=1, ge=1, le=5)
    estimated_effort: int = Field(default=0, ge=0)
    xp_reward: int = Field(default=0, ge=0)


class BacklogUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    importance_score: int | None = Field(default=None, ge=1, le=5)
    estimated_effort: int | None = Field(default=None, ge=0)
    xp_reward: int | None = Field(default=None, ge=0)
    status: BacklogStatus | None = None


class BacklogAssignRequest(BaseModel):
    assigned_day: date


class BacklogRead(ORMModel):
    id: str
    user_id: str
    title: str
    description: str | None
    importance_score: int
    estimated_effort: int
    xp_reward: int
    status: BacklogStatus
    created_at: datetime
    updated_at: datetime


class BacklogAssignmentResponse(BaseModel):
    backlog: BacklogRead
    task: TaskRead
