import pytest


@pytest.mark.anyio
async def test_register_success(async_client):
    r = await async_client.post(
        "/auth/register",
        json={"email": "test@email.com", "password": "Password123"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "test@email.com"
    assert data["role"] == "user"
    assert "id" in data
    assert "password_hash" not in data


@pytest.mark.anyio
async def test_register_duplicate_email(async_client):
    await async_client.post(
        "/auth/register",
        json={"email": "duplicate@email.com", "password": "Password123"},
    )
    r = await async_client.post(
        "/auth/register",
        json={"email": "duplicate@email.com", "password": "Password123"},
    )
    assert r.status_code == 409


@pytest.mark.anyio
async def test_login_success(async_client):
    await async_client.post(
        "/auth/register",
        json={"email": "login@email.com", "password": "Password123"},
    )
    r = await async_client.post(
        "/auth/login",
        data={"username": "login@email.com", "password": "Password123"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_wrong_password(async_client):
    await async_client.post(
        "/auth/register",
        json={"email": "wrongpass@email.com", "password": "Password123"},
    )
    r = await async_client.post(
        "/auth/login",
        data={"username": "wrongpass@email.com", "password": "WrongPassword"},
    )
    assert r.status_code == 401


@pytest.mark.anyio
async def test_me_success(async_client):
    await async_client.post(
        "/auth/register",
        json={"email": "me@email.com", "password": "Password123"},
    )
    login = await async_client.post(
        "/auth/login",
        data={"username": "me@email.com", "password": "Password123"},
    )
    token = login.json()["access_token"]
    r = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["email"] == "me@email.com"


@pytest.mark.anyio
async def test_me_no_token(async_client):
    r = await async_client.get("/auth/me")
    assert r.status_code == 401


@pytest.mark.anyio
async def test_me_invalid_token(async_client):
    r = await async_client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert r.status_code == 401