from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from app.http.client import HttpClient
from app.repositories.blood_center import BloodCenterRepository


class BaseCrawler(ABC):
    def __init__(
        self,
        blood_center_repository: BloodCenterRepository | None = None,
    ):
        self.blood_center_repository = blood_center_repository or BloodCenterRepository()

    def perform(self):
        parsed_document = self.parse(self.document())
        blood_center_data = self.blood_center_data()
        self.combined_data = parsed_document | blood_center_data

        snapshot_exists = self.save_blood_data(blood_center_data, parsed_document)
        if snapshot_exists:
            return self.combined_data

        return self.combined_data

    def save_blood_data(self, blood_center_data, parsed_document):
        return self.blood_center_repository.save_snapshot(
            blood_center_data,
            parsed_document["collected_at"],
            parsed_document["bloods"],
        )

    def download_page(self):
        client = HttpClient(url=self.source_url())

        return client.download_html()

    def parse(self, document):
        document_parser = self.create_parser()

        return document_parser.parse(document)

    def document(self):
        page = self.download_page()

        return BeautifulSoup(page.text, "html.parser")

    def create_parser(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must define create_parser()"
        )

    @abstractmethod
    def source_url(self):
        raise NotImplementedError("Subclasses must implement the source_url method.")

    @abstractmethod
    def blood_center_data(self):
        raise NotImplementedError(
            "Subclasses must implement the blood_center_data method."
        )
