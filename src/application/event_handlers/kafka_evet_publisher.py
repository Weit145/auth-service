from src.application.services.event_bus import IEventBus
from src.infrastructure.events.kafka_event_bus import KafkaRepository

class KafkaEventPublisher(IEventBus):
    def __init__(self):
        self.kafka = KafkaRepository()

    async def publish(self, event:object) -> None:
        await self.kafka.send_message(event.topic, message=event.message)
