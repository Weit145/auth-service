from contextlib import asynccontextmanager
from typing import Union, List
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.admin import NewTopic, AIOKafkaAdminClient
from app.core.config import settings


class KafkaHelper:
    def __init__(self, url='localhost:9092', enable_idempotence=True):
        self.bootstrap_servers = url
        self.enable_idempotence = enable_idempotence

    def get_producer(self)->AIOKafkaProducer:
        return AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            enable_idempotence=self.enable_idempotence,
        )

    def get_consumer(self, topics: Union[str, List[str]], group_id: str, auto_offset_reset: str = "earliest") -> AIOKafkaConsumer:
        if isinstance(topics, str):
            topics = [topics]
        return AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset
        )

    
    def get_admin(self)->AIOKafkaAdminClient:
        return AIOKafkaAdminClient(
            bootstrap_servers=self.bootstrap_servers,
        )
    

    @asynccontextmanager
    async def transaction_produсer(self):
        producer = self.get_producer()
        await producer.start()
        try:
            yield producer
        finally:
            await producer.stop()

    @asynccontextmanager
    async def transaction_consumer(self,topics: Union[str, List[str]], group_id: str):
        consumer = self.get_consumer(topics,group_id)
        await consumer.start()
        try:
            yield consumer
        finally:
            await consumer.stop()

    @asynccontextmanager
    async def transaction_admin(self):
        admin = self.get_admin()
        await admin.start()
        try:
            yield admin
        finally:
            await admin.close()

kf_helper = KafkaHelper(url=settings.kafka_url)
