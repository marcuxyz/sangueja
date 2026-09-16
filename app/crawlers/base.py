from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from app.http.client import HttpClient
from app.repositories.blood_center import BloodCenterRepository


class BaseCrawler(ABC):
    def __init__(
        self,
        client: HttpClient | None = None,
        blood_center_repository: BloodCenterRepository | None = None,
    ):
        self.client = client or HttpClient()
        self.blood_center_repository = blood_center_repository or BloodCenterRepository()

    def execute(self):
        raw_html = self.fetch()
        parsed_data = self.parse(raw_html)
        self.combined_data = parsed_data

        snapshot_exists = self.save_blood_data(parsed_data)
        if snapshot_exists:
            return self.combined_data

        return self.combined_data

    def save_blood_data(self, parsed_document):
        return self.blood_center_repository.save_snapshot(
            self.blood_center_name,
            parsed_document["collected_at"],
            parsed_document["bloods"],
        )

    @abstractmethod
    def parse(self):
        raise NotImplementedError(f"{self.__class__.__name__} must define parse()")
