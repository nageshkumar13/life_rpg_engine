from datetime import date

from sqlalchemy.orm import Session

from app.core.enums import TaskType
from app.models.habit import Habit
from app.models.task import Task
from app.models.user import User
from app.utils.ids import new_id


def seed_demo_data(db: Session) -> None:
    user = db.get(User, "demo-user")
    if not user:
        user = User(id="demo-user", email="demo@example.com")
        db.add(user)

    if not db.query(Habit).filter(Habit.user_id == user.id).first():
        db.add(
            Habit(
                id=new_id(),
                user_id=user.id,
                title="Morning workout",
                description="Move every morning",
                target_minutes=30,
                xp_base=25,
            )
        )

    if not db.query(Task).filter(Task.user_id == user.id).first():
        db.add(
            Task(
                id=new_id(),
                user_id=user.id,
                title="Deep work block",
                description="Ship one meaningful backend slice",
                type=TaskType.PLANNED,
                importance_score=4,
                estimated_minutes_total=90,
                assigned_day=date.today(),
            )
        )

    db.commit()
