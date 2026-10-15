from psycopg.errors import UniqueViolation
from infrastructure.database import get_connection


class PostgresUserRepository:

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str
    ) -> int:

        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO users (
                            email,
                            first_name,
                            last_name,
                            password_hash
                        )
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            email,
                            first_name,
                            last_name,
                            password_hash
                        )
                    )

                    user_id = cursor.fetchone()[0]

            return user_id

        except UniqueViolation as error:
            raise ValueError("Email already registered") from error
    def get_user_by_email(self, email: str) -> dict | None:

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, email, first_name,
                           last_name, password_hash
                    FROM users
                    WHERE email = %s
                    """,
                    (email,)
                )

                row = cursor.fetchone()

                if row is None:
                    return None

                return {
                    "id": row[0],
                    "email": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "password_hash": row[4]
                }
    def get_user_by_id(self, user_id: int) -> dict | None:

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, email, first_name, last_name
                    FROM users
                    WHERE id = %s
                    """,
                    (user_id,)
                )

                row = cursor.fetchone()

                if row is None:
                    return None

                return {
                    "id": row[0],
                    "email": row[1],
                    "first_name": row[2],
                    "last_name": row[3]
                }