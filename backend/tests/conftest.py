import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography.fernet import Fernet

os.environ["DATABASE_URL"] = "postgresql://ats_user:ats_password@localhost:5432/ats_db"
os.environ["SECRET_KEY"] = "a" * 64
os.environ["ENCRYPTION_KEY"] = Fernet.generate_key().decode()
os.environ["ENVIRONMENT"] = "dev"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: registers all models with Base
from app.database import Base, engine, get_db
from app.main import app

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def register(client, email="test@example.com", password="password123"):
    r = client.post("/auth/register", json={"email": email, "password": password})
    return r.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}
