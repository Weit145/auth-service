from src.domain.entities.user import User
from src.domain.value_objects import Email, Username, PasswordHash, RefreshToken
from src.application.dtos.inputs import CreateUserInput


def convert_input_to_user(dto: CreateUserInput) -> User:
    return User(
        username=Username(dto.username),
        email=Email(dto.email),
        password_hash=PasswordHash(dto.password),
        refresh_token_hash=RefreshToken(""),
        is_active=True,
        is_verified=False,
        role="user",
    )
