from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.xp_repository import XPRepository
from app.schemas.xp import XPLogListResponse


router = APIRouter()


@router.get("/logs", response_model=XPLogListResponse)
def list_xp_logs(user_id: str = Query(...), db: Session = Depends(get_db)):
    return XPLogListResponse(items=XPRepository(db).list_for_user(user_id))

