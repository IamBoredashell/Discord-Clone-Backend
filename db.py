import psycopg
import asyncio

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None

async def init_db():
    global pool
    pool = AsyncConnectionPool(DATABASE_URL, min_size=1, max_size=16)


