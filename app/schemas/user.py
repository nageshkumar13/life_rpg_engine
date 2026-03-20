from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.schemas.common import ORMModel


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(ORMModel):
    id: str
    email: EmailStr
    level: int
    total_xp: int
    current_streak: int
    best_streak: int
    created_at: datetime
    updated_at: datetime
