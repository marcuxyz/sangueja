from unittest.mock import patch
from bs4 import BeautifulSoup

from app.crawlers.hemoba.parser import Parser


def test_compose_bloods(hemoba_html):
    parser = Parser()
    parser_html = BeautifulSoup(hemoba_html, "html.parser")
    compose_bloods = parser.compose_rh(parser_html)

    assert compose_bloods is not None
    assert compose_bloods == [
        {"name": "A+", "status": "Alerta"},
        {"name": "A-", "status": "Alerta"},
        {"name": "B+", "status": "Alerta"},
        {"name": "B-", "status": "Crítico"},
        {"name": "AB+", "status": "Estável"},
        {"name": "AB-", "status": "Estável"},
        {"name": "O+", "status": "Crítico"},
        {"name": "O-", "status": "Crítico"},
    ]


def test_define_name():
    parser = Parser()

    assert parser is not None
    assert parser.define_name() == "Hemoba"


@patch("app.crawlers.hemoba.parser.Parser.parse")
def test_get_blood_updated_date(parser_mock, hemoba_html):
    parser_mock.return_value = hemoba_html
    parser = Parser()
    parser_html = BeautifulSoup(hemoba_html, "html.parser")

    assert parser is not None
    assert parser.get_blood_updated_date(parser_html) == "2026-07-27T09:35:31-03:00"


def test_fetch_bloods(hemoba_html):
    parser = Parser()
    parserd_html = BeautifulSoup(hemoba_html, "html.parser")
    raw_html = parser.fetch_bloods(parserd_html)

    assert raw_html is not None
    assert "A+" in raw_html.text.strip()
    assert "AB" in raw_html.text.strip()


def test_fetch_blood_informations(hemoba_html):
    parser = Parser()
    parserd_html = BeautifulSoup(hemoba_html, "html.parser")
    blodds = parser.fetch_blood_informations(parserd_html)

    assert "A+" in blodds[0].text.strip()
    assert "A-" in blodds[1].text.strip()
    assert "B+" in blodds[2].text.strip()
    assert "B-" in blodds[3].text.strip()
