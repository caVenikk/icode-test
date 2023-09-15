from sqlalchemy import select, func, asc
from sqlalchemy.orm import sessionmaker

from contracts.exceptions import CannotSignCompletedContractException
from contracts.models import Contract, Status
from contracts.schemas import ContractBaseSchema
from repository import BaseRepository


class ContractRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def all(self) -> list[Contract]:
        with self._session() as s:
            query = select(Contract).order_by(asc(Contract.id))
            return list(s.execute(query).scalars().all())

    def get(self, contract_id: int) -> Contract | None:
        with self._session() as s:
            return (s.execute(select(Contract).where(Contract.id == contract_id))).scalar()

    def create(self, contract_data: ContractBaseSchema) -> Contract | None:
        contract = Contract(**contract_data.dict())
        with self._session() as s:
            s.add(contract)
            s.commit()
        return contract

    def sign(self, contract_id: int) -> Contract | None:
        with self._session() as s:
            contract = s.execute(select(Contract).where(Contract.id == contract_id)).scalar()
            if contract.status == Status.COMPLETED:
                raise CannotSignCompletedContractException(contract_id)
            if contract.status == Status.ACTIVE:
                return None
            contract.status = Status.ACTIVE
            contract.signed_at = func.now()
            s.commit()
        return contract

    def complete(self, contract_id: int) -> Contract | None:
        with self._session() as s:
            contract = s.execute(select(Contract).where(Contract.id == contract_id)).scalar()
            if contract.status == Status.COMPLETED:
                return None
            contract.status = Status.COMPLETED
            s.commit()
        return contract
