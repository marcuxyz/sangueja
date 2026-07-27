from bs4 import BeautifulSoup


class Parser:
    def parse(self, raw_html: str):
        parserd_html = BeautifulSoup(raw_html, "html.parser")

        return {
            "name": self.define_name(),
            "bloods": self.compose_rh(parserd_html),
            "last_release": self.get_blood_last_release(parserd_html),
        }

    def define_name(self):
        return "Hemoba"

    def compose_rh(self, html):
        bloods_html = self.fetch_bloods(html)
        blod_informations = self.fetch_blood_informations(bloods_html)

        informations = [
            {
                "name": blood.h1.text.strip(),
                "level": blood.p.text.strip(),
            }
            for blood in blod_informations
        ]
        return informations

    def fetch_bloods(self, html):
        return html.find(
            id="block-bagov-base-views-block-view-card-card-estatistico-sup-critico"
        )

    def fetch_blood_informations(self, html):
        html_selector = (
            "p-0 p-lg-1 p-md-1 card-footer w-100 border-0 text-center text-uppercase"
        )

        return html.find_all("div", class_=html_selector)

    def get_blood_last_release(self, html):
        return html.find("time")["datetime"]
