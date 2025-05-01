import os
from dotenv import load_dotenv

load_dotenv()

RABBIT_URL = os.getenv("RABBIT_URL")
DATABASE_URL=os.getenv("DB_URL")
RABBIT_QUEUE_ANALISE=os.getenv("RABBIT_QUEUE_ANALISE")