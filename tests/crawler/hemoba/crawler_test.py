from unittest.mock import patch

from app.crawlers.base import Base
from app.crawlers.hemoba.crawler import Crawler


@patch.object(Base, "perform", return_value={"name": "Hemoba"})
def test_base_perform_is_called_during_initialization(mock_perform):
    crawler = Crawler(autostart=True)

    assert crawler is not None
    mock_perform.assert_called_once()


@patch("app.crawlers.base.HttpClient.download_html")
def test_get_a_positive_test(download_html, hemoba_html):
    download_html.return_value.text = hemoba_html
    crawler = Crawler(autostart=True)

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


def test_crawler_uses_source_url_from_environment(monkeypatch):
    monkeypatch.setenv("HEMOBA_SOURCE_URL", "https://hemoba.example/source")

    crawler = Crawler(autostart=False)

    assert crawler.target_url() == "https://hemoba.example/source"


def test_crawler_parser_is_hemoba_parser():
    crawler = Crawler(autostart=False)

    assert crawler.parser().__class__.__name__ == "Parser"


def test_crawler_identifies_blood_center():
    crawler = Crawler(autostart=False)

    assert crawler.blood_center() == {
        "blood_center": "Hemoba",
        "city": "Salvador",
        "state": "BA",
    }
