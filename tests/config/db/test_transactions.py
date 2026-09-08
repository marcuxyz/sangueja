import psycopg
import pytest

from config.db.connection import Connection
from config.db.transactions import Transaction


@pytest.fixture
def database_connection(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DB_NAME", "sangueja_test")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PASSWORD", "postgres")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_USERNAME", "postgres")

    try:
        connection = Connection().connect()
    except psycopg.OperationalError as error:
        pytest.skip(f"PostgreSQL de teste indisponível: {error}")

    yield connection

    Transaction(connection).drop_all()
    connection.close()


def test_create_all_creates_all_tables(database_connection):
    transaction = Transaction(database_connection)

    transaction.create_all()

    with database_connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name IN (
                  'blood_centers',
                  'blood_types',
                  'blood_center_stocks',
                  'blood_stock_items'
              )
            ORDER BY CASE table_name
                WHEN 'blood_centers' THEN 1
                WHEN 'blood_types' THEN 2
                WHEN 'blood_center_stocks' THEN 3
                WHEN 'blood_stock_items' THEN 4
            END
            """)
        tables = [row[0] for row in cursor.fetchall()]

    assert tables == [
        "blood_centers",
        "blood_types",
        "blood_center_stocks",
        "blood_stock_items",
    ]


def test_drop_all_removes_all_tables(database_connection):
    transaction = Transaction(database_connection)
    transaction.create_all()

    transaction.drop_all()

    with database_connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name IN (
                  'blood_centers',
                  'blood_types',
                  'blood_center_stocks',
                  'blood_stock_items'
              )
            """)
        table_count = cursor.fetchone()[0]

    assert table_count == 0
