# app/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AssetCreate(BaseModel):
    filename: str
    file_type: str
    category: str | None = None
    path: str


class AssetOut(BaseModel):
    id: int
    filename: str
    file_type: str
    category: str | None
    path: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True