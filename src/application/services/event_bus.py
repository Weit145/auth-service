from abc import ABC, abstractmethod


class IEventBus(ABC):
    @abstractmethod
    async def publish(self, event: object) -> None:
        pass
