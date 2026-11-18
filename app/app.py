from app.schemas import UserUpdate
from app.schemas import UserCreate
from app.schemas import UserRead
from sqlalchemy import select
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate
from app.db import Post, User, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import Annotated
from uuid import UUID

# users
from app.users import auth_backend, current_active_user, fastapi_users

#ImageKit
from app.images import upload_image


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
AuthDep = Annotated[User, Depends(current_active_user)]

@asynccontextmanager
async def lifespan(app:FastAPI):
  await create_db_and_tables()
  yield
  

app = FastAPI(lifespan=lifespan)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix='/auth', tags=['auth'])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth/reset", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth/verify", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])



@app.get('/post')
async def get_posts(session: SessionDep):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()
    # result = Post.select()
    return posts

@app.post("/posts")
def create_posts(payload: PostCreate):
    print(payload)
    return payload

@app.post("/upload")
async def upload_file(
    user: AuthDep,
    session: SessionDep,
    file: UploadFile = File(...),
    title: str = Form(""),
):
    content = await file.read()
    image_url = upload_image(content, file.filename)
  
    if not image_url:
        raise HTTPException(status_code=500, detail="Failed to upload image")
    
    post = Post(
        title=title,
        url=image_url,
        file_type=file.content_type.split('/')[0],
        file_name=file.filename,
        user_id=user.id
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get('/feed')
async def get_feed(
  session: SessionDep,
  user: AuthDep
):
  result = await session.execute(select(Post).order_by(Post.created_at.desc()).filter(Post.user_id == user.id))
  posts = result.scalars().all()
  return posts

@app.get('/posts/{id}')
async def get_post(id: UUID, session: SessionDep):
  post = await session.get(Post, id)
  if not post:
    raise HTTPException(status_code=404, detail="Post not found")
  return post

@app.delete('/posts/{id}')
async def delete_post(id: UUID, session: SessionDep):
  post = await session.get(Post, id)
  if not post:
    raise HTTPException(status_code=404, detail="Post not found")
  await session.delete(post)
  await session.commit()
  return {"message": "Post deleted successfully"}