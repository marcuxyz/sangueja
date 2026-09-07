from unittest.mock import patch
from bs4 import BeautifulSoup

from app.crawlers.hemoba.parser import Parser


def test_parse_blood_availability(hemoba_html):
    parser = Parser()
    parser_html = BeautifulSoup(hemoba_html, "html.parser")
    blood_availability = parser.parse_blood_availability(parser_html)

    assert blood_availability is not None
    assert blood_availability == [
        {"name": "A+", "status": "Alerta"},
        {"name": "A-", "status": "Alerta"},
        {"name": "B+", "status": "Alerta"},
        {"name": "B-", "status": "Crítico"},
        {"name": "AB+", "status": "Estável"},
        {"name": "AB-", "status": "Estável"},
        {"name": "O+", "status": "Crítico"},
        {"name": "O-", "status": "Crítico"},
    ]


def test_extract_collection_timestamp(hemoba_html):
    parser = Parser()
    parser_html = BeautifulSoup(hemoba_html, "html.parser")

    assert parser is not None
    assert (
        parser.extract_collection_timestamp(parser_html) == "2026-07-27T09:35:31-03:00"
    )


def test_find_blood_section(hemoba_html):
    parser = Parser()
    document = BeautifulSoup(hemoba_html, "html.parser")
    bloods_section = parser.find_blood_section(document)

    assert bloods_section is not None
    assert "A+" in bloods_section.text.strip()
    assert "AB" in bloods_section.text.strip()


def test_find_blood_cards(hemoba_html):
    parser = Parser()
    document = BeautifulSoup(hemoba_html, "html.parser")
    blood_cards = parser.find_blood_cards(parser.find_blood_section(document))

    assert "A+" in blood_cards[0].text.strip()
    assert "A-" in blood_cards[1].text.strip()
    assert "B+" in blood_cards[2].text.strip()
    assert "B-" in blood_cards[3].text.strip()
