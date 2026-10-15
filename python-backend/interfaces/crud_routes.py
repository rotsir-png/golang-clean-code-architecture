from fastapi import APIRouter, Depends, HTTPException

from interfaces.auth_routes import get_current_user
from infrastructure.crud_repository import PostgresUserCRUDRepository
from infrastructure.permission_repository import PostgresPermissionRepository
from usecases.read_crud import get_record, list_records


router = APIRouter()


@router.get("/crud/users/describe")
def describe_users(current_user=Depends(get_current_user)):
    permission_repository = PostgresPermissionRepository()

    allowed = permission_repository.has_permission(
        user_id=current_user["id"],
        permission="users:read_all"
    )

    if not allowed:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    repository = PostgresUserCRUDRepository()

    return {
        "table": "users",
        "columns": repository.describe()
    }


@router.get("/crud/users/{user_id}")
def read_user(
    user_id: int,
    current_user=Depends(get_current_user)
):
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's profile"
        )

    repository = PostgresUserCRUDRepository()

    try:
        user = get_record(
            record_id=user_id,
            repository=repository
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.get("/crud/users")
def read_users(
    page: int = 1,
    page_size: int = 10,
    current_user=Depends(get_current_user)
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be at least 1"
        )

    if page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=400,
            detail="Page size must be between 1 and 100"
        )

    permission_repository = PostgresPermissionRepository()

    can_read_all = permission_repository.has_permission(
        user_id=current_user["id"],
        permission="users:read_all"
    )

    if can_read_all:
        repository = PostgresUserCRUDRepository()

        users = list_records(
            page=page,
            page_size=page_size,
            repository=repository
        )

        return {
            "page": page,
            "page_size": page_size,
            "data": users
        }

    users = [current_user]

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "page": page,
        "page_size": page_size,
        "total": 1,
        "data": users[start:end]
    }