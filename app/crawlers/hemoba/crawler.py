from pathlib import                    Path

from jinja2 import                     Template

from app.crawlers.base import          BaseCrawler
from app.crawlers.hemoba.parser import Parser
from app.services.whatsapp import      Whatsapp

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_PATH = ROOT_DIR / "templates" / "alert.jinja2"


class HemobaCrawler(BaseCrawler):
    URL = "http://www.hemoba.ba.gov.br/"

    def __init__(self):
        super().__init__()

        self.blood_center_name = "Hemoba"
        self._parser = Parser()

    def fetch(self) -> str:
        response = self.client.download_html()
        return response.text

    def parse(self, raw_html: str):
        return self._parser.parse(raw_html)

    def send_alert(self):
        whatsapp_service = Whatsapp()
        alert_template = TEMPLATE_PATH.read_text(encoding="utf-8")
        critical_blood_types = self.filter_warning_blood_types()
        rendered_alert = Template(alert_template).render(
            {
                "blood_center_name": self.parsed_data["name"],
                "blood_types": critical_blood_types,
                "collected_at": self.parsed_data["collected_at"],
            }
        )

        whatsapp_service.send_notification(message=rendered_alert)

    def filter_warning_blood_types(self):
        return filter(self.is_critical_blood_type, self.parsed_data["bloods"])

    def is_critical_blood_type(self, blood_type):
        return blood_type["status"].lower() in ["crítico", "alerta"]
