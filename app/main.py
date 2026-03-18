from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.init_db import init_db


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def startup() -> None:
    if settings.environment.lower() != "test":
        init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "LIFE RPG ENGINE backend is running"}
