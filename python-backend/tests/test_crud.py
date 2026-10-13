import pytest

from usecases.read_crud import get_record, list_records


class FakeCRUDRepository:
    def __init__(self):
        self.records = [
            {
                "id": 1,
                "email": "user1@example.com",
                "first_name": "User",
                "last_name": "One"
            },
            {
                "id": 2,
                "email": "user2@example.com",
                "first_name": "User",
                "last_name": "Two"
            }
        ]

    def get_one(self, record_id: int) -> dict | None:
        for record in self.records:
            if record["id"] == record_id:
                return record
        return None

    def get_list(self, page: int, page_size: int) -> list[dict]:
        start = (page - 1) * page_size
        end = start + page_size
        return self.records[start:end]


def test_get_record_success():
    repository = FakeCRUDRepository()

    result = get_record(1, repository)

    assert result["id"] == 1
    assert result["email"] == "user1@example.com"


def test_get_record_not_found():
    repository = FakeCRUDRepository()

    result = get_record(999, repository)

    assert result is None


def test_get_record_invalid_id():
    repository = FakeCRUDRepository()

    with pytest.raises(ValueError, match="Record ID must be positive"):
        get_record(0, repository)


def test_list_records_pagination():
    repository = FakeCRUDRepository()

    result = list_records(
        page=2,
        page_size=1,
        repository=repository
    )

    assert len(result) == 1
    assert result[0]["id"] == 2


def test_list_records_invalid_page():
    repository = FakeCRUDRepository()

    with pytest.raises(ValueError, match="Page must be at least 1"):
        list_records(0, 10, repository)


def test_list_records_invalid_page_size():
    repository = FakeCRUDRepository()

    with pytest.raises(ValueError, match="Page size must be between 1 and 100"):
        list_records(1, 101, repository)