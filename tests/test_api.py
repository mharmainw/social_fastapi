from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import database


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(test_engine, "connect")
def configure_sqlite(dbapi_connection, connection_record):
    dbapi_connection.create_function(
        "now",
        0,
        lambda: datetime.now(timezone.utc).isoformat(),
    )
    dbapi_connection.execute("PRAGMA foreign_keys=ON")


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

database.engine = test_engine
database.SessionLocal = TestingSessionLocal

from app import models  # noqa: E402
from app.main import app  # noqa: E402


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[database.get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    models.Base.metadata.drop_all(bind=test_engine)
    models.Base.metadata.create_all(bind=test_engine)
    yield


def create_user(email="owner@example.com", password="Password123!"):
    response = client.post(
        "/users/",
        json={"email": email, "password": password},
    )
    assert response.status_code == 201
    return response.json()


def login(email="owner@example.com", password="Password123!"):
    response = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_post(headers, title="Test post"):
    response = client.post(
        "/posts/",
        headers=headers,
        json={
            "title": title,
            "content": "Test content",
            "published": True,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_docs_and_openapi_are_available():
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200
    assert client.get("/").status_code == 404


def test_user_creation_and_authentication():
    user = create_user()

    assert user["email"] == "owner@example.com"
    assert "password" not in user
    assert client.get(f"/users/{user['id']}").status_code == 200

    bad_login = client.post(
        "/login",
        data={"username": "owner@example.com", "password": "wrong"},
    )
    assert bad_login.status_code == 403

    headers = login()
    assert headers["Authorization"].startswith("Bearer ")
    assert client.get("/posts/", headers=headers).status_code == 200


def test_posts_require_authentication():
    assert client.get("/posts/").status_code == 401
    assert client.post(
        "/posts/",
        json={"title": "Denied", "content": "Denied", "published": True},
    ).status_code == 401


def test_post_crud_and_update_persistence():
    create_user()
    headers = login()
    post = create_post(headers)
    post_id = post["id"]

    fetched = client.get(f"/posts/{post_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["Post"]["id"] == post_id
    assert fetched.json()["votes"] == 0

    updated = client.put(
        f"/posts/{post_id}",
        headers=headers,
        json={
            "title": "Updated title",
            "content": "Updated content",
            "published": False,
        },
    )
    assert updated.status_code == 200

    persisted = client.get(f"/posts/{post_id}", headers=headers)
    assert persisted.status_code == 200
    assert persisted.json()["Post"]["title"] == "Updated title"
    assert persisted.json()["Post"]["published"] is False

    assert client.delete(f"/posts/{post_id}", headers=headers).status_code == 204
    assert client.get(f"/posts/{post_id}", headers=headers).status_code == 404


def test_post_ownership_is_enforced():
    create_user()
    owner_headers = login()
    post = create_post(owner_headers)

    create_user("other@example.com")
    other_headers = login("other@example.com")

    update = client.put(
        f"/posts/{post['id']}",
        headers=other_headers,
        json={
            "title": "Unauthorized",
            "content": "Unauthorized",
            "published": True,
        },
    )
    assert update.status_code == 403
    assert client.delete(
        f"/posts/{post['id']}",
        headers=other_headers,
    ).status_code == 403
    assert client.get(
        f"/posts/{post['id']}",
        headers=owner_headers,
    ).status_code == 200


def test_vote_lifecycle_and_count():
    create_user()
    owner_headers = login()
    post = create_post(owner_headers)

    create_user("voter@example.com")
    voter_headers = login("voter@example.com")
    vote = {"post_id": post["id"], "dir": 1}

    assert client.post("/vote/", headers=voter_headers, json=vote).status_code == 201

    fetched = client.get(f"/posts/{post['id']}", headers=owner_headers)
    assert fetched.status_code == 200
    assert fetched.json()["votes"] == 1

    assert client.post(
        "/vote/",
        headers=voter_headers,
        json=vote,
    ).status_code == 409

    assert client.post(
        "/vote/",
        headers=voter_headers,
        json={"post_id": post["id"], "dir": 0},
    ).status_code == 201

    fetched = client.get(f"/posts/{post['id']}", headers=owner_headers)
    assert fetched.status_code == 200
    assert fetched.json()["votes"] == 0

    assert client.post(
        "/vote/",
        headers=voter_headers,
        json={"post_id": post["id"], "dir": 0},
    ).status_code == 404
