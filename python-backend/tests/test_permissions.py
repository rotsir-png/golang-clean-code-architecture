from fastapi.testclient import TestClient

import main
from interfaces import auth_routes, crud_routes


client = TestClient(main.app)


FAKE_USER = {
    "id": 1,
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
}


class FakePermissionRepository:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin

    def has_permission(self, user_id, permission):
        return self.is_admin and permission == "users:read_all"


class FakeCRUDRepository:
    def get_list(self, page, page_size):
        return [
            FAKE_USER,
            {
                "id": 2,
                "email": "other@example.com",
                "first_name": "Other",
                "last_name": "User",
            },
        ]


def test_regular_user_sees_only_self(monkeypatch):
    monkeypatch.setattr(
        crud_routes,
        "PostgresPermissionRepository",
        lambda: FakePermissionRepository(is_admin=False),
    )

    main.app.dependency_overrides[auth_routes.get_current_user] = lambda: FAKE_USER

    try:
        response = client.get("/crud/users")

        assert response.status_code == 200
        assert response.json()["data"] == [FAKE_USER]
    finally:
        main.app.dependency_overrides.clear()


def test_admin_can_list_users(monkeypatch):
    monkeypatch.setattr(
        crud_routes,
        "PostgresPermissionRepository",
        lambda: FakePermissionRepository(is_admin=True),
    )

    monkeypatch.setattr(
        crud_routes,
        "PostgresUserCRUDRepository",
        FakeCRUDRepository,
    )

    main.app.dependency_overrides[auth_routes.get_current_user] = lambda: FAKE_USER

    try:
        response = client.get("/crud/users")

        assert response.status_code == 200
        assert len(response.json()["data"]) == 2
    finally:
        main.app.dependency_overrides.clear()


def test_invalid_pagination(monkeypatch):
    monkeypatch.setattr(
        crud_routes,
        "PostgresPermissionRepository",
        lambda: FakePermissionRepository(),
    )

    main.app.dependency_overrides[auth_routes.get_current_user] = lambda: FAKE_USER

    try:
        response = client.get("/crud/users?page=0")
        assert response.status_code == 400

        response = client.get("/crud/users?page_size=101")
        assert response.status_code == 400
    finally:
        main.app.dependency_overrides.clear()