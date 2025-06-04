# api/models/user.py
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime

from api.db.session import Base  # 繼承你剛才重構好的 Base

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


# 🔍 說明對照表
# SQLModel	                        SQLAlchemy ORM
# Field(..., primary_key=True)	    mapped_column(..., primary_key=True)
# default_factory=uuid4	            default=uuid4（注意：使用 mapped_column 的寫法）
# table=True	                    改為繼承 Base 並明確指定 __tablename__
# SQLModel	                        改為繼承 Base (DeclarativeBase)