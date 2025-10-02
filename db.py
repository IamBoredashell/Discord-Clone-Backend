import asyncio
import os
import psycopg_pool

#Local import
from config import DATABASE_URL

pool = None

async def init_db():
    global pool
    pool = psycopg_pool.AsyncConnectionPool(DATABASE_URL, min_size=1, max_size=16)

async def close_db():
    await pool.close()
