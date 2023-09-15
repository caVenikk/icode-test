from datetime import datetime

from contracts.exceptions import ContractNotFoundException
from contracts.schemas import ContractBaseSchema, ContractSchema
from repository import Repository
from utils import depends


@depends
def get_contracts(repository: Repository = Repository()) -> list[ContractSchema]:
    contracts = repository.contracts.all()
    contract_schemas = [ContractSchema.from_orm(contract) for contract in contracts]
    return contract_schemas


@depends
def get_contract(contract_id: int, repository: Repository = Repository()) -> ContractSchema:
    contract = repository.contracts.get(contract_id)
    return ContractSchema.from_orm(contract)


@depends
def create_contract(contract_data: ContractBaseSchema, repository: Repository = Repository()) -> ContractSchema:
    if contract_data.status:
        contract_data.signed_at = datetime.now()
    contract = repository.contracts.create(contract_data)
    return ContractSchema.from_orm(contract)


@depends
def sign_contract(contract_id: int, repository: Repository = Repository()) -> ContractSchema | None:
    if not repository.contracts.get(contract_id):
        raise ContractNotFoundException(contract_id)
    contract = repository.contracts.sign(contract_id)
    if not contract:
        return None
    return ContractSchema.from_orm(contract)


@depends
def complete_contract(contract_id: int, repository: Repository = Repository()) -> ContractSchema | None:
    if not repository.contracts.get(contract_id):
        raise ContractNotFoundException(contract_id)
    contract = repository.contracts.complete(contract_id)
    if not contract:
        return None
    return ContractSchema.from_orm(contract)


def print_contract(contract: ContractSchema) -> None:
    print(
        f"\nНомер договора: {contract.id}\n"
        f"Название договора: {contract.name}\n"
        f"Дата создания: {contract.created_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"Дата подписания: {contract.signed_at.strftime('%d.%m.%Y %H:%M:%S') if contract.signed_at else 'Не подписан'}\n"
        f"Статус договора: {contract.status.value}\n"
        f"Проект №: {contract.project.id if contract.project else 'Не привязан'}\n"
    )
