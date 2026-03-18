from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.utils.datetime import utcnow


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(String(32), default="PLANNED")
    importance_score: Mapped[int] = mapped_column(Integer, default=1)
    estimated_minutes_total: Mapped[int] = mapped_column(Integer, default=0)
    assigned_day: Mapped[date | None] = mapped_column(Date, index=True, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="PLANNED")
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    source_backlog_id: Mapped[str | None] = mapped_column(ForeignKey("backlog_tasks.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="tasks")
    chunks = relationship("TaskChunk", back_populates="task", cascade="all, delete-orphan", order_by="TaskChunk.order_index")

