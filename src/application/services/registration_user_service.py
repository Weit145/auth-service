from dataclasses import dataclass

from src.application.dtos.inputs import ConfirmUserInput
from src.application.dtos.outputs import CookieOutput, Cookie
from src.domain.repositories.iuser_repository import IUserRepository
from src.domain.value_objects import(
    PasswordHash,
    Email
)

from src.application.services.event_bus import IEventBus
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.security.token_service import TokenService

@dataclass
class RegistrationUserService:
    
    repo:IUserRepository
    password_service:PasswordService
    token_service:TokenService
    event_bus: IEventBus

    async def execute(self, dto:ConfirmUserInput)->CookieOutput:
        email  = self.token_service.decode_jwt_email(dto.token)
        if email is None:
            raise Exception("Invalid token")

        user = await self.repo.get_by_email(Email(email))
        if user is None:
            raise Exception("Not email in db")

        access_token = self.token_service.create_access_token_user({"sub": user.username.value})
        refresh_token = self.token_service.create_refresh_token({"sub": user.username.value})
        user.password_hash = PasswordHash(
            self.password_service.get_password_hash(refresh_token))

        await self.repo.add(user)

        return CookieOutput(
            access_token=access_token,
            cookie=Cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=7*24*60*60
            )
        )
