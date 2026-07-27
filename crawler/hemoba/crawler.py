import os

from httpx import Client

from crawler.base import Base
from crawler.hemoba.parser import Parser

DEFAULT_URL = os.getenv("HEMOBA_SOURCE_URL")


class Crawler(Base):
    @staticmethod
    def perform():
        response = Client.get(DEFAULT_URL)
        parser = Parser()
        return parser.parse(response)
