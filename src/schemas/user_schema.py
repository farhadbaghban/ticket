from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserAuth(BaseModel):
    id: int
    email: Optional[EmailStr] = None


class UserCreateLogin(BaseModel):
    password: str
    email: Optional[EmailStr] = None
