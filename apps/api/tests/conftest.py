# Shared pytest fixtures for all tests.
# Each test gets an isolated DB session (rolled back after) and a test client
# wired to that session so tests never interfere with each other.
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Force local storage backend before any app imports resolve settings
os.environ.setdefault("OBJECT_STORAGE_PROVIDER", "local")

from app.config import settings
from app.core.security import hash_password
from app.db.base import Base, import_all_models
from app.db.session import get_db
from app.main import app
from app.storage.factory import get_storage
from app.models.organization import Organization
from app.models.project import CriticalityLevel, Industry, Project
from app.models.user import User, UserRole

TEST_DATABASE_URL = settings.database_url.replace("/assurance_os", "/assurance_os_test")

import_all_models()

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(autouse=True)
def reset_storage_cache():
    get_storage.cache_clear()
    yield
    get_storage.cache_clear()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# --- Reusable data fixtures ---

@pytest.fixture
def demo_org(db):
    org = Organization(name="Test Org", industry="defense")
    db.add(org)
    db.flush()
    return org


@pytest.fixture
def demo_user(db, demo_org):
    user = User(
        organization_id=demo_org.id,
        email="test@example.com",
        name="Test User",
        password_hash=hash_password("testpass123"),
        role=UserRole.admin,
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture
def demo_project(db, demo_org):
    project = Project(
        organization_id=demo_org.id,
        name="Test Project",
        industry=Industry.defense,
        criticality_level=CriticalityLevel.high,
    )
    db.add(project)
    db.flush()
    return project


@pytest.fixture
def auth_headers(client, demo_user):
    """Returns Authorization headers for the demo_user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
