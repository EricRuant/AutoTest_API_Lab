# test_api/clients/api_httpx_unit.py
# 匯入 httpx 套件中的非同步用戶端
from httpx import AsyncClient   # 匯入 httpx 的非同步客戶端

# 使用 FastAPI app 僅為型別提示，不要重建 client
from api.api_main import app


# 建立使用者（POST）
async def async_response_post(data: dict, client: AsyncClient):
    """
    呼叫 POST /users/
    用於建立新使用者
    """
    return await client.post("/users/", json=data)

# 取得使用者資訊（GET）
async def async_response_get(user_id: str, client: AsyncClient):
    """
    呼叫 GET /users/{id}
    根據 ID 取得使用者資訊
    """
    return await client.get(f"/users/{user_id}")

# 完整更新使用者（PUT）
async def async_response_put(user_id: str, data: dict, client: AsyncClient):
    """
    呼叫 PUT /users/{id}
    用於整筆覆蓋更新使用者資料
    """
    return await client.put(f"/users/{user_id}", json=data)

# 部分更新使用者（PATCH）
async def async_response_patch(user_id: str, data: dict, client: AsyncClient):
    """
    呼叫 PATCH /users/{id}
    用於部分更新使用者資料
    """
    return await client.patch(f"/users/{user_id}", json=data)

# 刪除使用者（DELETE）
async def async_response_delete(user_id: str, client: AsyncClient):
    """
    呼叫 DELETE /users/{id}
    用於刪除指定使用者
    """
    return await client.delete(f"/users/{user_id}")
