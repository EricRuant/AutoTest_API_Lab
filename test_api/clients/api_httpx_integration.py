from httpx import AsyncClient   #

# 發送 POST 請求建立使用者
async def async_response_post(data):
    url = f"/users/"  
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        return await client.post(url, json=data)
    
# 取得使用者資訊
async def async_response_get(user_id):
    url = f"/users/{user_id}"  
    
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        return await client.get(url)

# 使用 PUT 完整更新    
async def async_response_put(user_id, data):
    url = f"/users/{user_id}"  
    
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        return await client.put(url, json=data)

# 使用 PATCH 部分更新
async def async_response_patch(user_id, data):
    url = f"/users/{user_id}"  
    
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        return await client.patch(url, json=data)
    
# 使用 DELETE 刪除使用者
async def async_response_delete(user_id):
    url = f"/users/{user_id}"  
    
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        return await client.delete(url)
