import os
from dotenv import load_dotenv

load_dotenv()

RABBIT_URL = os.getenv("RABBIT_URL")
DATABASE_URL=os.getenv("DB_URL")