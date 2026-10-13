import pytest

from usecases.register_user import register_user
from usecases.login_user import login_user
from infrastructure.password_hasher import hash_password, verify_password


class FakeUserRepository:
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str
    ) -> int:
        user_id = self.next_id
        self.next_id += 1

        self.users[email] = {
            "id": user_id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password_hash": password_hash
        }

        return user_id

    def get_user_by_email(self, email: str) -> dict | None:
        return self.users.get(email)


def test_register_user_success():
    repository = FakeUserRepository()

    user = register_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="Test1234",
        repository=repository,
        hash_password=hash_password
    )

    assert user.id == 1
    assert user.email == "test@example.com"
    assert repository.users["test@example.com"]["password_hash"] != "Test1234"


def test_register_user_short_password():
    repository = FakeUserRepository()

    with pytest.raises(ValueError, match="Password must be at least 8 characters"):
        register_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="123",
            repository=repository,
            hash_password=hash_password
        )


def test_login_user_success():
    repository = FakeUserRepository()

    repository.create_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password_hash=hash_password("Test1234")
    )

    user = login_user(
        email="test@example.com",
        password="Test1234",
        repository=repository,
        verify_password=verify_password
    )

    assert user["email"] == "test@example.com"


def test_login_user_wrong_password():
    repository = FakeUserRepository()

    repository.create_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password_hash=hash_password("Test1234")
    )

    with pytest.raises(ValueError, match="Invalid email or password"):
        login_user(
            email="test@example.com",
            password="WrongPassword",
            repository=repository,
            verify_password=verify_password
        )