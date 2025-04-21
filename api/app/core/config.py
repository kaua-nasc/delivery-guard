from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

RABBIT_URL=os.getenv("RABBIT_URL")
RABBIT_EXCHANGE=os.getenv("RABBIT_EXCHANGE")
RABBIT_QUEUE_ANALISE=os.getenv("RABBIT_QUEUE_ANALISE")

class RabbitMQSettings(BaseSettings):
    url: str = RABBIT_URL
    exchange: str = RABBIT_EXCHANGE
    queue_analise: str = RABBIT_QUEUE_ANALISE

    class Config:
        env_prefix = "RABBITMQ_"

rabbitmq_settings = RabbitMQSettings()