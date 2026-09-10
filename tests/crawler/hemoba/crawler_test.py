from unittest.mock import patch

from app.crawlers.base import Base
from app.crawlers.hemoba.crawler import Crawler
from config.db.connection import Connection
from config.db.transactions import Transaction


@patch.object(Base, "perform", return_value={"name": "Hemoba"})
def test_base_perform_is_called_once_times(mock_perform):
    crawler = Crawler()
    crawler.perform()

    assert crawler is not None
    mock_perform.assert_called_once()


@patch("app.crawlers.base.HttpClient.download_html")
def test_return_data_of_database_test(download_html, hemoba_html):
    conn = Connection().connect()
    transaction = Transaction(conn)
    download_html.return_value.text = hemoba_html

    transaction.create_all()
    for blood_type in ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"):
        transaction.insert_blood_type(blood_type)
    conn.commit()

    crawler = Crawler()
    crawler.perform()

    with conn.cursor() as cur:
        cur.execute("SELECT name, city, state, address FROM blood_centers;")
        blood_center = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM blood_center_stocks;")
        blood_center_stocks = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM blood_stock_items;")
        blood_stock_items = cur.fetchone()[0]

    assert blood_center is not None
    assert blood_center_stocks == 1
    assert blood_stock_items == 8

    transaction.drop_all()


def test_crawler_uses_source_url_from_environment(monkeypatch):
    monkeypatch.setenv("HEMOBA_SOURCE_URL", "https://hemoba.example/source")

    crawler = Crawler()

    assert crawler.target_url() == "https://hemoba.example/source"


def test_crawler_parser_is_hemoba_parser():
    crawler = Crawler()

    assert crawler.parser().__class__.__name__ == "Parser"


def test_crawler_identifies_blood_center():
    crawler = Crawler()

    assert crawler.blood_center() == {
        "name": "Hemoba",
        "city": "Salvador",
        "state": "BA",
        "address": "Ladeira do Hospital Geral, s/n, Brotas - Cep: 40.286-240 - Complexo HGE, Hemoba e Cican",
    }
