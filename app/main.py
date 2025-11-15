import asyncio

from app.gateway.gRPC.server import serve

if __name__ == "__main__":
    asyncio.run(serve())    