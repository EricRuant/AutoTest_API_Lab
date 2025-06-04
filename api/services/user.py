from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from passlib.hash import bcrypt

from api.models.user import User, FORBIDDEN_FIELDS, ALLOWED_FIELDS
from api.repository.user_repo import (
    create_user_repo, get_user_by_id, is_email_taken, is_username_taken, 
    delete_user_by_id, updata_user_by_id
)
from api.schemas import UserCreate, UserUpdatePatch, UserUpdatePut


async def register_user(user_data: UserCreate, db: AsyncSession) -> User:
    email = user_data.email.lower()
    if await is_email_taken(db, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    if await is_username_taken(db, user_data.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    return await create_user_repo(user_data, db)


async def register_get(id: UUID, db: AsyncSession) -> User:
    user = await get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def has_changes(user: User, data: dict) -> bool:
    for key, new_value in data.items():
        if not hasattr(user, key):
            continue 
        old_value = getattr(user, key)

        if key == "password":
            if not bcrypt.verify(new_value, old_value):
                return True
        elif old_value != new_value:
            return True
    return False

async def register_patch(id: UUID, updata: UserUpdatePatch, db: AsyncSession) -> User:
    user = await get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    data_dict = updata.model_dump(exclude_unset=True)

    for key, value in data_dict.items():
        if key in FORBIDDEN_FIELDS:
            raise HTTPException(status_code=403, detail=f"Field '{key}' is not allowed to be updated")
        if key not in ALLOWED_FIELDS:
            raise HTTPException(status_code=400, detail=f"Field '{key}' cannot be updated")

    if not await has_changes(user, data_dict):
        return JSONResponse(
            status_code=200,
            content={"message": "No changes detected", "data": {"id": str(user.id)}}
        )

    for key, value in data_dict.items():
        if key == "password":
            value = bcrypt.hash(value)
        setattr(user, key, value)

    return await updata_user_by_id(user, db)

async def register_put(id: UUID, updata: UserUpdatePut, db: AsyncSession) -> User:
    user = await get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    data_dict = updata.model_dump()

    if not await has_changes(user, data_dict):
        return JSONResponse(
            status_code=200,
            content={"message": "No changes detected", "data": {"id": str(user.id)}}
        )

    for key, value in data_dict.items():
        if key == "password":
            value = bcrypt.hash(value)
        setattr(user, key, value)

    return await updata_user_by_id(user, db)

async def register_delete(id: UUID, db: AsyncSession) -> User:
    user = await get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await delete_user_by_id(user, db)
