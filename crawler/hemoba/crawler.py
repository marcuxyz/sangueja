from httpx import Client

from crawler.base import Base
from crawler.hemoba.parser import Parser

# DEFAULT_URL = "https://hemoes.es.gov.br/"
DEFAULT_URL = ""


class Crawler(Base):
    @staticmethod
    def perform():
        response = Client.get(DEFAULT_URL)
        parser = Parser()
        return parser.parse(response)
