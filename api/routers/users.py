# api/routers/users.py
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Union

from api.db.session import get_session as default_session  # ✅ 設定 alias
from api.schemas import (
    UserCreate, UserResponse, UserUpdatePatch,
    UserUpdatePut
)
from api.services.user import (
    register_user, register_get, register_delete, 
    register_patch, register_put
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
 
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(default_session)):
    new_user = await register_user(user, db)
    
    return new_user

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: UUID, db: AsyncSession = Depends(default_session)):
    user = await register_get(id, db) 

    return user 

@router.patch("/{id}", response_model=UserResponse)
async def update_user_patch(id: UUID, updata: UserUpdatePatch, db: AsyncSession = Depends(default_session)) -> Union[UserResponse, dict]:
    updated_user = await register_patch(id, updata,  db)
    
    return updated_user

@router.put("/{id}", response_model=UserResponse)
async def update_user_put(id: UUID, updata: UserUpdatePut, db: AsyncSession = Depends(default_session)) -> Union[UserResponse, dict]:
    updated_user = await register_put(id, updata,  db)
    
    return updated_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID, db: AsyncSession = Depends(default_session)) -> Response:
    await register_delete(id, db)


# 🔧 重點技巧：用 alias 取代直寫函式
# ✅ 目標是：
# 保留正式環境的 Depends(get_session) 行為，但又能讓測試時的 dependency_overrides 套用成功。
# 也就是：
#     ✅ 正式環境：正常使用 get_session（MySQL）
#     ✅ 測試環境：自動被 TestClient 的 app.dependency_overrides[get_session] = ... 覆蓋掉，改用 SQLite（或其他測試 session）
# 💡 為什麼這樣就能讓 dependency_overrides[get_session] 生效？
#     因為 Python 是依據「函式的物件位置」來比對的，不是比名字。