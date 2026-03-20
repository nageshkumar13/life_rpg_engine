from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.review import DailyReviewListResponse, DailyReviewRead
from app.services.daily_review_service import DailyReviewService


router = APIRouter()


@router.post("/freeze", response_model=DailyReviewRead, status_code=status.HTTP_201_CREATED)
def freeze_day(target_date: date = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return DailyReviewService(db).freeze_day(current_user.id, target_date)


@router.post("", response_model=DailyReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(
    review_date: date = Query(...),
    remark: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DailyReviewService(db).create_review(current_user.id, review_date, remark)


@router.get("", response_model=DailyReviewListResponse)
def list_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return DailyReviewListResponse(items=DailyReviewService(db).list_reviews(current_user.id))
