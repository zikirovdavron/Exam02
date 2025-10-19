from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from queries import *

app = FastAPI(
    title="Users and Posts API",description="API для CRUD операций с пользователями и их постами",version="1.1.0"
)

class UserBase(BaseModel):
    full_name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

class PostBase(BaseModel):
    title: str
    content: str | None = None

class PostCreate(PostBase):
    user_id: int

class PostResponse(PostBase):
    id: int
    published_at: datetime
    user_id: int


@app.post("/userss/", response_model=UserResponse, summary="Создать нового пользователя")
async def create_user_endpoint(user: UserCreate):
    user_id = await create_new_user(full_name=user.full_name, email=user.email, password=user.password)
    created_user = await get_user_by_id(user_id)
    return created_user

@app.get("/users/", response_model=list[UserResponse], summary="Получить список всех пользователей")
async def get_users_endpoint():
    return await get_all_users()

@app.get("/users/{user_id}", response_model=UserResponse, summary="Получить пользователя по ID")
async def get_single_user_endpoint(user_id: int):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    return user

@app.put("/users/{user_id}", response_model=UserResponse, summary="Обновить данные пользователя")
async def update_user_endpoint(user_id: int, user: UserBase):
    return await update_user_info(user_id=user_id, full_name=user.full_name, email=user.email)

@app.delete("/users/{user_id}", summary="Удалить пользователя по ID")
async def delete_user_endpoint(user_id: int):
    return await delete_user_by_id(user_id)


@app.post("/posts/", response_model=PostResponse, summary="Создать новый пост")
async def create_post_endpoint(post: PostCreate):
    post_id = await create_new_post(title=post.title, content=post.content, user_id=post.user_id)
    created_post = await get_post_by_id(post_id)
    return created_post

@app.get("/posts/", response_model=list[PostResponse], summary="Получить список всех постов")
async def get_posts_endpoint():
    return await get_all_posts()

@app.get("/posts/{post_id}", response_model=PostResponse, summary="Получить пост по ID")
async def get_single_post_endpoint(post_id: int):
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден!")
    return post

@app.put("/posts/{post_id}", response_model=PostResponse, summary="Обновить пост")
async def update_post_endpoint(post_id: int, post: PostBase):
    return await update_post_info(post_id=post_id, title=post.title, content=post.content)

@app.delete("/posts/{post_id}", summary="Удалить пост по ID")
async def delete_post_endpoint(post_id: int):
    return await delete_post_by_id(post_id)