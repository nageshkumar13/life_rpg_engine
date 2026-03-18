from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.utils.datetime import utcnow


class DailyReview(Base):
    __tablename__ = "daily_review"
    __table_args__ = (UniqueConstraint("user_id", "review_date", name="uq_daily_review_day"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    review_date: Mapped[date] = mapped_column(Date, index=True)
    discipline_score: Mapped[int] = mapped_column(Integer, default=0)
    productivity_score: Mapped[int] = mapped_column(Integer, default=0)
    habit_score: Mapped[int] = mapped_column(Integer, default=0)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    planned_completed: Mapped[int] = mapped_column(Integer, default=0)
    planned_total: Mapped[int] = mapped_column(Integer, default=0)
    unplanned_completed: Mapped[int] = mapped_column(Integer, default=0)
    habit_completed: Mapped[int] = mapped_column(Integer, default=0)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

