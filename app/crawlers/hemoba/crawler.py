import os

from app.crawlers.crawler_base import CrawlerBase
from app.crawlers.hemoba.parser import Parser


class Crawler(CrawlerBase):
    def __init__(self, autostart: bool = True):
        super().__init__(autostart=autostart)

    def parser_class(self):
        return Parser()

    def target_url(self):
        return os.getenv("HEMOBA_SOURCE_URL")

    def blood_center(self):
        return {"blood_center": "Hemoba", "city": "Salvador", "state": "BA"}
