from database import get_connection
from fastapi import HTTPException
import asyncpg


async def create_new_user(full_name: str, email: str, password: str):
    hashed_password = f"hashed_{password}_for_demo"
    async with get_connection() as conn:
        try:
            user_id = await conn.fetchval(
                "INSERT INTO users(full_name, email, hashed_password) VALUES ($1, $2, $3) RETURNING id",
                full_name, email, hashed_password
            )
            return user_id
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким email уже существует!"
            )

async def get_all_users():
    async with get_connection() as conn:
        records = await conn.fetch("SELECT id, full_name, email, created_at FROM users")
        return [dict(record) for record in records]

async def get_user_by_id(user_id: int):
    async with get_connection() as conn:
        record = await conn.fetchrow("SELECT id, full_name, email, created_at FROM users WHERE id = $1", user_id)
        if record:
            return dict(record)
        return None

async def update_user_info(user_id: int, full_name: str, email: str):
    async with get_connection() as conn:
        try:
            record = await conn.fetchrow(
                "UPDATE users SET full_name = $1, email = $2 WHERE id = $3 RETURNING id, full_name, email, created_at",
                full_name, email, user_id
            )
            if not record:
                raise HTTPException(status_code=404, detail="Пользователь не найден!")
            return dict(record)
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким email уже существует!"
            )

async def delete_user_by_id(user_id: int):
    async with get_connection() as conn:
        result = await conn.execute("DELETE FROM users WHERE id = $1", user_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Пользователь не найден!")
        return {"message": "Пользователь успешно удален"}


async def create_new_post(title: str, content: str, user_id: int):
    async with get_connection() as conn:
        user = await conn.fetchrow("SELECT id FROM users WHERE id = $1", user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Невозможно создать пост: пользователь с id={user_id} не найден.")
        
        post_id = await conn.fetchval(
            "INSERT INTO posts(title, content, user_id) VALUES ($1, $2, $3) RETURNING id",
            title, content, user_id
        )
        return post_id

async def get_all_posts():
    async with get_connection() as conn:
        records = await conn.fetch("SELECT * FROM posts ORDER BY published_at DESC")
        return [dict(record) for record in records]

async def get_post_by_id(post_id: int):
    async with get_connection() as conn:
        record = await conn.fetchrow("SELECT * FROM posts WHERE id = $1", post_id)
        if record:
            return dict(record)
        return None

async def update_post_info(post_id: int, title: str, content: str):
    async with get_connection() as conn:
        record = await conn.fetchrow(
            "UPDATE posts SET title = $1, content = $2 WHERE id = $3 RETURNING *",
            title, content, post_id
        )
        if not record:
            raise HTTPException(status_code=404, detail="Пост не найден!")
        return dict(record)

async def delete_post_by_id(post_id: int):
    async with get_connection() as conn:
        result = await conn.execute("DELETE FROM posts WHERE id = $1", post_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Пост не найден!")
        return {"message": "Пост успешно удален"}