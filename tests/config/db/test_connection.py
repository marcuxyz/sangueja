from config.db.connection import DATABASE_CONFIG_PATH, Connection


def test_database_yml_contains_all_environments():
    text = None

    with open(DATABASE_CONFIG_PATH, "r") as f:
        text = f.read()

    assert text is not None
    assert "test" in text
    assert "development" in text
    assert "production" in text


def test_load_production_database_config(monkeypatch):
    monkeypatch.setenv("ENV_PATH", "production")
    monkeypatch.setenv("DB_NAME", "sangueja_production")

    db = Connection()
    config_production = db.load_database_yml()["production"]

    assert config_production == {
        "pool": 20,
        "database": "sangueja_production",
        "host": "localhost",
        "username": "postgres",
        "password": "postgres",
        "port": 5432,
    }


def test_load_development_database_config(monkeypatch):
    monkeypatch.setenv("ENV_PATH", "development")
    monkeypatch.setenv("DB_NAME", "sangueja_development")

    db = Connection()
    model = db.development()

    assert model.pool == 20
    assert model.host == "localhost"
    assert model.database == "sangueja_development"
    assert model.username == "postgres"
    assert model.password == "postgres"
    assert model.port == 5432


def test_load_test_database_config():
    db = Connection()
    model = db.test()

    assert model.pool == 20
    assert model.host == "localhost"
    assert model.database == "sangueja_test"
    assert model.username == "postgres"
    assert model.password == "postgres"
    assert model.port == 5432


def test_production_config_loads_database_name_from_environment_variable(monkeypatch):
    monkeypatch.setenv("DB_NAME", "sangue123")

    db = Connection()
    production = db.load_database_yml()["production"]

    assert "sangue123" == production["database"]
