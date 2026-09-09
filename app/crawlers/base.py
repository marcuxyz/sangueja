from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from app.http.client import HttpClient
from app.repositories.blood_center import BloodCenterRepository


class Base(ABC):
    def __init__(
        self,
        blood_center_repository: BloodCenterRepository | None = None,
    ):
        self.blood_center_repository = blood_center_repository or BloodCenterRepository()

    def perform(self):
        parsed_doc = self.parse(self.document())
        params = self.blood_center()

        self.save_blood_data(params, parsed_doc)

        return params | parsed_doc

    def save_blood_data(self, blood_center, parsed_document):
        self.blood_center_repository.save_snapshot(
            blood_center,
            parsed_document["collected_at"],
            parsed_document["bloods"],
        )

    def download_page(self):
        client = HttpClient(url=self.target_url())

        return client.download_html()

    def parse(self, document):
        parser = self.parser()

        return parser.parse(document)

    def document(self):
        page = self.download_page()

        return BeautifulSoup(page.text, "html.parser")

    def parser(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must define parser_class()"
        )

    @abstractmethod
    def target_url(self):
        raise NotImplementedError("Subclasses must implement the target_url method.")

    @abstractmethod
    def blood_center(self):
        raise NotImplementedError("Subclasses must implement the blood_center method.")
