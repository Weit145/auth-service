from abc import ABC, abstractmethod
from proto import auth_pb2


class IAuthServiceImpl(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def CreateUser(self, request,context)->auth_pb2.Okey:
        pass

    @abstractmethod
    async def RegistrationUser(self, request,context)->auth_pb2.CookieResponse:
        pass

    @abstractmethod
    async def RefreshToken(self, request,context)->auth_pb2.AccessTokenResponse:
        pass

    @abstractmethod
    async def Authenticate(self, request,context)->auth_pb2.CookieResponse:
        pass

    @abstractmethod
    async def CurrentUser(self, request,context)->auth_pb2.CurrentUserResponse:
        pass

    @abstractmethod
    async def LogOutUser(self, request,context)->auth_pb2.Empty:
        pass