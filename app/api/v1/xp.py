from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.repositories.xp_repository import XPRepository
from app.schemas.xp import XPLogListResponse


router = APIRouter()


@router.get("/logs", response_model=XPLogListResponse)
def list_xp_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return XPLogListResponse(items=XPRepository(db).list_for_user(current_user.id))
