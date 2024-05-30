from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from db.models.users import User
from operation.users.security import get_hashed_password, authenticate_user
from schemas.user_schema import UserCreateLogin, UserAuth
from exceptions import UserAlreadyExists, UserNotFound
from operation.users.jwt import JWTHandler


class UserOpration:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, user: UserCreateLogin):
        password = get_hashed_password(user.password)
        user.password = password
        user = User(**user.model_dump())
        async with self.db as db:
            try:
                db.add(user)
                await db.commit()
                await db.refresh(user)
                return UserAuth(id=user.id, email=user.email)
            except IntegrityError:
                raise UserAlreadyExists

    async def login_user(self, data: UserCreateLogin):
        user = await authenticate_user(
            password=data.password,
            email=data.email,
            session=self.db,
        )
        if user:
            email = user.email
            access_token = JWTHandler.generate_token(email=email)
            return access_token

        else:
            raise UserNotFound

    async def get_user(self, email):
        async with self.db as db:
            user = await db.execute(select(User).where(User.email == email))
            user = user.scalar_one_or_none()
            if user is None:
                raise UserNotFound
            return UserAuth(id=user.id, email=user.email)

    async def get_users(self, skip: int, limit: int):
        async with self.db as db:
            result = await db.execute(select(User).offset(skip).limit(limit))
            users = result.scalars().all()
            return users

    async def delete_user(self, email):
        async with self.db as db:
            db_user = await db.execute(select(User).where(User.email == email))
            db_user = db_user.scalar_one_or_none()
            if db_user is None:
                raise UserNotFound
            db.delete(db_user)
            await db.commit()
            return db_user
