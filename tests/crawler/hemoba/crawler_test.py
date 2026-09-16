from unittest.mock import patch

from app.crawlers.base import BaseCrawler
from app.crawlers.hemoba.crawler import HemobaCrawler
from config.db.connection import Connection
from config.db.transactions import Transaction


@patch.object(BaseCrawler, "perform", return_value={"name": "Hemoba"})
def test_base_perform_is_called_once_times(mock_perform):
    crawler = HemobaCrawler()
    crawler.perform()

    assert crawler is not None
    mock_perform.assert_called_once()


@patch.object(HemobaCrawler, "send_alert")
@patch("app.crawlers.base.HttpClient.download_html")
def test_return_data_of_database(
    download_html, mock_send_alert, hemoba_html, monkeypatch
):
    conn = Connection().connect()
    download_html.return_value.text = hemoba_html
    monkeypatch.setenv("WHATSAPP_URL", "https://test.whatsapp")
    monkeypatch.setenv("WHATSAPP_TOKEN", "9A8897CGS7")
    monkeypatch.setenv("WHATSAPP_NUMBER", "719899999999")

    crawler = Crawler()
    first_result = crawler.perform()
    second_result = crawler.perform()
    crawler.send_alert()

    with conn.cursor() as cur:
        cur.execute("SELECT name, city, state, address FROM blood_centers;")
        blood_center = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM blood_center_stocks;")
        blood_center_stocks = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM blood_stock_items;")
        blood_stock_items = cur.fetchone()[0]

    mock_send_alert.assert_called_once_with()
    assert blood_center is not None
    assert blood_center_stocks == 1
    assert blood_stock_items == 8
    assert second_result == first_result


@patch("app.crawlers.base.HttpClient.download_html")
def test_return_critical_blood_types(download_html, hemoba_html):
    download_html.return_value.text = hemoba_html
    crawler = Crawler()

    crawler.perform()

    warning_blood_types = list(crawler.filter_warning_blood_types())

    assert warning_blood_types == [
        {"name": "A+", "status": "Alerta"},
        {"name": "A-", "status": "Alerta"},
        {"name": "B+", "status": "Alerta"},
        {"name": "B-", "status": "Crítico"},
        {"name": "O+", "status": "Crítico"},
        {"name": "O-", "status": "Crítico"},
    ]


def test_crawler_uses_source_url_from_environment(monkeypatch):
    monkeypatch.setenv("HEMOBA_SOURCE_URL", "https://hemoba.example/source")

    crawler = HemobaCrawler()

    assert crawler.source_url() == "https://hemoba.example/source"


def test_crawler_parser_is_hemoba_parser():
    crawler = HemobaCrawler()

    assert crawler.create_parser().__class__.__name__ == "Parser"


def test_crawler_identifies_blood_center():
    crawler = HemobaCrawler()

    assert crawler.blood_center_data() == {
        "name": "Hemoba",
        "city": "Salvador",
        "state": "BA",
        "address": "Ladeira do Hospital Geral, s/n, Brotas - Cep: 40.286-240 - Complexo HGE, Hemoba e Cican",
    }
