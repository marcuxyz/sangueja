from unittest.mock import patch

from app.crawlers.base import BaseCrawler
from app.crawlers.hemoba.crawler import HemobaCrawler
from config.db.connection import Connection
from config.db.transactions import Transaction
from app.http.client import HttpClient


@patch.object(BaseCrawler, "execute", return_value={"name": "Hemoba"})
def test_base_execute_is_called_once_times(mock_execute):
    crawler = HemobaCrawler()
    crawler.execute()

    assert crawler is not None
    mock_execute.assert_called_once()


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

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO blood_centers(name) VALUES (%s)"
            + " ON CONFLICT (name) DO NOTHING",
            ("Hemoba",),
        )
        conn.commit()

    crawler = HemobaCrawler()
    first_result = crawler.execute()
    second_result = crawler.execute()
    crawler.send_alert()

    with conn.cursor() as cur:
        cur.execute("SELECT name FROM blood_centers;")
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
    crawler = HemobaCrawler()
    crawler.execute()
    warning_blood_types = list(crawler.filter_warning_blood_types())

    assert warning_blood_types == [
        {"name": "A+", "status": "Alerta"},
        {"name": "A-", "status": "Alerta"},
        {"name": "B+", "status": "Alerta"},
        {"name": "B-", "status": "Crítico"},
        {"name": "O+", "status": "Crítico"},
        {"name": "O-", "status": "Crítico"},
    ]


def test_crawler_uses_source_url_from_environment():
    crawler = HemobaCrawler()

    assert crawler.URL == "http://www.hemoba.ba.gov.br/"


def test_crawler_parser_is_hemoba_parser():
    crawler = HemobaCrawler()

    assert crawler._parser.__class__.__name__ == "Parser"
