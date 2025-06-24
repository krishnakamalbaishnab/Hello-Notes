from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    is_active: bool = True

class UserInDB(User):
    hashed_password: str 