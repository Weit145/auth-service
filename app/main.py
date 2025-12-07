import asyncio

from app.kafka.repositories.kafka_repositories import KafkaRepository
from app.gateway.gRPC.server import serve

async def main():
    kf = KafkaRepository()
    await kf.wait_kafka()
    asyncio.create_task(kf.get_message("delete", "auth_service"))
    await serve()

if __name__ == "__main__":
    asyncio.run(main())