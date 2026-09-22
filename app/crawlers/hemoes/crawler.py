import os
from pathlib import Path

from jinja2 import Template

from app.crawlers.base import BaseCrawler
from app.crawlers.hemoes.parser import HemoesParser
from app.services.whatsapp import Whatsapp

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_PATH = ROOT_DIR / "templates" / "alert.jinja2"


class HemoesCrawler(BaseCrawler):
    URL = os.getenv(
        "HEMOES_URL",
        "https://dados.es.gov.br/api/action/datastore_search?resource_id=d73f9335-f454-4d1a-bfba-51ed2dac9cb6&limit=1&sort=_id+desc",
    )

    def __init__(self):
        super().__init__()

        self.blood_center_name = "Hemoes"
        self.blood_center_address = "https://hemoes.es.gov.br/enderecos-dos-hemocentros"
        self._parser = HemoesParser()

    def fetch(self) -> str:
        response = self.client.download_html()
        return response.text

    def parse(self, raw_html: str):
        data = self._parser.parse(raw_html)
        return {
            "name": self.blood_center_name,
            "address": self.blood_center_address,
        } | data

    def send_alert(self):
        whatsapp_service = Whatsapp()
        notification_message = self.message_data(self.parsed_data)

        whatsapp_service.send_notification(message=notification_message)

    def message_data(self, data: dict):
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
        return Template(template).render(
            {
                "blood_center_name": data["name"],
                "collected_at": data["collected_at"],
                "blood_center_address": data["address"],
                "blood_types": self.filter_warning_blood_types(),
            }
        )

    def filter_warning_blood_types(self):
        return filter(self.filter_blood_types, self.parsed_data["blood_types"])

    def filter_blood_types(self, blood_type):
        return blood_type["status"].lower() in ["crítico", "alerta"]
