from typing import TYPE_CHECKING

from utils.exceptions import ValidationException

if TYPE_CHECKING:
    from contracts.schemas import ContractBaseSchema


class ContractValidator:
    def __init__(self, contract_data: "ContractBaseSchema"):
        self.contract_data = contract_data
        self.__errors: list[str] = []

    def validate(self) -> None:
        self.validate_name()

        if self.__errors:
            raise ValidationException(self.__errors)

    def validate_name(self) -> None:
        if not isinstance(self.contract_data.name, str):
            self.__errors.append(f"Имя должно быть строкой")
