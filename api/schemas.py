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
    model_config = ConfigDict(extra="forbid") 

    username: Optional[str] = Field(default=None, min_length=3)
    password: Optional[str] = Field(default=None, min_length=6)
    email: Optional[EmailStr] = Field(default=None)

    # 🔸暫時加入，只為了測試
    admin: Optional[bool] = None  
    id: Optional[UUID] = None   
    created_at: Optional[datetime] = None  
    
class UserUpdatePut(BaseModel):
    model_config = ConfigDict(extra="forbid")  

    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    email: EmailStr
 
