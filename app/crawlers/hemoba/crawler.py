import os
from pathlib import Path

from jinja2 import Template

from app.crawlers.base import Base
from app.crawlers.hemoba.parser import Parser
from app.services.whatsapp import Whatsapp

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_PATH = ROOT_DIR / "templates" / "alert.jinja2"


class HemobaCrawler(Base):
    def __init__(self):
        super().__init__()

    def create_parser(self):
        return Parser()

    def source_url(self):
        return os.getenv("HEMOBA_SOURCE_URL", "https://www.ba.gov.br/hemoba/")

    def send_alert(self):
        whatsapp_service = Whatsapp()
        alert_template = TEMPLATE_PATH.read_text(encoding="utf-8")
        critical_blood_types = self.filter_warning_blood_types()
        rendered_alert = Template(alert_template).render(
            {
                "blood_center_name": self.combined_data["name"],
                "blood_types": critical_blood_types,
                "collected_at": self.combined_data["collected_at"],
            }
        )

        whatsapp_service.send_notification(message=rendered_alert)

    def blood_center_data(self):
        return {
            "name": "Hemoba",
            "city": "Salvador",
            "state": "BA",
            "address": "Ladeira do Hospital Geral, s/n, Brotas - Cep: 40.286-240 - Complexo HGE, Hemoba e Cican",
        }

    def filter_warning_blood_types(self):
        return filter(self.is_critical_blood_type, self.combined_data["bloods"])

    def is_critical_blood_type(self, blood_type):
        return blood_type["status"].lower() in ["crítico", "alerta"]
