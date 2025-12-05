from proto import auth_pb2_grpc

from app.gateway.services.auth_service import AuthServiceImpl


class AuthServicer(auth_pb2_grpc.AuthServicer):
    async def CreateUser(self, request, context):
        return await AuthServiceImpl().CreateUser(request,context)
    
    async def RegistrationUser(self, request, context):
        return await AuthServiceImpl().RegistrationUser(request, context)
    
    async def RefreshToken(self, request, context):
        return await AuthServiceImpl().RefreshToken(request, context)
    
    async def Authenticate(self, request, context):
        return await AuthServiceImpl().Authenticate(request, context)
    
    async def CurrentUser(self, request, context):
        return await AuthServiceImpl().CurrentUser(request, context)