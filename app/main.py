import asyncio

from app.kafka.repositories.kafka_repositories import KafkaRepository
from app.gateway.gRPC.server import serve
from app.core.db.db_hellper import db_helper


async def main():
    kf = KafkaRepository()
    await kf.wait_kafka()

    migrations_task = asyncio.create_task(db_helper.run_migrations())
    kafka_task = asyncio.create_task(kf.get_message("delete", "auth_service"))
    kafka_task_check = asyncio.create_task(
        kf.get_message("check_verified", "auth_service")
    )
    kafka_task_admin_delete = asyncio.create_task(kf.get_message("admin_delete_user", "auth_service"))
    kafka_task_admin_ban = asyncio.create_task(kf.get_message("admin_ban_user", "auth_service"))
    gateway_task = asyncio.create_task(serve())
    
    await asyncio.gather(migrations_task, kafka_task, gateway_task, kafka_task_check,kafka_task_admin_delete,kafka_task_admin_ban)


if __name__ == "__main__":
    asyncio.run(main())
