import os
import yaml
import psycopg
from pathlib import Path
from jinja2 import  Template

from .model import ConnectionModel


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_CONFIG_PATH = ROOT_DIR / 'config' / 'database.yml'

class Connection:
    def __init__(self):
        self.config = self.load_database_yml()

    def connect(self):
        env = os.getenv("APP_ENV", "development")
        env_method = getattr(self, env)()

        return psycopg.connect(
            f"""
                dbname={env_method.database}
                user={env_method.username}
                password={env_method.password}
                host={env_method.host}
                port={env_method.port}
            """
        )

    def create_table(self):
        pass

    def production(self):
        config = self.load_database_yml()

        return ConnectionModel(**config['production'])

    def development(self):
        config = self.load_database_yml()

        return ConnectionModel(**config['development'])

    def test(self):
        config = self.load_database_yml()

        return ConnectionModel(**config['test'])

    def load_database_yml(self):
        try:
            template = DATABASE_CONFIG_PATH.read_text(encoding='utf-8')
        except FileNotFoundError as error:
            raise FileNotFoundError(
                "Don't exists config/database.yml file"
            ) from error

        rendered_config = Template(template).render(ENV=os.environ)
        return yaml.safe_load(rendered_config) or {}
