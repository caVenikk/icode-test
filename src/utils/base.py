from dataclasses import asdict, dataclass

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


@dataclass
class BaseSchema:
    dict = asdict
