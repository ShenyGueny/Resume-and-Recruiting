from .conftest import register, auth_headers

APP_PAYLOAD = {
    "company_name": "Acme Corp",
    "job_title": "Software Engineer",
    "job_description": "Build great things.",
    "status": "saved",
}


def test_list_applications_empty(client):
    token = register(client, "a@test.com")
    r = client.get("/applications", headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json() == []


def test_create_application(client):
    token = register(client, "a@test.com")
    r = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token))
    assert r.status_code == 201
    data = r.json()
    assert data["company_name"] == "Acme Corp"
    assert data["status"] == "saved"
    assert "id" in data


def test_get_application_by_id(client):
    token = register(client, "a@test.com")
    created = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token)).json()
    r = client.get(f"/applications/{created['id']}", headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_get_application_not_found(client):
    token = register(client, "a@test.com")
    r = client.get(
        "/applications/00000000-0000-0000-0000-000000000000",
        headers=auth_headers(token),
    )
    assert r.status_code == 404


def test_update_application_status(client):
    token = register(client, "a@test.com")
    created = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token)).json()
    r = client.patch(
        f"/applications/{created['id']}",
        json={"status": "applied"},
        headers=auth_headers(token),
    )
    assert r.status_code == 200
    assert r.json()["status"] == "applied"


def test_delete_application(client):
    token = register(client, "a@test.com")
    created = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token)).json()
    r = client.delete(f"/applications/{created['id']}", headers=auth_headers(token))
    assert r.status_code == 204
    r2 = client.get(f"/applications/{created['id']}", headers=auth_headers(token))
    assert r2.status_code == 404


def test_user_isolation(client):
    token_a = register(client, "a@test.com")
    token_b = register(client, "b@test.com")
    client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token_a))
    r = client.get("/applications", headers=auth_headers(token_b))
    assert r.json() == []


def test_kanban_status_transitions(client):
    token = register(client, "a@test.com")
    created = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token)).json()
    app_id = created["id"]
    for status in ("applied", "interviewing", "offer"):
        r = client.patch(
            f"/applications/{app_id}",
            json={"status": status},
            headers=auth_headers(token),
        )
        assert r.status_code == 200
        assert r.json()["status"] == status
