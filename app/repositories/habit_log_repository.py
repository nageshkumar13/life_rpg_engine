from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.habit_log import HabitLog


class HabitLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, log: HabitLog) -> HabitLog:
        self.db.add(log)
        self.db.flush()
        return log

    def get_for_day(self, habit_id: str, day: date) -> HabitLog | None:
        stmt = select(HabitLog).where(HabitLog.habit_id == habit_id, HabitLog.log_date == day)
        return self.db.scalar(stmt)

    def list_for_user_range(self, user_id: str, start_date: date, end_date: date) -> list[HabitLog]:
        stmt = select(HabitLog).where(HabitLog.user_id == user_id, HabitLog.log_date >= start_date, HabitLog.log_date <= end_date)
        return list(self.db.scalars(stmt).all())

