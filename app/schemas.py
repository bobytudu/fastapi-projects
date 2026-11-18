from pydantic import BaseModel, EmailStr
from fastapi_users import schemas
import uuid

class PostCreate(BaseModel):
  title: str
  content: str

# User schemas
class UserCreate(schemas.BaseUserCreate):
  pass

class UserUpdate(schemas.BaseUserUpdate):
  pass

class UserDelete(BaseModel):
  pass

class UserRead(schemas.BaseUser[uuid.UUID]):
  pass