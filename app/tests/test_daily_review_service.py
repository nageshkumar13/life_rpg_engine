from datetime import date

from app.core.enums import HabitLogStatus, TaskStatus, TaskType
from app.models.habit_log import HabitLog
from app.models.task import Task
from app.models.user import User
from app.models.xp_log import XPLog
from app.services.daily_review_service import DailyReviewService
from app.utils.datetime import utcnow
from app.utils.ids import new_id


def test_daily_review_service_creates_snapshot(db_session):
    user = User(id="review-user", email="review@example.com")
    db_session.add(user)
    db_session.flush()

    db_session.add(
        Task(
            id=new_id(),
            user_id=user.id,
            title="Planned task",
            type=TaskType.PLANNED,
            assigned_day=date.today(),
            status=TaskStatus.DONE,
            importance_score=3,
            estimated_minutes_total=60,
            completion_percentage=100,
        )
    )
    db_session.add(
        HabitLog(
            id=new_id(),
            habit_id=new_id(),
            user_id=user.id,
            log_date=date.today(),
            status=HabitLogStatus.COMPLETED,
            actual_minutes=20,
            xp_earned=25,
            streak_after_log=1,
        )
    )
    db_session.add(
        XPLog(
            id=new_id(),
            user_id=user.id,
            source_type="HABIT_LOG",
            source_id=new_id(),
            xp_delta=25,
            reason="Test XP",
            created_at=utcnow(),
        )
    )
    db_session.commit()

    review = DailyReviewService(db_session).create_review(user.id, date.today())
    assert review.discipline_score == 100
    assert review.habit_score == 100
    assert review.xp_earned == 25
