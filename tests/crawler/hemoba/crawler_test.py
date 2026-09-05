from unittest.mock import patch

from app.crawlers.base import Base
from app.crawlers.hemoba.crawler import Crawler


def test_autostart_false_does_not_populate_data():
    crawler = Crawler(autostart=False)

    assert crawler is not None
    assert crawler.data is None


@patch.object(Base, "perform", return_value={"name": "Hemoba"})
def test_base_perform_is_called_during_initialization(mock_perform):
    crawler = Crawler()

    assert crawler is not None
    mock_perform.assert_called_once()


@patch("app.crawlers.base.HttpClient.download_html")
def test_get_a_positive_test(download_html, hemoba_html):
    download_html.return_value.text = hemoba_html
    crawler = Crawler()

    assert crawler.data is not None
    assert crawler.data["blood_center"] == "Hemoba"
    assert crawler.data["collected_at"] == "2026-07-27T09:35:31-03:00"
    assert crawler.data["bloods"] == [
        {"name": "A+", "status": "Alerta"},
        {"name": "A-", "status": "Alerta"},
        {"name": "B+", "status": "Alerta"},
        {"name": "B-", "status": "Crítico"},
        {"name": "AB+", "status": "Estável"},
        {"name": "AB-", "status": "Estável"},
        {"name": "O+", "status": "Crítico"},
        {"name": "O-", "status": "Crítico"},
    ]
