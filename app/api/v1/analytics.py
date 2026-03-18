from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.analytics import AnalyticsOverview
from app.services.analytics_service import AnalyticsService


router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
def analytics_overview(user_id: str = Query(...), db: Session = Depends(get_db)):
    return AnalyticsService(db).overview(user_id)

