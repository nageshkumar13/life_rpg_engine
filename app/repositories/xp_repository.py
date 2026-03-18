from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.xp_log import XPLog


class XPRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, xp_log: XPLog) -> XPLog:
        self.db.add(xp_log)
        self.db.flush()
        return xp_log

    def list_for_user(self, user_id: str) -> list[XPLog]:
        stmt = select(XPLog).where(XPLog.user_id == user_id).order_by(XPLog.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def total_for_day(self, user_id: str, target_date: date) -> int:
        stmt = select(func.coalesce(func.sum(XPLog.xp_delta), 0)).where(
            XPLog.user_id == user_id,
            func.date(XPLog.created_at) == target_date.isoformat(),
        )
        return int(self.db.scalar(stmt) or 0)
