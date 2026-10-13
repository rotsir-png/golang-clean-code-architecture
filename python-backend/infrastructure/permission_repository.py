from infrastructure.database import get_connection


class PostgresPermissionRepository:

    def has_permission(
        self,
        user_id: int,
        permission: str
    ) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM user_permissions
                        WHERE user_id = %s
                          AND permission = %s
                    )
                    """,
                    (user_id, permission)
                )

                return cursor.fetchone()[0]