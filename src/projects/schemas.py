from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from contracts.models import Status
from database import create_database_session
from projects.models import Project
from utils import depends
from utils.base import BaseSchema


@dataclass
class ProjectBaseSchema(BaseSchema):
    name: str


@dataclass
class ContractInProjectSchema(BaseSchema):
    id: int
    name: str
    created_at: datetime
    signed_at: datetime
    status: Status

    @classmethod
    def from_orm(cls, contract):
        if not contract:
            return None
        return cls(
            id=contract.id,
            name=contract.name,
            created_at=contract.created_at,
            signed_at=contract.signed_at,
            status=contract.status,
        )


@dataclass
class ProjectWithContractsSchema(ProjectBaseSchema):
    contracts: list[ContractInProjectSchema]


@dataclass
class ProjectSchema(ProjectWithContractsSchema):
    id: int

    def __repr__(self):
        return f'Проект "{self.name}" №{self.id}'

    @classmethod
    @depends
    def from_orm(cls, project: Project | None, session: sessionmaker = create_database_session()):
        if not project:
            return None
        with session() as s:
            s.add(project)
            return cls(
                id=project.id,
                name=project.name,
                contracts=[ContractInProjectSchema.from_orm(contract) for contract in project.contracts],
            )
