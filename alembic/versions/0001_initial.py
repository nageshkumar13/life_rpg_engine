"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-03-18
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("total_xp", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("current_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("best_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "backlog_tasks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("importance_score", sa.Integer(), nullable=False),
        sa.Column("estimated_effort", sa.Integer(), nullable=False),
        sa.Column("xp_reward", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_backlog_tasks_user_id", "backlog_tasks", ["user_id"])

    op.create_table(
        "habits",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("unit_type", sa.String(length=32), nullable=False),
        sa.Column("target_minutes", sa.Integer(), nullable=False),
        sa.Column("xp_base", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_habits_user_id", "habits", ["user_id"])

    op.create_table(
        "daily_review",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("review_date", sa.Date(), nullable=False),
        sa.Column("discipline_score", sa.Integer(), nullable=False),
        sa.Column("productivity_score", sa.Integer(), nullable=False),
        sa.Column("habit_score", sa.Integer(), nullable=False),
        sa.Column("xp_earned", sa.Integer(), nullable=False),
        sa.Column("planned_completed", sa.Integer(), nullable=False),
        sa.Column("planned_total", sa.Integer(), nullable=False),
        sa.Column("unplanned_completed", sa.Integer(), nullable=False),
        sa.Column("habit_completed", sa.Integer(), nullable=False),
        sa.Column("remark", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "review_date", name="uq_daily_review_day"),
    )
    op.create_index("ix_daily_review_user_id", "daily_review", ["user_id"])
    op.create_index("ix_daily_review_review_date", "daily_review", ["review_date"])

    op.create_table(
        "tasks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("importance_score", sa.Integer(), nullable=False),
        sa.Column("estimated_minutes_total", sa.Integer(), nullable=False),
        sa.Column("assigned_day", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("completion_percentage", sa.Float(), nullable=False),
        sa.Column("source_backlog_id", sa.String(length=36), sa.ForeignKey("backlog_tasks.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_tasks_user_id", "tasks", ["user_id"])
    op.create_index("ix_tasks_assigned_day", "tasks", ["assigned_day"])

    op.create_table(
        "task_chunks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("task_id", sa.String(length=36), sa.ForeignKey("tasks.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False),
        sa.Column("actual_minutes", sa.Integer(), nullable=True),
        sa.Column("xp_earned", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_task_chunks_task_id", "task_chunks", ["task_id"])

    op.create_table(
        "habit_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("habit_id", sa.String(length=36), sa.ForeignKey("habits.id"), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("log_date", sa.Date(), nullable=False),
        sa.Column("actual_minutes", sa.Integer(), nullable=False),
        sa.Column("xp_earned", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("streak_after_log", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("habit_id", "log_date", name="uq_habit_log_day"),
    )
    op.create_index("ix_habit_logs_habit_id", "habit_logs", ["habit_id"])
    op.create_index("ix_habit_logs_user_id", "habit_logs", ["user_id"])
    op.create_index("ix_habit_logs_log_date", "habit_logs", ["log_date"])

    op.create_table(
        "xp_log",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("source_id", sa.String(length=36), nullable=False),
        sa.Column("xp_delta", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_xp_log_user_id", "xp_log", ["user_id"])
    op.create_index("ix_xp_log_source_id", "xp_log", ["source_id"])


def downgrade() -> None:
    op.drop_index("ix_xp_log_source_id", table_name="xp_log")
    op.drop_index("ix_xp_log_user_id", table_name="xp_log")
    op.drop_table("xp_log")
    op.drop_index("ix_habit_logs_log_date", table_name="habit_logs")
    op.drop_index("ix_habit_logs_user_id", table_name="habit_logs")
    op.drop_index("ix_habit_logs_habit_id", table_name="habit_logs")
    op.drop_table("habit_logs")
    op.drop_index("ix_task_chunks_task_id", table_name="task_chunks")
    op.drop_table("task_chunks")
    op.drop_index("ix_tasks_assigned_day", table_name="tasks")
    op.drop_index("ix_tasks_user_id", table_name="tasks")
    op.drop_table("tasks")
    op.drop_index("ix_daily_review_review_date", table_name="daily_review")
    op.drop_index("ix_daily_review_user_id", table_name="daily_review")
    op.drop_table("daily_review")
    op.drop_index("ix_habits_user_id", table_name="habits")
    op.drop_table("habits")
    op.drop_index("ix_backlog_tasks_user_id", table_name="backlog_tasks")
    op.drop_table("backlog_tasks")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
