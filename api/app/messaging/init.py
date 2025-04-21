from fastapi import FastAPI

from ..messaging.connection import RabbitMQConnection

rabbitmq_connection = None

async def connect_rabbitmq(app: FastAPI):
    global rabbitmq_connection
    rabbitmq_connection = RabbitMQConnection()
    await rabbitmq_connection.connect()
    app.state.rabbitmq_connection = rabbitmq_connection

async def close_rabbitmq(app: FastAPI):
    if hasattr(app.state, 'rabbitmq_connection'):
        await app.state.rabbitmq_connection.close()