from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.backlog import router as backlog_router
from app.api.v1.habits import router as habits_router
from app.api.v1.health import router as health_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.users import router as users_router
from app.api.v1.xp import router as xp_router


api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(habits_router, prefix="/habits", tags=["habits"])
api_router.include_router(backlog_router, prefix="/backlog", tags=["backlog"])
api_router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(xp_router, prefix="/xp", tags=["xp"])
