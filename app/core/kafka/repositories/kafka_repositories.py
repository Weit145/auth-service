from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.admin import NewTopic, AIOKafkaAdminClient
from app.core.kafka.kf_helper import kf_helper

class KafkaRepository():

    async def create_topic(self, name_topic:str, partitions:int = 3, replication:int =1):
        admin_client = kf_helper.get_admin()
        topic_list = [NewTopic(name=name_topic,
            num_partitions=partitions,
            replication_factor=replication)]
        try:
            await admin_client.start()
            await admin_client.create_topics(new_topics=topic_list, validate_only=False)
        finally:
            await admin_client.close()


    async def send_message(self,topic:str, message:str):
        producer = kf_helper.get_producer()
        await producer.start()
        try:
            await  producer.send_and_wait(topic,message.encode('utf-8'))
        except:
            await producer.stop()

    async def get_message(self,topic:str, group_id:str):
        consumer = kf_helper.get_consumer(topic,group_id)
        await consumer.start()
        try:
            async for msg in consumer:
                return msg.value.decode() 
        finally:
            await consumer.stop()