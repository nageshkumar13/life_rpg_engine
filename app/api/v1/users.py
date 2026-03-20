from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead


router = APIRouter()


@router.get("", response_model=list[UserRead])
def list_users(current_user: User = Depends(get_current_user)) -> list[User]:
    return [current_user]


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
