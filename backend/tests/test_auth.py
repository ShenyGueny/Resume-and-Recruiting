from .conftest import register, auth_headers


def test_register_returns_token(client):
    r = client.post("/auth/register", json={"email": "a@test.com", "password": "pass1234"})
    assert r.status_code == 201
    assert "access_token" in r.json()


def test_register_duplicate_email_rejected(client):
    client.post("/auth/register", json={"email": "a@test.com", "password": "pass1234"})
    r = client.post("/auth/register", json={"email": "a@test.com", "password": "pass1234"})
    assert r.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"email": "a@test.com", "password": "pass1234"})
    r = client.post("/auth/login", json={"email": "a@test.com", "password": "pass1234"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "a@test.com", "password": "pass1234"})
    r = client.post("/auth/login", json={"email": "a@test.com", "password": "wrongpassword"})
    assert r.status_code == 401


def test_login_unknown_email(client):
    r = client.post("/auth/login", json={"email": "ghost@test.com", "password": "pass1234"})
    assert r.status_code == 401


def test_get_me_authenticated(client):
    token = register(client, "me@test.com")
    r = client.get("/auth/me", headers=auth_headers(token))
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "me@test.com"
    assert "id" in data


def test_get_me_unauthenticated(client):
    r = client.get("/auth/me")
    assert r.status_code == 403


def test_update_api_key_stores_hint(client):
    token = register(client, "key@test.com")
    r = client.put(
        "/auth/api-key",
        json={"api_key": "sk-ant-abcdefgh1234"},
        headers=auth_headers(token),
    )
    assert r.status_code == 200
    data = r.json()
    assert data["api_key_hint"] == "...1234"
    assert "api_key_encrypted" not in data
