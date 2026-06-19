from .conftest import register, auth_headers

PROFILE = {
    "experience": [{"title": "Engineer", "company": "Acme", "years": 2}],
    "education": [{"degree": "BS Computer Science", "school": "State U"}],
    "skills": ["Python", "SQL", "FastAPI"],
}


def test_get_profile_not_found(client):
    token = register(client, "p@test.com")
    r = client.get("/profile", headers=auth_headers(token))
    assert r.status_code == 404


def test_upsert_profile_creates(client):
    token = register(client, "p@test.com")
    r = client.put("/profile", json=PROFILE, headers=auth_headers(token))
    assert r.status_code == 200
    data = r.json()
    assert data["skills"] == ["Python", "SQL", "FastAPI"]
    assert data["experience"][0]["company"] == "Acme"
    assert "id" in data


def test_upsert_profile_updates_in_place(client):
    token = register(client, "p@test.com")
    client.put("/profile", json=PROFILE, headers=auth_headers(token))
    updated = {**PROFILE, "skills": ["Go", "Kubernetes"]}
    r = client.put("/profile", json=updated, headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["skills"] == ["Go", "Kubernetes"]


def test_get_profile_after_upsert(client):
    token = register(client, "p@test.com")
    client.put("/profile", json=PROFILE, headers=auth_headers(token))
    r = client.get("/profile", headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["education"][0]["degree"] == "BS Computer Science"


def test_profile_unauthenticated(client):
    r = client.get("/profile")
    assert r.status_code == 403
