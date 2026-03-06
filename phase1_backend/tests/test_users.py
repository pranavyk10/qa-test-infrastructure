import pytest

@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_create_user(client):
    resp = await client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "alice@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_duplicate_user(client):
    await client.post("/users/", json={"name": "Bob", "email": "bob@example.com"})
    resp = await client.post("/users/", json={"name": "Bob", "email": "bob@example.com"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    resp = await client.get("/users/9999")
    assert resp.status_code == 404

@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_and_fetch_user(client):
    resp = await client.post("/users/", json={"name": "Charlie", "email": "charlie@example.com"})
    assert resp.status_code == 201
    user_id = resp.json()["id"]
    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Charlie"

@pytest.mark.asyncio
async def test_get_user_invalid_id_type(client):
    resp = await client.get("/users/abc")
    assert resp.status_code == 422  # FastAPI validation error
