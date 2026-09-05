from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from sqlalchemy import text
from sqlalchemy import create_engine

from app.http.client import HttpClient


class Base(ABC):
    def __init__(self, autostart: bool = True):
        self.data = None

        if autostart:
            self.data = self.payload()

    def perform(self):
        return self.parse(self.document())

    def download_page(self):
        client = HttpClient(url=self.target_url())

        return client.download_html()

    def parse(self, docuemnt):
        parser = self.parser_instance()

        return parser.parse(docuemnt)

    def document(self):
        page = self.download_page()

        return BeautifulSoup(page.text, "html.parser")

    def payload(self):
        return self.blood_center() | self.perform()

    def parser_instance(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must define parser_class()"
        )

    @abstractmethod
    def target_url(self):
        raise NotImplementedError("Subclasses must implement the target_url method.")

    @abstractmethod
    def blood_center(self):
        raise NotImplementedError("Subclasses must implement the blood_center method.")
