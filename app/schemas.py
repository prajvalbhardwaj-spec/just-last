from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ─── User Schemas ────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Auth Schemas ─────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ─── Blog Schemas ─────────────────────────────────────────────────────────────

class BlogCreate(BaseModel):
    title: str
    content: str


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class BlogOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = {"from_attributes": True}
