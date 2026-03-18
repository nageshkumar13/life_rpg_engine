from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.review import DailyReviewListResponse, DailyReviewRead
from app.services.daily_review_service import DailyReviewService


router = APIRouter()


@router.post("/freeze", response_model=DailyReviewRead, status_code=status.HTTP_201_CREATED)
def freeze_day(user_id: str = Query(...), target_date: date = Query(...), db: Session = Depends(get_db)):
    return DailyReviewService(db).freeze_day(user_id, target_date)


@router.post("", response_model=DailyReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(user_id: str = Query(...), review_date: date = Query(...), remark: str | None = None, db: Session = Depends(get_db)):
    return DailyReviewService(db).create_review(user_id, review_date, remark)


@router.get("", response_model=DailyReviewListResponse)
def list_reviews(user_id: str = Query(...), db: Session = Depends(get_db)):
    return DailyReviewListResponse(items=DailyReviewService(db).list_reviews(user_id))

