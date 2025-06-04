# 建立資料表
import asyncio
from api.db.session import engine
from api.models.user import User
from api.db.session import Base


# =======================
# 建立資料庫與資料表的主函式
# =======================
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())

# 使用方式說明：
# 為了確保相對路徑正確，請用模組方式執行（不要直接用 python 檔名）
# 正確指令：python -m api.Create_and_Query.api_create_db