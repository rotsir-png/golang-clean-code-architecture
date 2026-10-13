from typing import Protocol


class UserRepository(Protocol):

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str
    ) -> int:
        ...

    def get_user_by_email(self, email: str) -> dict | None:
        ...

    def get_user_by_id(self, user_id: int) -> dict | None:
        ...