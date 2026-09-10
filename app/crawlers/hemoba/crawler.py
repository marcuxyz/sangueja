import os

from app.crawlers.base import Base
from app.crawlers.hemoba.parser import Parser


class Crawler(Base):
    def __init__(self):
        super().__init__()

    def parser(self):
        return Parser()

    def target_url(self):
        return os.getenv("HEMOBA_SOURCE_URL", "https://www.ba.gov.br/hemoba/")

    def blood_center(self):
        return {
            "name": "Hemoba",
            "city": "Salvador",
            "state": "BA",
            "address": "Ladeira do Hospital Geral, s/n, Brotas - Cep: 40.286-240 - Complexo HGE, Hemoba e Cican",
        }
