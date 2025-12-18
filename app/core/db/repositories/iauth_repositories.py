from abc import ABC, abstractmethod

from ..models.auth import Auth


class IAuthRepository(ABC):
    @abstractmethod
    async def create_auth_user(self, user: Auth, context) -> None:
        pass

    @abstractmethod
    async def activate_user_with_refresh(
        self, user: Auth, refresh_token: str, context
    ) -> None:
        pass

    @abstractmethod
    async def add_refresh_token(self, user: Auth, refresh_token: str, context) -> None:
        pass

    @abstractmethod
    async def get_user_by_login(self, login: str, context) -> Auth | None:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str, context) -> Auth | None:
        pass

    @abstractmethod
    async def delete_auth_user(self, user: Auth) -> None:
        pass

    @abstractmethod
    async def update_auth_user(self, user: Auth, context) -> None:
        pass
