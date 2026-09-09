from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from app.http.client import HttpClient
from config.db.connection import Connection
from config.db.query import Query


class Base(ABC):
    def __init__(self, autostart: bool = True):
        self.query = Query(Connection())

    def perform(self):
        parsed_doc = self.parse(self.document())
        params = self.blood_center()

        insert_sql = "INSERT INTO blood_centers(name, city, state, address) VALUES (%s, %s, %s, %s)"
        query_sql = "SELECT name FROM blood_centers WHERE name = %s;"

        self.query.find_or_create(insert_sql, query_sql, params)

        return params | parsed_doc

    def download_page(self):
        client = HttpClient(url=self.target_url())

        return client.download_html()

    def parse(self, docuemnt):
        parser = self.parser()

        return parser.parse(docuemnt)

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
