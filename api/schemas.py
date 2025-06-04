# api/schemas.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime

class UserUpdatePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")  # ✅ 新版設定方式

    username: Optional[str] = Field(default=None, min_length=3)
    password: Optional[str] = Field(default=None, min_length=6)
    email: Optional[EmailStr] = Field(default=None)
    admin: Optional[bool] = None  # 🔸暫時加入，只為了測試
    id: Optional[UUID] = None   # 🔸暫時加入，只為了測試
    created_at: Optional[datetime] = None   # 🔸暫時加入，只為了測試
    
class UserUpdatePut(BaseModel):
    model_config = ConfigDict(extra="forbid")  # ✅ 新版設定方式

    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    email: EmailStr
 

# extra="forbid"（預設）：多欄位直接報錯
# extra="ignore"：忽略多餘欄位
# extra="allow"：保留進去但不做驗證