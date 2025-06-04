from sqlalchemy import select
from api.models.user import User
from uuid import UUID

async def assert_response(user_id, user_username, user_email, session):
    stmt = select(User).where(User.id == UUID(user_id))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    assert user is not None, f"使用者 {user_id} 不存在於資料庫中"
    assert user.username == user_username, f"使用者 {user_id} 的 username 不正確"
    assert user.email == user_email, f"使用者 {user_id} 的 email 不正確"


async def assert_response_delete(user_id, session):
    stmt = select(User).where(User.id == UUID(user_id))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    assert user is None, f"使用者 {user_id} 還存在於資料庫中"
