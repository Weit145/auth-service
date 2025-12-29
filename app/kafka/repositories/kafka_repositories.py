import json
import asyncio
from typing import Union, List
from aiokafka.admin import NewTopic

from app.kafka.kf_helper import kf_helper


class KafkaRepository:
    async def create_topic(
        self, name_topic: str, partitions: int = 3, replication: int = 1
    ):
        topic_list = [
            NewTopic(
                name=name_topic,
                num_partitions=partitions,
                replication_factor=replication,
            )
        ]
        async with kf_helper.transaction_admin() as admin:
            await admin.create_topics(new_topics=topic_list, validate_only=False)

    async def send_message(self, topic: str, message: dict):
        async with kf_helper.transaction_produсer() as producer:
            await producer.send_and_wait(topic, json.dumps(message).encode("utf-8"))

    async def get_message(self, topic: Union[str, List[str]], group_id: str):
        async with kf_helper.transaction_consumer(
            topics=topic, group_id=group_id
        ) as consumer:
            async for msg in consumer:
                data = json.loads(msg.value.decode("utf-8"))
                from app.gateway.services.auth_service import AuthServiceImpl

                if topic == "delete":
                    await AuthServiceImpl().DeleteUserFromUserService(data)
                elif topic == "check_verified":
                    await AuthServiceImpl().DeleteNoVerifiedUser(data)
                elif topic == "admin_delete_user":
                    await AuthServiceImpl().DeleteUserFromUserService(data)
                elif topic == "admin_ban_user":
                    await AuthServiceImpl().BanUser(data)


    async def wait_kafka(self, retries=10000, delay=20):
        for i in range(retries):
            try:
                await self.create_topic(name_topic="auth")
                await self.create_topic(name_topic="registration")
                return
            except Exception as e:
                print(f"Kafka not ready yet ({i + 1}/{retries}): {e}")
                await asyncio.sleep(delay)
        raise Exception("Kafka is not available after retries")
