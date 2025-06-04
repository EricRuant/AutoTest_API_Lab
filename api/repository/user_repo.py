# api/repository/user_repo.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from passlib.hash import bcrypt

from api.models.user import User
from api.schemas import UserCreate

async def is_username_taken(db: AsyncSession, username: str) -> bool:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none() is not None

async def is_email_taken(db: AsyncSession, email: str) -> bool:
    result = await db.execute(select(User).where(User.email == email.lower()))
    return result.scalar_one_or_none() is not None

async def create_user_repo(user_date: UserCreate, db: AsyncSession) -> User:
    hashed_password = bcrypt.hash(user_date.password)
    new_user = User(
        username=user_date.username,
        email=user_date.email.lower(),
        password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

async def get_user_by_id(user_id: UUID, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def updata_user_by_id(user: User, db: AsyncSession) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def delete_user_by_id(user: User, db: AsyncSession):
    await db.delete(user)
    await db.commit()
