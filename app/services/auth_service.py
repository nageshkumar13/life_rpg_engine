from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ValidationError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, LoginRequest, SignupRequest
from app.utils.ids import new_id


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    def signup(self, payload: SignupRequest) -> AuthResponse:
        if len(payload.password) < 6:
            raise ValidationError("Password must be at least 6 characters")

        existing_user = self.user_repository.get_by_email(payload.email)
        if existing_user:
            raise ConflictError("Email already exists")

        user = User(
            id=new_id(),
            email=str(payload.email),
            password_hash=hash_password(payload.password),
        )
        self.user_repository.create(user)
        self.db.commit()
        self.db.refresh(user)

        return AuthResponse(access_token=create_access_token(user.id), user=user)

    def login(self, payload: LoginRequest) -> AuthResponse:
        user = self.user_repository.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise ValidationError("Invalid email or password")

        return AuthResponse(access_token=create_access_token(user.id), user=user)
