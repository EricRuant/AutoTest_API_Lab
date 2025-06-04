import re
from uuid import UUID
from test_api.test.unit.helpers.test_user_sql_assertions import (
    assert_response
)

# ISO 8601 格式的正規表達式 
ISO = re.compile(
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?'
)

async def assert_response_success(response, session):
    assert response.status_code == 200
    data = response.json()

    assert "id" in data             
    assert UUID(data["id"])            
    uuid_obj = UUID(data["id"])
    assert uuid_obj.version == 4        

    assert ISO.fullmatch(data["created_at"])  
    assert "password" not in data     

    user_id = data["id"]
    user_email = data["email"]
    user_username = data["username"]
    await assert_response(user_id, user_username, user_email, session)

async def assert_response_fail_404(response):
    assert response.status_code == 404  
    assert response.json()["detail"] == "User not found"

async def assert_response_fail_422(response, user_id):
    assert response.status_code == 422
    details = response.json().get("detail", [])[0]

    assert details["loc"] == ["path", "id"] 
    assert details["type"] == "uuid_parsing"
    assert "uuid" in details["msg"].lower()          
    assert str(user_id) in details["input"]          