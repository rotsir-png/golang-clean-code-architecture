from infrastructure.database import get_connection


class PostgresUserCRUDRepository:

    def get_one(self, record_id: int) -> dict | None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, email, first_name, last_name
                    FROM users
                    WHERE id = %s
                    """,
                    (record_id,)
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

    def get_list(
        self,
        page: int,
        page_size: int
    ) -> list[dict]:
        offset = (page - 1) * page_size

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, email, first_name, last_name
                    FROM users
                    ORDER BY id
                    LIMIT %s OFFSET %s
                    """,
                    (page_size, offset)
                )

                rows = cursor.fetchall()

                return [
                    {
                        "id": row[0],
                        "email": row[1],
                        "first_name": row[2],
                        "last_name": row[3]
                    }
                    for row in rows
                ]
    def describe(self) -> list[dict]:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = 'users'
                      AND column_name IN (
                          'id',
                          'email',
                          'first_name',
                          'last_name'
                      )
                    ORDER BY ordinal_position
                    """
                )

                rows = cursor.fetchall()

                return [
                    {
                        "column": row[0],
                        "type": row[1],
                        "nullable": row[2] == "YES"
                    }
                    for row in rows
                ]