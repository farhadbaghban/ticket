from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.users import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def get_user(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one()
    return user


async def authenticate_user(email: str, password: str, session: AsyncSession):
    user = await get_user(email=email, db=session)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
