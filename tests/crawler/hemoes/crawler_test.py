from unittest.mock import patch

from app.crawlers.base import BaseCrawler
from app.crawlers.hemoes.crawler import HemoesCrawler
from config.db.connection import Connection
from config.db.transactions import Transaction
from app.http.client import HttpClient


@patch.object(BaseCrawler, "execute", return_value={"name": "Homes"})
def test_base_execute_is_called_once_times(mock_execute):
    crawler = HemoesCrawler()

    crawler.execute()

    assert crawler is not None
    mock_execute.assert_called_once()


@patch.object(HemoesCrawler, "send_alert")
@patch("app.crawlers.base.HttpClient.download_html")
def test_return_data_of_database(
    download_html, mock_send_alert, hemoes_fixture, monkeypatch
):
    crawler = HemoesCrawler()
    conn = Connection().connect()
    download_html.return_value.text = hemoes_fixture
    monkeypatch.setenv("WHATSAPP_URL", "https://test.whatsapp")
    monkeypatch.setenv("WHATSAPP_TOKEN", "9A8897CGS7")
    monkeypatch.setenv("WHATSAPP_NUMBER", "719899999999")

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO blood_centers(name) VALUES (%s)"
            + " ON CONFLICT (name) DO NOTHING",
            (crawler.blood_center_name,),
        )
        conn.commit()

    first_result = crawler.execute()
    second_result = crawler.execute()

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


@patch.object(HemoesCrawler, "send_alert")
@patch("app.crawlers.base.HttpClient.download_html")
def test_return_critical_blood_types(download_html, mock_send_alert, hemoes_fixture):
    download_html.return_value.text = hemoes_fixture
    conn = Connection().connect()
    crawler = HemoesCrawler()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO blood_centers(name) VALUES (%s)"
            + " ON CONFLICT (name) DO NOTHING",
            (crawler.blood_center_name,),
        )
        conn.commit()

    crawler.execute()
    warning_blood_types = list(crawler.filter_warning_blood_types())

    mock_send_alert.assert_called_once_with()
    assert warning_blood_types == [
        {"name": "A-", "status": "Crítico"},
        {"name": "B-", "status": "Crítico"},
        {"name": "B+", "status": "Crítico"},
        {"name": "AB-", "status": "Alerta"},
        {"name": "AB+", "status": "Alerta"},
        {"name": "O-", "status": "Alerta"},
    ]


@patch.object(HemoesCrawler, "send_alert")
@patch("app.crawlers.base.HttpClient.download_html")
def test_valid_message_data(download_html, mock_send_alert, hemoes_fixture):
    conn = Connection().connect()
    download_html.return_value.text = hemoes_fixture
    crawler = HemoesCrawler()

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO blood_centers(name) VALUES (%s)"
            + " ON CONFLICT (name) DO NOTHING",
            (crawler.blood_center_name,),
        )
        conn.commit()

    crawler.execute()
    message_notification = crawler.message_data(crawler.parsed_data)

    mock_send_alert.assert_called_once_with()
    assert "🩸 Tipo sanguíneo: B-\n  🔴 Status: Crítico\n\n" in message_notification


def test_crawler_uses_source_url_from_environment(monkeypatch):
    crawler = HemoesCrawler()


def test_crawler_parser_is_hemoba_parser():
    crawler = HemoesCrawler()

    assert crawler._parser.__class__.__name__ == "HemoesParser"
