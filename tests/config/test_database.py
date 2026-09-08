from config.database import DATABASE_CONFIG_PATH, Database
from unittest import mock


def test_database_yml_contains_all_environments():
    text = None

    with open(DATABASE_CONFIG_PATH, "r") as f:
        text = f.read()

    assert text is not None
    assert "test" in text
    assert "development" in text
    assert "production" in text


def test_load_production_database_config():
    db = Database()
    config_production = db.load_database_yml()["production"]

    assert config_production == {
        "pool": 20,
        "database": "sangueja",
        "host": "localhost",
        "username": "admin",
        "password": "admin",
    }


def test_load_development_database_config():
    db = Database()
    config_development = db.load_database_yml()["development"]

    assert config_development == {
        "pool": 20,
        "database": "sangueja",
        "host": "localhost",
        "username": "admin",
        "password": "admin",
    }


def test_load_test_database_config():
    db = Database()
    config_test = db.load_database_yml()["test"]

    assert config_test == {
        "pool": 20,
        "database": "sangueja",
        "host": "localhost",
        "username": "admin",
        "password": "admin",
    }


def test_database_production_config_attributes():
    db = Database()
    production = db.production()

    assert production.pool == 20
    assert production.host == "localhost"
    assert production.database == "sangueja"
    assert production.username == "admin"
    assert production.password == "admin"


def test_production_config_loads_database_name_from_environment_variable(monkeypatch):
    monkeypatch.setenv("DATABASE_NAME", "sangue123")

    db = Database()
    production = db.load_database_yml()["production"]

    assert "sangue123" == production["database"]
