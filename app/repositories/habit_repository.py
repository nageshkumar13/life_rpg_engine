from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.habit import Habit


class HabitRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, habit: Habit) -> Habit:
        self.db.add(habit)
        self.db.flush()
        return habit

    def get(self, habit_id: str) -> Habit | None:
        stmt = select(Habit).options(selectinload(Habit.logs)).where(Habit.id == habit_id)
        return self.db.scalar(stmt)

    def list_for_user(self, user_id: str, active_only: bool = False) -> list[Habit]:
        stmt = select(Habit).options(selectinload(Habit.logs)).where(Habit.user_id == user_id)
        if active_only:
            stmt = stmt.where(Habit.is_active.is_(True))
        return list(self.db.scalars(stmt.order_by(Habit.created_at.desc())).all())

