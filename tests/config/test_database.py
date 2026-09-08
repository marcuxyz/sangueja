from config.database import DATABASE_CONFIG_PATH, Database
from unittest import mock


def test_must_exists_environments():
    text = None

    with open(DATABASE_CONFIG_PATH, 'r') as f:
        text = f.read()

    assert text is not None
    assert 'test' in text
    assert 'development' in text
    assert 'production' in text
