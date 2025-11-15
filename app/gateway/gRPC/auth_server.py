from proto import auth_pb2_grpc

from app.gateway.services.auth_service import AuthServiceImpl


class AuthServicer(auth_pb2_grpc.AuthServicer):
    async def CreateUser(self, request, context):
        return await AuthServiceImpl().CreateUser(request)
    
    async def RegistrationUser(self, request, context):
        return await AuthServiceImpl().RegistrationUser(request)
    
    async def RefreshToken(self, request, context):
        return await AuthServiceImpl().RefreshToken(request)
    
    async def Authenticate(self, request, context):
        return await AuthServiceImpl().Authenticate(request)
    
    async def CurrentUser(self, request, context):
        return await AuthServiceImpl().CurrentUser(request)