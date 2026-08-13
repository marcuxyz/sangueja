from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class BloodCenter(Base):
    __tablename__ = "blood_centers"

    id = mapped_column(Integer(), primary_key=True)
    name = mapped_column(String(50))
    city = mapped_column(String(16))
    state = mapped_column(String(2))

    def __repr__(self) -> str:
        return f"Blood Center(id={self.id!r}, name={self.name!r}, city={self.city!r})"
