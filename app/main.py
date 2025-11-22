import asyncio

from app.core.kafka.repositories.kafka_repositories import KafkaRepository
from app.gateway.gRPC.server import serve

async def main():
    kf = KafkaRepository()
    # await kf.create_topic(name_topic="auth")
    await serve()

if __name__ == "__main__":
    asyncio.run(main())