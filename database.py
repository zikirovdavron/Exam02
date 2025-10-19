import asyncpg
from contextlib import asynccontextmanager
import os



DB_CONFIG = {
    "host":"localhost",
    "port":5432,
    "database":"Exam22",
    "user":"postgres",
    "password":"160606"
}




@asynccontextmanager
async def get_connection():
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        await conn.close()
