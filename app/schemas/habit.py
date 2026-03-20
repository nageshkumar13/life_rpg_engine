from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import HabitUnitType
from app.schemas.common import ORMModel
from app.schemas.habit_log import HabitLogRead


class HabitCreate(BaseModel):
    user_id: str | None = None
    title: str
    description: str | None = None
    unit_type: HabitUnitType = HabitUnitType.MINUTES
    target_minutes: int = Field(default=0, ge=0)
    xp_base: int = Field(default=10, ge=0)


class HabitUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    unit_type: HabitUnitType | None = None
    target_minutes: int | None = Field(default=None, ge=0)
    xp_base: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class HabitRead(ORMModel):
    id: str
    user_id: str
    title: str
    description: str | None
    unit_type: HabitUnitType
    target_minutes: int
    xp_base: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    logs: list[HabitLogRead] = []
