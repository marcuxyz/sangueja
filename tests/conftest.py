import pytest
from dotenv import load_dotenv

from utils import load_fixture

load_dotenv()


@pytest.fixture
def hemoba_html():
    return load_fixture("hemoba.html")
