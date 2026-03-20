from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.task import TaskCreate, TaskListResponse, TaskRead, TaskUpdate
from app.schemas.task_chunk import TaskChunkCreate, TaskChunkRead, TaskChunkUpdate
from app.services.task_service import TaskService


router = APIRouter()


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).create_task(payload.model_copy(update={"user_id": current_user.id}))


@router.get("/today", response_model=TaskListResponse)
def get_today_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskListResponse(items=TaskService(db).get_tasks_for_day(current_user.id, date.today()))


@router.get("", response_model=TaskListResponse)
def list_tasks_by_date(assigned_day: date = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskListResponse(items=TaskService(db).list_tasks_by_date(current_user.id, assigned_day))


@router.get("/range", response_model=TaskListResponse)
def list_tasks_in_range(
    start_day: date = Query(...),
    end_day: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TaskListResponse(items=TaskService(db).list_tasks_in_range(current_user.id, start_day, end_day))


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).get_task(current_user.id, task_id)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).update_task(current_user.id, task_id, payload)


@router.delete("/{task_id}", response_model=MessageResponse)
def delete_task(task_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    TaskService(db).delete_task(current_user.id, task_id)
    return MessageResponse(message="Task deleted")


@router.post("/{task_id}/active", response_model=TaskRead)
def mark_active(task_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).mark_active(current_user.id, task_id)


@router.post("/{task_id}/done", response_model=TaskRead)
def mark_done(task_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).mark_done(current_user.id, task_id)


@router.post("/{task_id}/missed", response_model=TaskRead)
def mark_missed(task_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).mark_missed(current_user.id, task_id)


@router.post("/{task_id}/chunks", response_model=TaskChunkRead, status_code=status.HTTP_201_CREATED)
def add_chunk(task_id: str, payload: TaskChunkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).add_chunk(current_user.id, task_id, payload)


@router.patch("/{task_id}/chunks/{chunk_id}", response_model=TaskChunkRead)
def update_chunk(
    task_id: str,
    chunk_id: str,
    payload: TaskChunkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TaskService(db).update_chunk(current_user.id, task_id, chunk_id, payload)


@router.post("/{task_id}/chunks/{chunk_id}/done", response_model=TaskRead)
def mark_chunk_done(
    task_id: str,
    chunk_id: str,
    actual_minutes: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TaskService(db).mark_chunk_done(current_user.id, task_id, chunk_id, actual_minutes)


@router.delete("/{task_id}/chunks/{chunk_id}", response_model=MessageResponse)
def delete_chunk(task_id: str, chunk_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    TaskService(db).delete_chunk(current_user.id, task_id, chunk_id)
    return MessageResponse(message="Chunk deleted")
