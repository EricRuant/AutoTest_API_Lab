from fastapi import FastAPI
from api.routers import users
from contextlib import asynccontextmanager

from test_app.db.test_session import get_test_session, engine
# ✅ 覆蓋原本 get_session
from api.db.session import get_session, Base


# ✅ 啟動後自動建立表格
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 正在建立資料表（SQLAlchemy）...")
    async with engine.begin() as conn:
        print(Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("💥 測試結束，刪除資料表（SQLAlchemy）...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(users.router)
    app.dependency_overrides[get_session] = get_test_session
    return app

app = create_app()
