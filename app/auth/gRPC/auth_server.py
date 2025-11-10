import grpc

from proto import auth_pb2,auth_pb2_grpc

class AuthServicer(auth_pb2_grpc.AuthServicer):
    async def CreateUser(self, request, context):
        username = request.username
        email = request.email
        password = request.password
        return auth_pb2.OkeyResponse(success=False, error="User already exists")