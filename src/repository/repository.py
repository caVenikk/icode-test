from database import create_database_session
from repository.contract_repository import ContractRepository
from repository.project_repository import ProjectRepository
from utils import Singleton


class Repository(metaclass=Singleton):
    def __init__(self):
        session = create_database_session()
        self.contracts = ContractRepository(session)
        self.projects = ProjectRepository(session)

    def __call__(self):
        return self
