import pytest
import jwt

from infrastructure.jwt_service import (
    create_access_token,
    verify_access_token,
)
import os
from datetime import datetime, timedelta, timezone

def test_valid_token():
    token = create_access_token(1)

    user_id = verify_access_token(token)

    assert user_id == 1


def test_invalid_token():
    with pytest.raises(ValueError, match="Invalid or expired"):
        verify_access_token("this-is-not-a-valid-token")


def test_wrong_token_type():
    import os

    secret_key = os.environ["KHAOJAI_JWT_SECRET"]

    token = jwt.encode(
        {
            "sub": "1",
            "type": "refresh"
        },
        secret_key,
        algorithm="HS256"
    )

    with pytest.raises(ValueError, match="Invalid or expired"):
        verify_access_token(token)

def test_expired_token():
    secret_key = os.environ["KHAOJAI_JWT_SECRET"]

    expired_token = jwt.encode(
        {
            "sub": "1",
            "type": "access",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        secret_key,
        algorithm="HS256"
    )

    with pytest.raises(
        ValueError,
        match="Invalid or expired access token"
    ):
        verify_access_token(expired_token)