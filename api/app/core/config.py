from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

RABBIT_URL=os.getenv("RABBIT_URL")
RABBIT_EXCHANGE=os.getenv("RABBIT_EXCHANGE")
RABBIT_QUEUE_ANALISE=os.getenv("RABBIT_QUEUE_ANALISE")

def get_valid_env(env: str | None):
    if env is None:
        raise 

    return env

class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="RABBITMQ_", extra="ignore")

    url: str = get_valid_env(RABBIT_URL)
    exchange: str = get_valid_env(RABBIT_EXCHANGE)
    queue_analise: str = get_valid_env(RABBIT_QUEUE_ANALISE)


rabbitmq_settings = RabbitMQSettings()