from contracts.schemas import ContractSchema
from projects.schemas import ProjectSchema, ProjectBaseSchema, ProjectWithContractsSchema
from repository import Repository
from utils import depends


@depends
def get_projects(repository: Repository = Repository()) -> list[ProjectSchema]:
    projects = repository.projects.all()
    project_schemas = [ProjectSchema.from_orm(project) for project in projects]
    return project_schemas


@depends
def get_project(project_id: int, repository: Repository = Repository()) -> ProjectSchema:
    project = repository.projects.get(project_id)
    return ProjectSchema.from_orm(project)


@depends
def create_project(
    project_schema: ProjectBaseSchema | ProjectWithContractsSchema,
    repository: Repository = Repository(),
) -> ProjectSchema:
    project = repository.projects.create(project_schema)
    return ProjectSchema.from_orm(project)


@depends
def attach_contract_to_project(
    project_id: int,
    contract: ContractSchema,
    repository: Repository = Repository(),
) -> None:
    repository.projects.attach_contract(project_id, contract.id)


def print_project(project: ProjectSchema) -> None:
    print(
        f"\nНомер проекта: {project.id}\n"
        f"Название проекта: {project.name}\n"
        "Enter – просмотр прикрепленных договоров | Q – Назад"
    )
