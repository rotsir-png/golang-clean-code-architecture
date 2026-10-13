from domain.crud_repository import CRUDRepository


def get_record(
    record_id: int,
    repository: CRUDRepository
) -> dict | None:
    if record_id <= 0:
        raise ValueError("Record ID must be positive")

    return repository.get_one(record_id)


def list_records(
    page: int,
    page_size: int,
    repository: CRUDRepository
) -> list[dict]:
    if page < 1:
        raise ValueError("Page must be at least 1")

    if page_size < 1 or page_size > 100:
        raise ValueError("Page size must be between 1 and 100")

    return repository.get_list(page, page_size)