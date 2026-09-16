from typing import Any, Mapping

from config.db.connection import Connection
from config.db.query import Query


class BloodCenterRepository:
    INSERT_SQL = "INSERT INTO blood_centers(name) " "VALUES (%s, %s, %s, %s)"
    FIND_SQL = "SELECT name FROM blood_centers WHERE name = %s;"
    FIND_CENTER_ID_SQL = "SELECT id FROM blood_centers WHERE name = %s;"
    FIND_STOCK_SQL = (
        "SELECT id FROM blood_center_stocks "
        "WHERE blood_center_id = %s AND collected_at = %s;"
    )
    INSERT_STOCK_SQL = (
        "INSERT INTO blood_center_stocks(blood_center_id, collected_at) "
        "VALUES (%s, %s) RETURNING id"
    )
    FIND_BLOOD_TYPE_ID_SQL = "SELECT id FROM blood_types WHERE name = %s;"
    INSERT_STOCK_ITEM_SQL = (
        "INSERT INTO blood_stock_items "
        "(blood_center_stock_id, blood_type_id, status) "
        "VALUES (%s, %s, %s)"
    )

    def __init__(self, query: Query | None = None):
        self.query = query or Query(Connection())

    def find_or_create(self, blood_center: Mapping[str, str]):
        return self.query.find_or_create(
            self.INSERT_SQL,
            self.FIND_SQL,
            blood_center,
        )

    def save_snapshot(
        self,
        blood_center_name: str,
        collected_at: str,
        bloods: list[Mapping[str, str]],
    ) -> bool:
        connection = self.query.conn
        try:
            with connection.cursor() as cursor:
                cursor.execute(self.FIND_CENTER_ID_SQL, (blood_center_name,))
                center_row = cursor.fetchone()

                if center_row is None:
                    raise ValueError(f"Blood center not found: {blood_center_name}")

                cursor.execute(
                    self.FIND_STOCK_SQL,
                    (center_row[0], collected_at),
                )
                if cursor.fetchone() is not None:
                    connection.commit()
                    return True

                cursor.execute(
                    self.INSERT_STOCK_SQL,
                    (center_row[0], collected_at),
                )
                stock_row = cursor.fetchone()

                if stock_row is None:
                    raise ValueError("Blood center stock was not created")

                for blood in bloods:
                    cursor.execute(self.FIND_BLOOD_TYPE_ID_SQL, (blood["name"],))
                    blood_type_row = cursor.fetchone()

                    if blood_type_row is None:
                        raise ValueError(f"Blood type not found: {blood['name']}")

                    cursor.execute(
                        self.INSERT_STOCK_ITEM_SQL,
                        (stock_row[0], blood_type_row[0], blood["status"]),
                    )

            connection.commit()
            return False
        except Exception:
            connection.rollback()
            raise
