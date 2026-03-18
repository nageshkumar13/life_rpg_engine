from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.backlog import BacklogAssignRequest, BacklogAssignmentResponse, BacklogCreate, BacklogRead, BacklogUpdate
from app.schemas.common import MessageResponse
from app.services.backlog_service import BacklogService


router = APIRouter()


@router.post("", response_model=BacklogRead, status_code=status.HTTP_201_CREATED)
def create_backlog(payload: BacklogCreate, db: Session = Depends(get_db)):
    return BacklogService(db).create_backlog(payload)


@router.get("", response_model=list[BacklogRead])
def list_backlog(user_id: str = Query(...), db: Session = Depends(get_db)):
    return BacklogService(db).list_backlog(user_id)


@router.patch("/{backlog_id}", response_model=BacklogRead)
def update_backlog(backlog_id: str, payload: BacklogUpdate, db: Session = Depends(get_db)):
    return BacklogService(db).update_backlog(backlog_id, payload)


@router.delete("/{backlog_id}", response_model=MessageResponse)
def delete_backlog(backlog_id: str, db: Session = Depends(get_db)):
    BacklogService(db).delete_backlog(backlog_id)
    return MessageResponse(message="Backlog item deleted")


@router.post("/{backlog_id}/assign", response_model=BacklogAssignmentResponse)
def assign_backlog(backlog_id: str, payload: BacklogAssignRequest, db: Session = Depends(get_db)):
    backlog, task = BacklogService(db).assign_to_day(backlog_id, payload.assigned_day)
    return BacklogAssignmentResponse(backlog=backlog, task=task)

