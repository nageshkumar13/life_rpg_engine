from datetime import date

from sqlalchemy.orm import Session

from app.core.enums import BacklogStatus, TaskType
from app.core.exceptions import NotFoundError
from app.models.backlog_task import BacklogTask
from app.repositories.backlog_repository import BacklogRepository
from app.schemas.backlog import BacklogCreate, BacklogUpdate
from app.schemas.task import TaskCreate
from app.services.task_service import TaskService
from app.utils.ids import new_id


class BacklogService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.backlog_repository = BacklogRepository(db)
        self.task_service = TaskService(db)

    def create_backlog(self, payload: BacklogCreate) -> BacklogTask:
        backlog = BacklogTask(id=new_id(), **payload.model_dump())
        self.backlog_repository.create(backlog)
        self.db.commit()
        self.db.refresh(backlog)
        return backlog

    def list_backlog(self, user_id: str) -> list[BacklogTask]:
        return self.backlog_repository.list_for_user(user_id)

    def get_backlog(self, backlog_id: str) -> BacklogTask:
        backlog = self.backlog_repository.get(backlog_id)
        if not backlog:
            raise NotFoundError("Backlog item not found")
        return backlog

    def update_backlog(self, backlog_id: str, payload: BacklogUpdate) -> BacklogTask:
        backlog = self.get_backlog(backlog_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(backlog, field, value)
        self.db.add(backlog)
        self.db.commit()
        self.db.refresh(backlog)
        return backlog

    def delete_backlog(self, backlog_id: str) -> None:
        backlog = self.get_backlog(backlog_id)
        self.backlog_repository.delete(backlog)
        self.db.commit()

    def assign_to_day(self, backlog_id: str, assigned_day: date) -> tuple[BacklogTask, object]:
        backlog = self.get_backlog(backlog_id)
        task = self.task_service.create_task(
            TaskCreate(
                user_id=backlog.user_id,
                title=backlog.title,
                description=backlog.description,
                type=TaskType.BACKLOG,
                importance_score=backlog.importance_score,
                estimated_minutes_total=backlog.estimated_effort,
                assigned_day=assigned_day,
                source_backlog_id=backlog.id,
            )
        )
        backlog.status = BacklogStatus.ASSIGNED
        self.db.add(backlog)
        self.db.commit()
        self.db.refresh(backlog)
        return backlog, task

