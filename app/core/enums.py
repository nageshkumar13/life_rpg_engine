from enum import Enum


class TaskType(str, Enum):
    PLANNED = "PLANNED"
    UNPLANNED = "UNPLANNED"
    HABIT_INSTANCE = "HABIT_INSTANCE"
    BACKLOG = "BACKLOG"


class TaskStatus(str, Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    DONE = "DONE"
    MISSED = "MISSED"


class ChunkStatus(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"


class HabitLogStatus(str, Enum):
    EXPECTED = "EXPECTED"
    COMPLETED = "COMPLETED"
    MISSED = "MISSED"


class BacklogStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class XPSourceType(str, Enum):
    TASK = "TASK"
    TASK_CHUNK = "TASK_CHUNK"
    HABIT_LOG = "HABIT_LOG"
    REVIEW = "REVIEW"
    BONUS = "BONUS"


class HabitUnitType(str, Enum):
    COUNT = "COUNT"
    MINUTES = "MINUTES"

