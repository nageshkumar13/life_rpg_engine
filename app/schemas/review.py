from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class DailyReviewRead(ORMModel):
    id: str
    user_id: str
    review_date: date
    discipline_score: int
    productivity_score: int
    habit_score: int
    xp_earned: int
    planned_completed: int
    planned_total: int
    unplanned_completed: int
    habit_completed: int
    remark: str | None
    created_at: datetime


class DailyReviewListResponse(BaseModel):
    items: list[DailyReviewRead]

