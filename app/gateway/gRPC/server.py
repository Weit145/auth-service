import grpc
from proto import auth_pb2, auth_pb2_grpc

from app.gateway.gRPC.auth_server import AuthServicer

async def serve():
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC сервер запущен на порту 50051...")
    await server.start()
    await server.wait_for_termination()
