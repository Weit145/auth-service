from abc import ABC, abstractmethod

from ..models.auth import Auth

class IAuthRepository(ABC):

    @abstractmethod
    async def create_auth_user(self, user: Auth) -> None:
        pass

    @abstractmethod
    async def activate_auth_user(self, user: Auth) -> None:
        pass
    
    @abstractmethod
    async def add_refresh_token(self,user:Auth,refresh_token:str)->None:
        pass
    
    @abstractmethod
    async def get_user_by_username(self,username:str)->Auth | None:
        pass

    @abstractmethod
    async def get_user_by_email(self,email:str)->Auth | None:
        pass
    
    @abstractmethod
    async def delete_auth_user(self, user: Auth) -> None:
        pass

    @abstractmethod
    async def update_auth_user(self, user: Auth) -> None:
        pass
