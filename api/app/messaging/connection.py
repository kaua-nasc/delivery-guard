import os
import pika

from ..core.config import rabbitmq_settings

class RabbitMQConnection:
    def __init__(self):
        self._connection = None
        self._channel = None
    
    async def connect(self):
        try:
            if not self._connection or self._connection.is_closed:
                parameters = pika.URLParameters(rabbitmq_settings.url)
                self._connection = pika.BlockingConnection(parameters)
                self._channel = self._connection.channel()
                
                self._channel.exchange_declare(
                    exchange=rabbitmq_settings.exchange,
                    exchange_type='topic',
                    durable=True
                )
                self._channel.queue_declare(
                    queue=rabbitmq_settings.queue_analise,
                    durable=True
                )
                self._channel.queue_bind(
                    exchange=rabbitmq_settings.exchange,
                    queue=rabbitmq_settings.queue_analise,
                    routing_key="transaction.#"
                )
            
            return self._channel
        except:
            print("Message Queue - Connection error")
            os._exit(0)
    
    async def close(self):
        if self._connection and self._connection.is_open:
            self._connection.close()