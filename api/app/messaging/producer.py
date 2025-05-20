import pika

from ..messaging.schemas import AnaliseMessage
from ..core.config import rabbitmq_settings
from fastapi import Request

class RabbitMQProducer:
    def __init__(self, request: Request):
        self.request = request
    
    async def publish(self, routing_key: str, message: AnaliseMessage):
        channel = self.request.app.state.rabbitmq_connection._channel
        channel.basic_publish(
            exchange=rabbitmq_settings.exchange,
            routing_key=routing_key,
            body=message.serialize(),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )