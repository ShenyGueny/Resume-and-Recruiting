from unittest.mock import patch, MagicMock
from .conftest import register, auth_headers
from app.schemas.pipeline import (
    ExtractionResult, MatchResult, GeneratedContent, ScoreBreakdown, PipelineContent,
)

APP_PAYLOAD = {
    "company_name": "Acme Corp",
    "job_title": "Software Engineer",
    "job_description": "We need a Python developer with FastAPI and PostgreSQL experience.",
    "status": "saved",
}

PROFILE_PAYLOAD = {
    "experience": [{"title": "Backend Engineer", "company": "StartupX", "years": 3}],
    "education": [{"degree": "BS Computer Science", "school": "State U"}],
    "skills": ["Python", "FastAPI", "SQL"],
}

MOCK_PIPELINE_RESULT = (
    78.5,
    PipelineContent(
        extraction=ExtractionResult(
            required_skills=["Python", "FastAPI", "PostgreSQL"],
            preferred_skills=["Docker"],
            responsibilities=["Build REST APIs", "Design schemas"],
            experience_level="mid",
        ),
        match=MatchResult(
            matched_skills=["Python", "FastAPI"],
            missing_skills=["PostgreSQL"],
            match_percentage=66.7,
        ),
        generated=GeneratedContent(
            tailored_bullets=["Built scalable REST APIs using FastAPI and Python"],
            summary="Experienced backend engineer with strong Python and FastAPI skills.",
        ),
        score_breakdown=ScoreBreakdown(skills=80.0, experience=75.0, education=70.0),
    ),
)


def _setup(client):
    token = register(client, "pipe@test.com")
    client.put("/auth/api-key", json={"api_key": "sk-ant-test1234"}, headers=auth_headers(token))
    client.put("/profile", json=PROFILE_PAYLOAD, headers=auth_headers(token))
    app = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token)).json()
    return token, app["id"]


def test_tailor_no_api_key(client):
    token = register(client, "pipe@test.com")
    client.put("/profile", json=PROFILE_PAYLOAD, headers=auth_headers(token))
    app = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token)).json()
    r = client.post("/pipeline/tailor", json={"application_id": app["id"]}, headers=auth_headers(token))
    assert r.status_code == 400
    assert "API key" in r.json()["detail"]


def test_tailor_no_profile(client):
    token = register(client, "pipe@test.com")
    client.put("/auth/api-key", json={"api_key": "sk-ant-test1234"}, headers=auth_headers(token))
    app = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token)).json()
    r = client.post("/pipeline/tailor", json={"application_id": app["id"]}, headers=auth_headers(token))
    assert r.status_code == 400
    assert "profile" in r.json()["detail"].lower()


def test_tailor_application_not_found(client):
    token = register(client, "pipe@test.com")
    client.put("/auth/api-key", json={"api_key": "sk-ant-test1234"}, headers=auth_headers(token))
    client.put("/profile", json=PROFILE_PAYLOAD, headers=auth_headers(token))
    r = client.post(
        "/pipeline/tailor",
        json={"application_id": "00000000-0000-0000-0000-000000000000"},
        headers=auth_headers(token),
    )
    assert r.status_code == 404


def test_tailor_no_job_description(client):
    token = register(client, "pipe@test.com")
    client.put("/auth/api-key", json={"api_key": "sk-ant-test1234"}, headers=auth_headers(token))
    client.put("/profile", json=PROFILE_PAYLOAD, headers=auth_headers(token))
    app = client.post(
        "/applications",
        json={"company_name": "Acme", "job_title": "Engineer"},
        headers=auth_headers(token),
    ).json()
    r = client.post("/pipeline/tailor", json={"application_id": app["id"]}, headers=auth_headers(token))
    assert r.status_code == 400
    assert "job description" in r.json()["detail"].lower()


@patch("app.routers.pipeline.run_pipeline", return_value=MOCK_PIPELINE_RESULT)
def test_tailor_success(mock_run, client):
    token, app_id = _setup(client)
    r = client.post("/pipeline/tailor", json={"application_id": app_id}, headers=auth_headers(token))
    assert r.status_code == 200
    data = r.json()
    assert data["ats_score"] == 78.5
    assert data["document_type"] == "resume"
    assert "content" in data
    assert data["content"]["generated"]["summary"] != ""
    assert len(data["content"]["generated"]["tailored_bullets"]) > 0


@patch("app.routers.pipeline.run_pipeline", return_value=MOCK_PIPELINE_RESULT)
def test_tailor_stores_document(mock_run, client):
    token, app_id = _setup(client)
    client.post("/pipeline/tailor", json={"application_id": app_id}, headers=auth_headers(token))
    r = client.get(f"/pipeline/documents/{app_id}", headers=auth_headers(token))
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["ats_score"] == 78.5


@patch("app.routers.pipeline.run_pipeline", return_value=MOCK_PIPELINE_RESULT)
def test_tailor_multiple_runs_accumulate(mock_run, client):
    token, app_id = _setup(client)
    client.post("/pipeline/tailor", json={"application_id": app_id}, headers=auth_headers(token))
    client.post("/pipeline/tailor", json={"application_id": app_id}, headers=auth_headers(token))
    r = client.get(f"/pipeline/documents/{app_id}", headers=auth_headers(token))
    assert len(r.json()) == 2


def test_list_documents_wrong_user(client):
    token_a = register(client, "a@test.com")
    token_b = register(client, "b@test.com")
    client.put("/auth/api-key", json={"api_key": "sk-ant-test1234"}, headers=auth_headers(token_a))
    client.put("/profile", json=PROFILE_PAYLOAD, headers=auth_headers(token_a))
    app = client.post("/applications", json=APP_PAYLOAD, headers=auth_headers(token_a)).json()
    r = client.get(f"/pipeline/documents/{app['id']}", headers=auth_headers(token_b))
    assert r.status_code == 404
