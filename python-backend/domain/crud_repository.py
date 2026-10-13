from typing import Protocol


class CRUDRepository(Protocol):

    def get_one(self, record_id: int) -> dict | None:
        ...

    def get_list(
        self,
        page: int,
        page_size: int
    ) -> list[dict]:
        ...