import os
from dataclasses import dataclass
from typing import ClassVar, Optional


@dataclass
class Database:
    username: str
    password: str
    host: str
    port: str
    name: str

    @property
    def url(self):
        return f"{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class Console:
    page_size: int


@dataclass
class Config:
    database: Database | None = None
    console: Console | None = None
    _config: ClassVar[Optional["Config"]] = None

    @classmethod
    def load(cls):
        if cls._config:
            return cls._config
        if os.path.exists("../.env"):
            from dotenv import load_dotenv

            load_dotenv()
        try:
            cls._config = cls(
                database=Database(
                    username=os.environ["DB_USER"],
                    password=os.environ["DB_PASSWORD"],
                    host=os.environ["DB_HOST"],
                    port=os.environ["DB_PORT"],
                    name=os.environ["DB_NAME"],
                ),
                console=Console(page_size=int(os.environ["PAGE_SIZE"])),
            )
        except KeyError:
            raise Exception("Environment variables do not exist")
        return cls._config
