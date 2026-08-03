from abc import ABC, abstractmethod
from app.http.client import HttpClient


class CrawlerBase(ABC):
    def __init__(self):
        self.response_text = self.perform()

    def perform(self):
        client = HttpClient(url=self.default_url())
        response = client.download_html()
        return response.text

    @abstractmethod
    def default_url(self):
        raise NotImplementedError("Subclasses must implement the default_url method.")
