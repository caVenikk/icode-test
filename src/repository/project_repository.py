from sqlalchemy import select, asc
from sqlalchemy.orm import sessionmaker

from contracts.models import Contract
from projects.models import Project
from projects.schemas import ProjectBaseSchema, ProjectWithContractsSchema
from repository import BaseRepository


class ProjectRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def all(self) -> list[Project]:
        with self._session() as s:
            query = select(Project).order_by(asc(Project.id))
            return list(s.execute(query).scalars().all())

    def get(self, project_id: int) -> Project | None:
        with self._session() as s:
            return (s.execute(select(Project).where(Project.id == project_id))).scalar()

    def create(self, project_data: ProjectBaseSchema | ProjectWithContractsSchema) -> Project | None:
        project_data_dict = project_data.dict()

        with self._session() as s:
            project = Project(id=project_data_dict.get("id"), name=project_data_dict.get("name"))
            s.add(project)
            if "contracts" in project_data_dict:
                contracts_data = project_data_dict["contracts"]
                contract_ids = [
                    contract_data.get("id") for contract_data in contracts_data if contract_data.get("id") is not None
                ]
                contracts = s.execute(select(Contract).where(Contract.id.in_(contract_ids))).scalars().all()
                project.contracts = contracts
            s.commit()
        return project

    def attach_contract(self, project_id: int, contract_id: int) -> Project | None:
        with self._session() as s:
            project = s.execute(select(Project).where(Project.id == project_id)).scalar()
            contract = s.execute(select(Contract).where(Contract.id == contract_id)).scalar()
            project.contracts.append(contract)
            s.commit()
        return project
