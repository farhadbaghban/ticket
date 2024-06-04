from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import get_db

from schemas.stadium_schema import StadiumCreate, StadiumRead
from operation.stadium.stadiums import StadiumOperation

from operation.users.jwt import JWTHandler
from schemas.auth_schema import TokenData
from exceptions import ValidationToken


router = APIRouter()


@router.post("/", tags=["stadiums"], summary="Create new stadium")
async def create_stadium(
    stadium: StadiumCreate = Body(),
    db: AsyncSession = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    async with db.begin() as transaction:
        if token_data:
            stadium = await StadiumOperation(db=transaction).create_stadium(
                stadium=stadium
            )
        else:
            raise ValidationToken
    return stadium


@router.get("/", response_model=List[StadiumRead], tags=["stadiums"])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    stadiums = await StadiumOperation(db=db).get_stadiums(skip=skip, limit=limit)
    return stadiums


@router.get("/{name}", tags=["stadiums"])
async def read_stadium(
    name,
    db: AsyncSession = Depends(get_db),
):
    stadium = await StadiumOperation(db=db).get_stadium(name=name)
    return stadium


@router.delete("/", tags=["stadium"])
async def delete_user(
    name,
    db: AsyncSession = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    if token_data:
        stadium = await StadiumOperation(db=db).delete_stadium(name=name)
    else:
        raise ValidationToken
    return stadium
