from unittest.mock import patch

from app.crawlers.crawler_base import CrawlerBase
from app.crawlers.hemoba.crawler import Crawler


@patch.object(CrawlerBase, "perform", return_value="base")
def test_base_perform_is_called_during_initialization(mock_perform):
    crawler = Crawler()

    assert crawler is not None
    mock_perform.assert_called_once()


@patch("app.crawlers.crawler_base.HttpClient.download_html")
def test_get_a_positive_test(download_html, hemoba_html):
    download_html.return_value.text = hemoba_html
    crawler = Crawler()
    crawler_parse = crawler.parse()

    assert crawler.response_text is not None
    assert crawler_parse["name"] == "Hemoba"
    assert crawler_parse["updated_date"] == "2026-07-27T09:35:31-03:00"
    assert crawler_parse["bloods"] == [
        {"name": "A+", "status": "Alerta"},
        {"name": "A-", "status": "Alerta"},
        {"name": "B+", "status": "Alerta"},
        {"name": "B-", "status": "Crítico"},
        {"name": "AB+", "status": "Estável"},
        {"name": "AB-", "status": "Estável"},
        {"name": "O+", "status": "Crítico"},
        {"name": "O-", "status": "Crítico"},
    ]
