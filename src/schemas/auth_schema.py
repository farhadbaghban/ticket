from pydantic import BaseModel, EmailStr, Field
from datetime import timedelta
from typing import Optional


class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    exp: Optional[timedelta] = None


class TokenResponseSchema(BaseModel):
    access: str | None = None
