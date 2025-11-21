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

    def get_consumer(self, topic: str, group_id: str, auto_offset_reset:str = "earliest")->AIOKafkaConsumer:
        return AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset
        )
    
    def get_admin(self)->AIOKafkaAdminClient:
        return AIOKafkaAdminClient(
            bootstrap_servers=self.bootstrap_servers,
        )
    

kf_helper = KafkaHelper(url=settings.kafka_url)
