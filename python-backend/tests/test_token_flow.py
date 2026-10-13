from fastapi.testclient import TestClient

import main
from infrastructure.jwt_service import (
    create_refresh_token,
    verify_refresh_token,
)

client = TestClient(main.app)


class FakeRefreshTokenRepository:
    def __init__(self):
        self.active_tokens = set()

    def save_token(self, user_id, token, expires_at):
        self.active_tokens.add((user_id, token))

    def is_token_active(self, token, user_id):
        return (user_id, token) in self.active_tokens

    def revoke_token(self, token, user_id):
        key = (user_id, token)

        if key not in self.active_tokens:
            return False

        self.active_tokens.remove(key)
        return True

    def rotate_token(self, old_token, new_token, user_id, expires_at):
        old_key = (user_id, old_token)

        if old_key not in self.active_tokens:
            return False

        self.active_tokens.remove(old_key)
        self.active_tokens.add((user_id, new_token))
        return True


class FakeUserRepository:
    def get_user_by_id(self, user_id):
        if user_id == 1:
            return {
                "id": 1,
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
            }
        return None


def test_refresh_rotation_and_logout(monkeypatch):
    fake_tokens = FakeRefreshTokenRepository()

    monkeypatch.setattr(
        main,
        "PostgresRefreshTokenRepository",
        lambda: fake_tokens,
    )
def test_logout_invalid_token(monkeypatch):
    fake_tokens = FakeRefreshTokenRepository()

    monkeypatch.setattr(
        main,
        "PostgresRefreshTokenRepository",
        lambda: fake_tokens,
    )

    response = client.post(
        "/users/logout",
        json={"refresh_token": "invalid-token"},
    )

    assert response.status_code == 401


def test_refresh_token_type():
    token = create_refresh_token(1)

    assert verify_refresh_token(token) == 1