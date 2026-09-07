from unittest.mock import Mock, patch

import pytest
from bs4 import BeautifulSoup

from app.crawlers.base import Base


class FakeCrawler(Base):
    def __init__(self, autostart=False):
        super().__init__(autostart=autostart)

    def target_url(self):
        return "https://example.com/blood"

    def blood_center(self):
        return {"blood_center": "Example"}

    def parser(self):
        return Mock(parse=Mock(return_value={"bloods": []}))


def test_initialization_does_not_collect_when_autostart_is_disabled():
    with patch.object(FakeCrawler, "perform") as perform:
        crawler = FakeCrawler(autostart=False)

    assert crawler.data is None
    perform.assert_not_called()
