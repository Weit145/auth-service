from abc import ABC, abstractmethod

from app.core.db.models.auth import Auth

class IAuthService(ABC):

    @abstractmethod
    async def CreateUser(self, request):
        pass

    @abstractmethod
    async def RegistrationUser(self, request):
        pass

    @abstractmethod
    async def RefreshToken(self, request):
        pass

    @abstractmethod
    async def Authenticate(self, request):
        pass

    @abstractmethod
    async def CurrentUser(self, request):
        pass
