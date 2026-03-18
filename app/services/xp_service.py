from sqlalchemy.orm import Session

from app.core.enums import XPSourceType
from app.core.exceptions import NotFoundError
from app.models.xp_log import XPLog
from app.repositories.user_repository import UserRepository
from app.repositories.xp_repository import XPRepository
from app.utils.ids import new_id
from app.utils.leveling import level_from_xp


class XPService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
        self.xp_repository = XPRepository(db)

    def grant_xp(self, user_id: str, source_type: XPSourceType, source_id: str, xp_delta: int, reason: str) -> XPLog:
        user = self.user_repository.get(user_id)
        if not user:
            raise NotFoundError("User not found")

        safe_delta = max(0, xp_delta)
        user.total_xp += safe_delta
        user.level = level_from_xp(user.total_xp)

        xp_log = XPLog(
            id=new_id(),
            user_id=user_id,
            source_type=source_type,
            source_id=source_id,
            xp_delta=safe_delta,
            reason=reason,
        )
        self.xp_repository.create(xp_log)
        self.db.add(user)
        self.db.flush()
        return xp_log
