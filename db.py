import psycopg
import psycopg_pool
import asyncio
import os
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None

async def init_db():
    global pool
    pool = psycopg_pool.AsyncConnectionPool(DATABASE_URL, min_size=1, max_size=16)
