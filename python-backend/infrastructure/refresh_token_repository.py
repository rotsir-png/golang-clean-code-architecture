import hashlib
from datetime import datetime, timezone

from infrastructure.database import get_connection


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class PostgresRefreshTokenRepository:

    def save_token(
        self,
        user_id: int,
        token: str,
        expires_at: datetime
    ) -> None:
        token_hash = hash_refresh_token(token)

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO refresh_tokens (
                        user_id,
                        token_hash,
                        expires_at
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (user_id, token_hash, expires_at)
                )

    def is_token_active(self, token: str, user_id: int) -> bool:
        token_hash = hash_refresh_token(token)

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1
                    FROM refresh_tokens
                    WHERE token_hash = %s
                      AND user_id = %s
                      AND revoked_at IS NULL
                      AND expires_at > NOW()
                    """,
                    (token_hash, user_id)
                )

                return cursor.fetchone() is not None

    def revoke_token(self, token: str, user_id: int) -> bool:
        token_hash = hash_refresh_token(token)

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE refresh_tokens
                    SET revoked_at = NOW()
                    WHERE token_hash = %s
                      AND user_id = %s
                      AND revoked_at IS NULL
                      AND expires_at > NOW()
                    RETURNING id
                    """,
                    (token_hash, user_id)
                )

                return cursor.fetchone() is not None
    def rotate_token(
        self,
        old_token: str,
        new_token: str,
        user_id: int,
        expires_at: datetime
    ) -> bool:
        old_hash = hash_refresh_token(old_token)
        new_hash = hash_refresh_token(new_token)

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE refresh_tokens
                    SET revoked_at = NOW()
                    WHERE token_hash = %s
                      AND user_id = %s
                      AND revoked_at IS NULL
                      AND expires_at > NOW()
                    RETURNING id
                    """,
                    (old_hash, user_id)
                )

                if cursor.fetchone() is None:
                    return False

                cursor.execute(
                    """
                    INSERT INTO refresh_tokens (
                        user_id,
                        token_hash,
                        expires_at
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (user_id, new_hash, expires_at)
                )

        return True