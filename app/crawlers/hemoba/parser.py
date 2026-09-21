from bs4 import BeautifulSoup


class Parser:
    def parse(self, raw_html: str) -> dict:
        soup = BeautifulSoup(raw_html, "html.parser")

        return {
            "blood_types": self.parse_blood_availability(soup),
            "collected_at": self.extract_collection_timestamp(soup),
        }

    def parse_blood_availability(self, document):
        bloods_section = self.find_blood_section(document)
        blood_cards = self.find_blood_cards(bloods_section)

        informations = [
            {
                "name": blood.h1.text.strip(),
                "status": blood.p.text.strip(),
            }
            for blood in blood_cards
        ]
        return informations

    def find_blood_section(self, document):
        return document.find(
            id="block-bagov-base-views-block-view-card-card-estatistico-sup-critico"
        )

    def find_blood_cards(self, bloods_section):
        html_selector = (
            "p-0 p-lg-1 p-md-1 card-footer w-100 border-0 text-center text-uppercase"
        )

        return bloods_section.find_all("div", class_=html_selector)

    def extract_collection_timestamp(self, document):
        return document.find("time")["datetime"]
