from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_review import DailyReview


class ReviewRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, review: DailyReview) -> DailyReview:
        self.db.add(review)
        self.db.flush()
        return review

    def get_for_day(self, user_id: str, review_date: date) -> DailyReview | None:
        stmt = select(DailyReview).where(DailyReview.user_id == user_id, DailyReview.review_date == review_date)
        return self.db.scalar(stmt)

    def list_for_user(self, user_id: str) -> list[DailyReview]:
        stmt = select(DailyReview).where(DailyReview.user_id == user_id).order_by(DailyReview.review_date.desc())
        return list(self.db.scalars(stmt).all())

