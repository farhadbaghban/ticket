from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import get_db
from schemas.user_schema import UserAuth, UserCreateLogin
from schemas.auth_schema import TokenData
from exceptions import ValidationToken
from operation.users.jwt import JWTHandler
from operation.users.users import UserOpration

router = APIRouter()


@router.post("/", tags=["users"], summary="Create new user")
async def create_user(
    user: UserCreateLogin = Body(), db: AsyncSession = Depends(get_db)
):
    return await UserOpration(db=db).create_user(user=user)


@router.get("/", response_model=List[UserAuth], tags=["users"])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    if token_data:
        users = await UserOpration(db=db).get_users(skip=skip, limit=limit)
        return users
    else:
        raise ValidationToken


@router.get("/{email}", tags=["users"])
async def read_user(
    email,
    db: AsyncSession = Depends(get_db),
    # token_data: TokenData = Depends(JWTHandler.verify_token),
):
    user = await UserOpration(db=db).get_user(email=email)
    return user


@router.delete("/", tags=["users"])
async def delete_user(
    db: AsyncSession = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    if token_data:
        user = await UserOpration(db=db).delete_user(email=token_data.email)
    else:
        raise ValidationToken
    return user


@router.post("/login", tags=["users"])
async def login(data: UserCreateLogin = Body(), db: AsyncSession = Depends(get_db)):
    token = await UserOpration(db=db).login_user(data=data)
    return token
