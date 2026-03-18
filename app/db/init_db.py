from app.db.base import Base
from app.db.session import engine
from app.models import backlog_task, daily_review, habit, habit_log, task, task_chunk, user, xp_log  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

