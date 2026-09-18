import pytest

from dotenv import load_dotenv
from rich import print

from config.db.connection import Connection
from config.db.transactions import Transaction
from utils import load_fixture

load_dotenv()


@pytest.fixture(autouse=True)
def before():
    connection = Connection().connect()
    transaction = Transaction(connection)

    transaction.create_all()
    for blood_type in ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"):
        transaction.insert_blood_type(blood_type)
    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO blood_centers(name) VALUES (%s)"
            + " ON CONFLICT (name) DO NOTHING",
            ("Hemoba",),
        )
        connection.commit()

    try:
        yield connection
    finally:
        transaction.drop_all()
        connection.close()


@pytest.fixture
def hemoba_html():
    return load_fixture("hemoba/example1.html")
