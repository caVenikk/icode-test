import msvcrt

from cli.depenpencies import _get_contracts, _get_projects, _get_contract_info
from cli.flags import RefreshContractsFlag
from cli.utils import clear_console, wait_for_exit_key
from contracts.exceptions import CannotSignCompletedContractException
from contracts.models import Status
from contracts.schemas import ContractBaseSchema
from contracts.validators import ContractValidator
from services.contracts import create_contract, sign_contract, complete_contract, get_contracts
from utils.exceptions import BreakAllLoops, ValidationException

refresh_contracts: RefreshContractsFlag = RefreshContractsFlag()


def contract_menu():
    while True:
        clear_console()
        print("Договор:")
        print("1 • Список договоров")
        print("2 • Список проектов")
        print("3 • Информация о договоре")
        print("4 • Создать")
        print("5 • Подтвердить договор")
        print("6 • Завершить договор")
        print("7 • В главное меню")
        print("Q • Завершить работу с программой")
        key = msvcrt.getch()

        match key:
            case b"1":
                _get_contracts()
            case b"2":
                _get_projects()
            case b"3":
                _get_contract_info()
            case b"4":
                _create_contract()
            case b"5":
                _sign_contract()
            case b"6":
                _complete_contract()
            case b"7":
                break
            case b"q" | b"Q" | b"\xa9" | b"\x89" | b"\x17":
                raise BreakAllLoops


def _create_contract():
    clear_console()
    contract_name = input("Введите название договора: ")
    contract_data = ContractBaseSchema(name=contract_name)
    validator = ContractValidator(contract_data)
    try:
        validator.validate()
    except ValidationException as e:
        print(e.details)
    while True:
        print("1 • Подписать договор")
        print("2 • Завершить договор")
        print("3 • Сохранить черновик")
        print("4 • Назад")
        print("Q • Завершить работу с программой")
        key = msvcrt.getch()

        match key:
            case b"1":
                contract_data.status = Status.ACTIVE
                break
            case b"2":
                contract_data.status = Status.COMPLETED
                break
            case b"3":
                break
            case b"4":
                return
            case b"q" | b"Q" | b"\xa9" | b"\x89" | b"\x17":
                raise BreakAllLoops

    contract = create_contract(contract_data)
    refresh_contracts.flag = True
    clear_console()
    if contract:
        postfix = ""
        if contract.status == Status.ACTIVE:
            postfix = " и подтвержден"
        elif contract.status == Status.COMPLETED:
            postfix = " и завершен"
        print(f"Договор №{contract.id} создан{postfix}")
    else:
        print("Не удалось создать договор")
    wait_for_exit_key()


def _sign_contract():
    clear_console()
    contracts = get_contracts()
    # Если нет ни одного чернового договора
    if not any([contract.status == Status.DRAFT for contract in contracts]):
        print("Нет ни одного чернового договора")
        wait_for_exit_key()
        return
    contract = _get_contracts(only_draft=True)
    # Если ничего не выбрано
    if not contract:
        return
    try:
        signed_contract = sign_contract(contract.id)
        if signed_contract:
            print(f"Договор №{signed_contract.id} успешно подтвержден")
            refresh_contracts.flag = True
        else:
            print("Ничего не изменилось")
        wait_for_exit_key()
    except CannotSignCompletedContractException as e:
        print(e.message)
        wait_for_exit_key()


def _complete_contract():
    clear_console()
    contracts = get_contracts()
    # Если нет ни одного активного договора
    if not any([contract.status == Status.ACTIVE for contract in contracts]):
        print("Нет ни одного активного договора")
        wait_for_exit_key()
        return
    contract = _get_contracts(only_active=True)
    # Если ничего не выбрано
    if not contract:
        return
    try:
        completed_contract = complete_contract(contract.id)
        if completed_contract:
            print(f"Договор №{completed_contract.id} успешно завершен")
            refresh_contracts.flag = True
        else:
            print("Ничего не изменилось")
        wait_for_exit_key()
    except CannotSignCompletedContractException as e:
        print(e.message)
        wait_for_exit_key()
