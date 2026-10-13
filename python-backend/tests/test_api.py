from fastapi.testclient import TestClient

from main import app, get_current_user


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_profile_without_token():
    response = client.get("/users/profile")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_profile_with_fake_user():
    fake_user = {
        "id": 1,
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    }

    app.dependency_overrides[get_current_user] = lambda: fake_user

    try:
        response = client.get("/users/profile")

        assert response.status_code == 200
        assert response.json() == fake_user

    finally:
        app.dependency_overrides.clear()