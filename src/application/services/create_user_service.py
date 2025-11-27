from dataclasses import dataclass

from src.application.dtos.inputs import CreateUserInput
from src.domain.repositories.iuser_repository import IUserRepository
from src.domain.value_objects import(

    PasswordHash,
)
from src.domain.events import(
    UserCreatedEvent,
)
from src.application.services.event_bus import IEventBus
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.security.token_service import TokenService
from src.application.utils.convert import convert_input_to_user

@dataclass
class CreateUserService:
    
    repo:IUserRepository
    password_service:PasswordService
    token_service:TokenService
    event_bus: IEventBus

    async def execute(self, dto:CreateUserInput)->None:
        new_user  = convert_input_to_user(dto)

        existing_user = await self.repo.get_by_username(new_user.username)
        if existing_user:
            raise Exception("Username already taken")

        existing_email = await self.repo.get_by_email(new_user.email)
        if existing_email:
            raise Exception("Email already registered")

        new_user.password_hash = PasswordHash(
            self.password_service.get_password_hash(new_user.password_hash.value))

        await self.repo.add(new_user)

        access_token = self.token_service.create_access_token_email({"sub": new_user.email.value})
        new_user._add_event(UserCreatedEvent(
            topic="user.created",
            message={
                "username": new_user.username.value,
                "email": new_user.email.value,
                "access_token": access_token
            }
        ))

        for event in new_user.pull_events():
            if self.event_bus:
                await self.event_bus.publish(event)
