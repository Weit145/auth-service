from dataclasses import dataclass

from src.application.dtos.inputs import LoginUserInput
from src.application.dtos.outputs import CookieOutput, Cookie
from src.domain.repositories.iuser_repository import IUserRepository
from src.domain.value_objects import(
    PasswordHash,
    Username
)

from src.application.services.event_bus import IEventBus
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.security.token_service import TokenService

@dataclass
class AuthenticateUserService:
    
    repo:IUserRepository
    password_service:PasswordService
    token_service:TokenService
    event_bus: IEventBus

    async def execute(self, dto:LoginUserInput)->CookieOutput:

        user = await self.repo.get_by_username(Username(dto.username))
        if user is None or user.is_verified is False:
            raise Exception("Not username in db")

        result = self.password_service.verify_password(dto.password, user.password_hash.value)
        if not result:
            raise Exception("Invalid password")

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

