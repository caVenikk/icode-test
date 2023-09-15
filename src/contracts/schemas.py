from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from contracts.models import Status, Contract
from database import create_database_session
from projects.models import Project
from utils import depends
from utils.base import BaseSchema


@dataclass
class ContractBaseSchema(BaseSchema):
    name: str
    status: Status | None = None
    signed_at: datetime | None = None


@dataclass
class ProjectInContractSchema(BaseSchema):
    id: int
    name: str

    @classmethod
    def from_orm(cls, project: Project | None):
        if not project:
            return None
        return cls(
            id=project.id,
            name=project.name,
        )


@dataclass
class ContractSchema(BaseSchema):
    id: int
    name: str
    created_at: datetime
    signed_at: datetime
    status: Status
    project: ProjectInContractSchema

    def __repr__(self):
        return f"{self.prefix}Договор №{self.id}"

    @property
    def prefix(self):
        match self.status:
            case Status.DRAFT:
                return ""
            case Status.ACTIVE:
                return "⟳ "
            case Status.COMPLETED:
                return "✓ "
        return ""

    @classmethod
    @depends
    def from_orm(cls, contract: Contract | None, session: sessionmaker = create_database_session()):
        if not contract:
            return None
        with session() as s:
            s.add(contract)
            return cls(
                id=contract.id,
                name=contract.name,
                created_at=contract.created_at,
                signed_at=contract.signed_at,
                status=contract.status,
                project=ProjectInContractSchema.from_orm(contract.project),
            )
