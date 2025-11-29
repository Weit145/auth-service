from dataclasses import dataclass

from src.application.dtos.inputs import RefreshTokenInput
from src.application.dtos.outputs import TokenOutput
from src.domain.repositories.iuser_repository import IUserRepository
from src.domain.value_objects import(
    PasswordHash,
    Username
)

from src.application.services.event_bus import IEventBus
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.security.token_service import TokenService

@dataclass
class RefreshTokenService:
    
    repo:IUserRepository
    password_service:PasswordService
    token_service:TokenService
    event_bus: IEventBus

    async def execute(self, dto:RefreshTokenInput)->TokenOutput:
        username  = self.token_service.decode_jwt_login(dto.refresh_token)
        if username is None:
            raise Exception("Invalid token")

        user = await self.repo.get_by_username(Username(username))
        if user is None or user.refresh_token_hash is None:
            raise Exception("Not username in db")

        result = self.password_service.verify_password(dto.refresh_token, user.refresh_token_hash.value)
        if not result:
            raise Exception("Invalid refresh token")

        access_token = self.token_service.create_access_token_user({"sub": username})

        return TokenOutput(
            access_token=access_token,
        )
