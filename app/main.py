import asyncio

from app.kafka.repositories.kafka_repositories import KafkaRepository
from app.gateway.gRPC.server import serve

async def main():
    kf = KafkaRepository()
    await kf.wait_kafka()
    await serve()

if __name__ == "__main__":
    asyncio.run(main())