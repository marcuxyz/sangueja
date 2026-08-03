import os

from app.crawlers.crawler_base import CrawlerBase
from app.crawlers.hemoba.parser import Parser


class Crawler(CrawlerBase):
    def __init__(self):
        super().__init__()

    def parse(self):
        parser = Parser()
        return parser.parse(self.response_text)

    def default_url(self):
        return os.getenv("HEMOBA_SOURCE_URL")
