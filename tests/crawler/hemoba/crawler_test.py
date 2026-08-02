from unittest.mock import patch
from crawler.hemoba.crawler import Crawler


@patch("crawler.hemoba.crawler.Client.get")
def test_get_a_positive_test(mock_get, hemoba_html):
    mock_get.return_value = hemoba_html
    crawler = Crawler.perform()

    assert crawler is not None
    assert crawler["name"] == "Hemoba"
    assert crawler["updated_date"] == "2026-07-27T09:35:31-03:00"
    assert crawler["bloods"] == [
        {"name": "A+", "level": "Alerta"},
        {"name": "A-", "level": "Alerta"},
        {"name": "B+", "level": "Alerta"},
        {"name": "B-", "level": "Crítico"},
        {"name": "AB+", "level": "Estável"},
        {"name": "AB-", "level": "Estável"},
        {"name": "O+", "level": "Crítico"},
        {"name": "O-", "level": "Crítico"},
    ]
