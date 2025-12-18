from src.domain.entities.user import User
from src.domain.value_objects import Email, Username, PasswordHash, RefreshToken
from src.infrastructure.database.models.user_orm_model import UserORM


def convert_user_to_orm(user: User) -> UserORM:
    return UserORM(
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        refresh_token_hash=user.refresh_token_hash,
        is_active=user.is_active,
        is_verified=user.is_verified,
        role=user.role,
    )


def convert_orm_to_user(user: UserORM | None) -> User | None:
    if user:
        return User(
            username=Username(user.username),
            email=Email(user.email),
            password_hash=PasswordHash(user.password_hash),
            refresh_token_hash=RefreshToken(user.refresh_token_hash),
            is_active=user.is_active,
            is_verified=user.is_verified,
            role=user.role,
        )
    return None
