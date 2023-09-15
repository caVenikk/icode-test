from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.base import Base
from projects.models import Project
from contracts.models import Contract
from config import Config


@lru_cache(maxsize=1)
def create_database_session():
    config = Config.load()
    db_engine = create_engine(f"postgresql+psycopg2://{config.database.url}", echo=False)

    # Base.metadata.drop_all(db_engine)  # Uncomment to drop all tables
    Base.metadata.create_all(db_engine)

    session = sessionmaker(db_engine)
    return session
