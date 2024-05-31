from pydantic import BaseModel,EmailStr,Field


class UserAuth(BaseModel):
    id: int
    email: EmailStr | None = Field(default=None)


class UserCreateLogin(BaseModel):
    password: str
    email: EmailStr | None = Field(default=None)
