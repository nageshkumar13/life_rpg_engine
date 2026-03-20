from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.analytics import AnalyticsOverview
from app.services.analytics_service import AnalyticsService


router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
def analytics_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return AnalyticsService(db).overview(current_user.id)
