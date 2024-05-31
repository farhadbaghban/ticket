from pydantic import BaseModel,EmailStr,Field
from datetime import timedelta


class TokenData(BaseModel):
    email: EmailStr | None = Field(default=None)
    exp: timedelta | None = None


class TokenResponseSchema(BaseModel):
    access: str | None = None
