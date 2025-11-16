from abc import ABC, abstractmethod
from proto import auth_pb2


from app.core.db.models.auth import Auth

class IAuthServiceImpl(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def CreateUser(self, request)->auth_pb2.Okey:
        pass

    @abstractmethod
    async def RegistrationUser(self, request)->auth_pb2.CookieResponse:
        pass

    @abstractmethod
    async def RefreshToken(self, request)->auth_pb2.AccessTokenResponse:
        pass

    @abstractmethod
    async def Authenticate(self, request)->auth_pb2.CookieResponse:
        pass

    @abstractmethod
    async def CurrentUser(self, request)->auth_pb2.CurrentUserResponse:
        pass
