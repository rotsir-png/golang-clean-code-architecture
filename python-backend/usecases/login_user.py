from typing import Callable

from domain.user_repository import UserRepository


def login_user(
    email: str,
    password: str,
    repository: UserRepository,
    verify_password: Callable[[str, str], bool]
) -> dict:

    user = repository.get_user_by_email(email)

    if user is None:
        raise ValueError("Invalid email or password")

    if not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid email or password")

    return {
        "id": user["id"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"]
    }