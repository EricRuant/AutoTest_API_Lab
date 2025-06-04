# api/models/user.py
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime

from api.db.session import Base 

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# ⛔ 不允許更新的欄位
FORBIDDEN_FIELDS = {"id", "created_at"}

# ✅ 允許更新的欄位
ALLOWED_FIELDS = {"username", "password", "email"}

