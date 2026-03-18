from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.backlog_task import BacklogTask


class BacklogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, backlog: BacklogTask) -> BacklogTask:
        self.db.add(backlog)
        self.db.flush()
        return backlog

    def get(self, backlog_id: str) -> BacklogTask | None:
        return self.db.get(BacklogTask, backlog_id)

    def list_for_user(self, user_id: str) -> list[BacklogTask]:
        stmt = select(BacklogTask).where(BacklogTask.user_id == user_id).order_by(BacklogTask.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def delete(self, backlog: BacklogTask) -> None:
        self.db.delete(backlog)

