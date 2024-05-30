from pydantic import BaseModel


class UserAuth(BaseModel):
    id: int
    email: str


class UserCreateLogin(BaseModel):
    password: str
    email: str
