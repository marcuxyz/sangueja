from pydantic import BaseModel

class DatabaseConfigModel(BaseModel):
    pool: int
    database: str
    host: str
    username: str
    password: str
    port: int
