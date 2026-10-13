import secrets
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()


def create_access_token(user_id: int) -> str:
    secret_key = os.environ["KHAOJAI_JWT_SECRET"]

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")


def verify_access_token(token: str) -> int:
    secret_key = os.environ["KHAOJAI_JWT_SECRET"]

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"]
        )

        if payload.get("type") != "access":
            raise ValueError("Invalid token type")

        return int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        raise ValueError("Invalid or expired access token")

def create_refresh_token(user_id: int) -> str:
    secret_key = os.environ["KHAOJAI_JWT_SECRET"]

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": secrets.token_urlsafe(24),
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")

def verify_refresh_token(token: str) -> int:
    secret_key = os.environ["KHAOJAI_JWT_SECRET"]

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"]
        )

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        return int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        raise ValueError("Invalid or expired refresh token")