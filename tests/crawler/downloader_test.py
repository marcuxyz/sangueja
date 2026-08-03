from unittest.mock import patch

from app.http.client import HttpClient


@patch("app.http.client.HttpClient.download_html")
def test_downloader(download_html, hemoba_html):
    url = "https://sangueja.com.br"
    download_html.return_value = hemoba_html
    page_downloader = HttpClient(url=url)

    response = page_downloader.download_html()

    assert "Hemoba" in response
