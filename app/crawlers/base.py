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

    def perform(self):
        raw_html = self.fetch()
        parsed_data = self.parse(raw_html)
        blood_center_data = self.blood_center_data()
        self.combined_data = parsed_data | blood_center_data

        snapshot_exists = self.save_blood_data(blood_center_data, parsed_data)
        if snapshot_exists:
            return self.combined_data

        return self.combined_data

    def save_blood_data(self, blood_center_data, parsed_document):
        return self.blood_center_repository.save_snapshot(
            blood_center_data,
            parsed_document["collected_at"],
            parsed_document["bloods"],
        )

    @abstractmethod
    def blood_center_data(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must define blood_center_data()"
        )

    @abstractmethod
    def parse(self):
        raise NotImplementedError(f"{self.__class__.__name__} must define parse()")

    def blood_center_data(self):
        raise NotImplementedError(
            "Subclasses must implement the blood_center_data method."
        )
