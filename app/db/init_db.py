from sqlalchemy import inspect, text

from app.db.base import Base
from app.db.session import engine
from app.models import backlog_task, daily_review, habit, habit_log, task, task_chunk, user, xp_log  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    user_columns = {column["name"] for column in inspector.get_columns("users")}
    if "password_hash" not in user_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(512)"))
