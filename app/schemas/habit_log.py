from datetime import date, datetime

from pydantic import BaseModel, Field

from app.core.enums import HabitLogStatus
from app.schemas.common import ORMModel


class HabitLogCreate(BaseModel):
    log_date: date
    actual_minutes: int = Field(default=0, ge=0)


class HabitLogRead(ORMModel):
    id: str
    habit_id: str
    user_id: str
    log_date: date
    actual_minutes: int
    xp_earned: int
    status: HabitLogStatus
    streak_after_log: int
    created_at: datetime

