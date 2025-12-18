from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User
from src.domain.value_objects import (
    Email,
    Username,
)


class IUserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_username(self, username: Username) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass
