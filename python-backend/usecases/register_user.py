from typing import Callable

from domain.user import User
from domain.user_repository import UserRepository


def register_user(
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    repository: UserRepository,
    hash_password: Callable[[str], str]
) -> User:

    if len(password) < 8:
        raise ValueError(
            "Password must be at least 8 characters"
        )

    hashed_password = hash_password(password)

    user_id = repository.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password_hash=hashed_password
    )

    return User(
        id=user_id,
        email=email,
        first_name=first_name,
        last_name=last_name
    )