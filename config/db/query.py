from typing import Any

from .connection import Connection


class Query:
    def __init__(self, conn: Connection):
        self.conn = conn.connect()

    def find(self, sql: str, *params: Any) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchone()
        except Exception:
            self.conn.rollback()
            raise

    def create(self, sql: str, *params: Any) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def find_or_create(self, insert_sql: str, query_sql: str, params: Any) -> None:
        find_one = self.find(query_sql, params["name"])

        if find_one: return True

        return self.create(insert_sql, *params)
