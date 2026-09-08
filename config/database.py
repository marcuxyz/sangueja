import os
from pathlib import Path

import yaml
from jinja2 import Template

ROOT_DIR = Path(__file__).resolve().parent.parent
DATABASE_CONFIG_PATH = ROOT_DIR / 'config' / 'database.yml'

class Database:
    def __init__(self):
        self.config = self.load_database_yml()

    def connect(self):
        pass

    def create_table(self):
        pass

    def load_database_yml(self):
        try:
            template = DATABASE_CONFIG_PATH.read_text(encoding='utf-8')
        except FileNotFoundError as error:
            raise FileNotFoundError(
                "Don't exists config/database.yml file"
            ) from error

        rendered_config = Template(template).render(ENV=os.environ)
        return yaml.safe_load(rendered_config) or {}
