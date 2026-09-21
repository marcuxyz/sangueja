from pathlib import Path

from jinja2 import Template

from app.crawlers.base import BaseCrawler
from app.crawlers.hemoba.parser import Parser
from app.services.whatsapp import Whatsapp

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_PATH = ROOT_DIR / "templates" / "alert.jinja2"


class HemobaCrawler(BaseCrawler):
    URL = "http://www.hemoba.ba.gov.br/"

    def __init__(self):
        super().__init__()

        self.blood_center_name = "Hemoba"
        self.blood_center_address = "https://www.ba.gov.br/hemoba/onde-doar"

        self._parser = Parser()

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
