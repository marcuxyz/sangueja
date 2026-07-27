from bs4 import BeautifulSoup


class Parser:
    def parse(self, raw_html: str):
        soup = BeautifulSoup(raw_html, "html.parser")

        return {
            "name": self.define_name(),
            "bloods": self.compose_rh(soup),
        }

    def define_name(self):
        return "Hemoba"

    def compose_bloods(self, soup):
        return [self.rh_a_positive(soup)]

    def compose_rh(self, html):
        div_html = html.find(id=self.bloods_container_selector_id())
        bloods = div_html.find_all(
            "div", class_=self.blood_informations_container_selector()
        )

        return [
            {
                "name": blood.h1.text.strip(),
                "level": blood.p.text.strip(),
            }
            for blood in bloods
        ]

    def bloods_container_selector_id(self):
        return "block-bagov-base-views-block-view-card-card-estatistico-sup-critico"

    def blood_informations_container_selector(self):
        return "p-0 p-lg-1 p-md-1 card-footer w-100 border-0 text-center text-uppercase"
