from sqlalchemy.orm import Session

from app.core.enums import ChunkStatus, TaskStatus, XPSourceType
from app.core.exceptions import NotFoundError, ValidationError
from app.models.task import Task
from app.repositories.task_chunk_repository import TaskChunkRepository
from app.repositories.task_repository import TaskRepository
from app.services.xp_engine import XPEngine
from app.services.xp_service import XPService
from app.utils.datetime import utcnow


class TaskProgressService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)
        self.chunk_repository = TaskChunkRepository(db)
        self.xp_service = XPService(db)
        self.engine = XPEngine()

    def recalculate_task_progress(self, task: Task) -> Task:
        chunks = self.chunk_repository.list_for_task(task.id)
        if not chunks:
            if task.status == TaskStatus.DONE:
                task.completion_percentage = 100.0
            else:
                task.completion_percentage = 0.0
            return self.task_repository.update(task)

        completed = sum(1 for chunk in chunks if chunk.status == ChunkStatus.DONE)
        task.completion_percentage = round((completed / len(chunks)) * 100, 2)
        if completed == len(chunks):
            task.status = TaskStatus.DONE
            task.completed_at = utcnow()
        elif completed > 0 and task.status == TaskStatus.PLANNED:
            task.status = TaskStatus.ACTIVE
        return self.task_repository.update(task)

    def mark_chunk_done(self, task_id: str, chunk_id: str, actual_minutes: int | None = None) -> Task:
        task = self.task_repository.get(task_id)
        if not task:
            raise NotFoundError("Task not found")

        chunk = self.chunk_repository.get(chunk_id)
        if not chunk or chunk.task_id != task.id:
            raise NotFoundError("Chunk not found")
        if chunk.status == ChunkStatus.DONE:
            return task

        chunk.status = ChunkStatus.DONE
        chunk.actual_minutes = actual_minutes
        chunk.completed_at = utcnow()
        chunk.xp_earned = self.engine.calculate_task_chunk_xp(chunk.estimated_minutes, task.importance_score)

        self.db.add(chunk)
        self.db.flush()

        self.xp_service.grant_xp(
            user_id=task.user_id,
            source_type=XPSourceType.TASK_CHUNK,
            source_id=chunk.id,
            xp_delta=chunk.xp_earned,
            reason=f"Completed chunk '{chunk.title}'",
        )

        updated_task = self.recalculate_task_progress(task)
        if updated_task.status == TaskStatus.DONE:
            bonus = self.engine.calculate_task_completion_bonus(updated_task.estimated_minutes_total, updated_task.importance_score)
            self.xp_service.grant_xp(
                user_id=updated_task.user_id,
                source_type=XPSourceType.TASK,
                source_id=updated_task.id,
                xp_delta=bonus,
                reason=f"Completed task '{updated_task.title}'",
            )
        return updated_task

    def mark_task_done(self, task_id: str) -> Task:
        task = self.task_repository.get(task_id)
        if not task:
            raise NotFoundError("Task not found")
        if task.chunks and any(chunk.status != ChunkStatus.DONE for chunk in task.chunks):
            raise ValidationError("All chunks must be completed before marking task done")
        if task.status == TaskStatus.DONE:
            return task

        task.status = TaskStatus.DONE
        task.completion_percentage = 100.0
        task.completed_at = utcnow()
        self.task_repository.update(task)

        bonus = self.engine.calculate_task_completion_bonus(task.estimated_minutes_total, task.importance_score)
        self.xp_service.grant_xp(
            user_id=task.user_id,
            source_type=XPSourceType.TASK,
            source_id=task.id,
            xp_delta=bonus,
            reason=f"Completed task '{task.title}'",
        )
        return task

