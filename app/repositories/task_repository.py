from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.flush()
        return task

    def get(self, task_id: str) -> Task | None:
        stmt = select(Task).options(selectinload(Task.chunks)).where(Task.id == task_id)
        return self.db.scalar(stmt)

    def list_by_date(self, user_id: str, day: date) -> list[Task]:
        stmt = (
            select(Task)
            .options(selectinload(Task.chunks))
            .where(Task.user_id == user_id, Task.assigned_day == day)
            .order_by(Task.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def list_range(self, user_id: str, start_date: date, end_date: date) -> list[Task]:
        stmt = (
            select(Task)
            .options(selectinload(Task.chunks))
            .where(Task.user_id == user_id, Task.assigned_day >= start_date, Task.assigned_day <= end_date)
        )
        return list(self.db.scalars(stmt).all())

    def update(self, task: Task) -> Task:
        self.db.add(task)
        self.db.flush()
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)

