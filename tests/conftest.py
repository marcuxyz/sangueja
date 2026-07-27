import pytest

from utils import load_fixture


@pytest.fixture
def hemoba_html():
    return load_fixture("hemoba.html")
