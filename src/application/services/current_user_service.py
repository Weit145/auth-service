from dataclasses import dataclass

from src.application.dtos.inputs import CurrentUserInput
from src.application.dtos.outputs import UserOutput
from src.domain.repositories.iuser_repository import IUserRepository
from src.domain.value_objects import(
    PasswordHash,
    Username
)

from src.application.services.event_bus import IEventBus
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.security.token_service import TokenService

@dataclass
class CurerentUserService:
    
    repo:IUserRepository
    password_service:PasswordService
    token_service:TokenService
    event_bus: IEventBus

    async def execute(self, dto:CurrentUserInput)->UserOutput:

        user = await self.repo.get_by_username(Username(dto.username))
        if user is None or user.is_verified is False:
            raise Exception("Not username in db")

        return UserOutput(
            username=user.username.value,
            is_verified=user.is_verified,
            is_active=user.is_active,
            role=user.role
        )

