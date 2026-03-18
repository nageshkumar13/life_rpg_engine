from datetime import date

from sqlalchemy.orm import Session

from app.core.enums import TaskStatus
from app.core.exceptions import NotFoundError, ValidationError
from app.models.task import Task
from app.models.task_chunk import TaskChunk
from app.repositories.task_chunk_repository import TaskChunkRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.task_chunk import TaskChunkCreate, TaskChunkUpdate
from app.services.task_progress_service import TaskProgressService
from app.utils.ids import new_id


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)
        self.chunk_repository = TaskChunkRepository(db)
        self.progress_service = TaskProgressService(db)

    def create_task(self, payload: TaskCreate) -> Task:
        task = Task(id=new_id(), **payload.model_dump())
        self.task_repository.create(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: str) -> Task:
        task = self.task_repository.get(task_id)
        if not task:
            raise NotFoundError("Task not found")
        return task

    def get_tasks_for_day(self, user_id: str, day: date) -> list[Task]:
        return self.task_repository.list_by_date(user_id, day)

    def list_tasks_by_date(self, user_id: str, day: date) -> list[Task]:
        return self.task_repository.list_by_date(user_id, day)

    def update_task(self, task_id: str, payload: TaskUpdate) -> Task:
        task = self.get_task(task_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.task_repository.update(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        self.task_repository.delete(task)
        self.db.commit()

    def mark_active(self, task_id: str) -> Task:
        task = self.get_task(task_id)
        if task.status != TaskStatus.PLANNED:
            raise ValidationError("Only planned tasks can be marked active")
        task.status = TaskStatus.ACTIVE
        self.task_repository.update(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def mark_done(self, task_id: str) -> Task:
        task = self.progress_service.mark_task_done(task_id)
        self.db.commit()
        self.db.refresh(task)
        return task

    def mark_missed(self, task_id: str) -> Task:
        task = self.get_task(task_id)
        if task.status not in {TaskStatus.PLANNED, TaskStatus.ACTIVE}:
            raise ValidationError("Only planned or active tasks can be marked missed")
        task.status = TaskStatus.MISSED
        self.task_repository.update(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def add_chunk(self, task_id: str, payload: TaskChunkCreate) -> TaskChunk:
        task = self.get_task(task_id)
        chunk = TaskChunk(id=new_id(), task_id=task.id, **payload.model_dump())
        self.chunk_repository.create(chunk)
        self.progress_service.recalculate_task_progress(task)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def update_chunk(self, task_id: str, chunk_id: str, payload: TaskChunkUpdate) -> TaskChunk:
        task = self.get_task(task_id)
        chunk = self.chunk_repository.get(chunk_id)
        if not chunk or chunk.task_id != task.id:
            raise NotFoundError("Chunk not found")
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(chunk, field, value)
        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def mark_chunk_done(self, task_id: str, chunk_id: str, actual_minutes: int | None = None) -> Task:
        task = self.progress_service.mark_chunk_done(task_id, chunk_id, actual_minutes)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_chunk(self, task_id: str, chunk_id: str) -> None:
        task = self.get_task(task_id)
        chunk = self.chunk_repository.get(chunk_id)
        if not chunk or chunk.task_id != task.id:
            raise NotFoundError("Chunk not found")
        self.chunk_repository.delete(chunk)
        self.progress_service.recalculate_task_progress(task)
        self.db.commit()
