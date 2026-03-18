from datetime import date, timedelta

from app.db.session import SessionLocal
from app.services.daily_review_service import DailyReviewService


def run_daily_reset(user_id: str, target_date: date | None = None) -> None:
    db = SessionLocal()
    try:
        service = DailyReviewService(db)
        day = target_date or (date.today() - timedelta(days=1))
        service.freeze_day(user_id, day)
    finally:
        db.close()

