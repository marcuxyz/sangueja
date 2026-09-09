from pydantic import BaseModel

class ConnectionModel(BaseModel):
    pool: int
    database: str
    host: str
    username: str
    password: str
    port: int
