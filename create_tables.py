import asyncio
from database import get_connection

async def main():
    async with get_connection() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(120) NOT NULL,
                email VARCHAR(120) NOT NULL UNIQUE,
                hashed_password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                title VARCHAR(150) NOT NULL,
                content TEXT,
                published_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                user_id INT REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )
    print('Таблицы "users" и "posts" успешно созданы!')

if __name__ == "__main__":
    asyncio.run(main())