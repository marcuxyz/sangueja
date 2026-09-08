from config.database import DATABASE_CONFIG_PATH, Database
from unittest import mock


def test_must_exists_environments():
    text = None

    with open(DATABASE_CONFIG_PATH, "r") as f:
        text = f.read()

    assert text is not None
    assert "test" in text
    assert "development" in text
    assert "production" in text


def test_production_setup():
    db = Database()
    config_production = db.load_database_yml()["production"]

    assert config_production == {
        "pool": 20,
        "database": "sangueja",
        "host": "localhost",
        "username": "admin",
        "password": "admin",
    }


def test_development_setup():
    db = Database()
    config_development = db.load_database_yml()["development"]

    assert config_development == {
        "pool": 20,
        "database": "sangueja",
        "host": "localhost",
        "username": "admin",
        "password": "admin",
    }


def test_test_setup():
    db = Database()
    config_test = db.load_database_yml()["test"]

    assert config_test == {
        "pool": 20,
        "database": "sangueja",
        "host": "localhost",
        "username": "admin",
        "password": "admin",
    }


def test_production_get_envrionment_value_from_os(monkeypatch):
    monkeypatch.setenv("DATABASE_NAME", "sangue123")

    db = Database()
    production = db.load_database_yml()["production"]

    assert "sangue123" == production["database"]
