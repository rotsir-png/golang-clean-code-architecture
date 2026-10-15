from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

from datetime import datetime, timedelta, timezone

from usecases.register_user import register_user
from usecases.login_user import login_user

from infrastructure.user_repository import PostgresUserRepository
from infrastructure.refresh_token_repository import PostgresRefreshTokenRepository
from infrastructure.password_hasher import hash_password, verify_password
from infrastructure.jwt_service import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
)


router = APIRouter()
security = HTTPBearer(auto_error=False)


class RegisterRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security)
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    try:
        user_id = verify_access_token(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    repository = PostgresUserRepository()
    user = repository.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@router.post("/users/register", status_code=201)
def register(request: RegisterRequest):
    repository = PostgresUserRepository()

    try:
        return register_user(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            password=request.password,
            repository=repository,
            hash_password=hash_password
        )
    except ValueError as error:
        message = str(error)

        raise HTTPException(
            status_code=409 if message == "Email already registered" else 400,
            detail=message
        )


@router.post("/users/login")
def login(request: LoginRequest):
    repository = PostgresUserRepository()

    try:
        user = login_user(
            email=request.email,
            password=request.password,
            repository=repository,
            verify_password=verify_password
        )

        access_token = create_access_token(user["id"])
        refresh_token = create_refresh_token(user["id"])

        token_repository = PostgresRefreshTokenRepository()
        token_repository.save_token(
            user_id=user["id"],
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )

        return {
            "message": "Login successful",
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))


@router.get("/users/profile")
def get_profile(user=Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"]
    }


@router.post("/users/refresh-token")
def refresh_access_token(request: RefreshTokenRequest):
    try:
        user_id = verify_refresh_token(request.refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    repository = PostgresUserRepository()
    user = repository.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)

    token_repository = PostgresRefreshTokenRepository()
    rotated = token_repository.rotate_token(
        old_token=request.refresh_token,
        new_token=new_refresh_token,
        user_id=user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )

    if not rotated:
        raise HTTPException(
            status_code=401,
            detail="Refresh token is revoked or not found"
        )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/users/logout")
def logout(request: LogoutRequest):
    try:
        user_id = verify_refresh_token(request.refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    token_repository = PostgresRefreshTokenRepository()
    revoked = token_repository.revoke_token(
        token=request.refresh_token,
        user_id=user_id
    )

    if not revoked:
        raise HTTPException(
            status_code=401,
            detail="Refresh token already revoked or not found"
        )

    return {"message": "Logout successful"}