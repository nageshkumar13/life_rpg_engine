from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task_chunk import TaskChunk


class TaskChunkRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, chunk: TaskChunk) -> TaskChunk:
        self.db.add(chunk)
        self.db.flush()
        return chunk

    def get(self, chunk_id: str) -> TaskChunk | None:
        return self.db.get(TaskChunk, chunk_id)

    def list_for_task(self, task_id: str) -> list[TaskChunk]:
        stmt = select(TaskChunk).where(TaskChunk.task_id == task_id).order_by(TaskChunk.order_index.asc())
        return list(self.db.scalars(stmt).all())

    def delete(self, chunk: TaskChunk) -> None:
        self.db.delete(chunk)

