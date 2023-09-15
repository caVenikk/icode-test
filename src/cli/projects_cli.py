import msvcrt

from cli.depenpencies import _get_contracts, _get_projects, _project_info_menu
from cli.flags import RefreshProjectsFlag, RefreshContractsFlag
from cli.utils import clear_console, wait_for_exit_key
from contracts.models import Status
from contracts.schemas import ContractSchema
from projects.schemas import ProjectBaseSchema, ProjectWithContractsSchema, ContractInProjectSchema
from projects.validators import ProjectValidator
from services.contracts import complete_contract, get_contracts
from services.projects import create_project, get_project, attach_contract_to_project
from utils.exceptions import BreakAllLoops, ValidationException

refresh_projects: RefreshProjectsFlag = RefreshProjectsFlag()
refresh_contracts: RefreshContractsFlag = RefreshContractsFlag()


def project_menu():
    while True:
        clear_console()
        print("Проект:")
        print("1 • Список проектов")
        print("2 • Список договоров")
        print("3 • Информация о проекте")
        print("4 • Создать")
        print("5 • Добавить договор")
        print("6 • Завершить договор")
        print("7 • В главное меню")
        print("Q • Завершить работу с программой")
        key = msvcrt.getch()

        match key:
            case b"1":
                _get_projects()
            case b"2":
                _get_contracts()
            case b"3":
                _get_project_info()
            case b"4":
                _create_project()
            case b"5":
                _attach_contract()
            case b"6":
                _complete_contract_from_project()
            case b"7":
                break
            case b"q" | b"Q" | b"\xa9" | b"\x89" | b"\x17":
                raise BreakAllLoops


def _get_project_info():
    while True:
        while True:
            clear_console()
            project_id = input("Введите номер проекта (для завершения программы введите Q): ")
            try:
                if project_id in ("q", "Q"):
                    raise BreakAllLoops
                project_id = int(project_id)
                break
            except ValueError:
                print("Неверный ввод. Введите число")
        project = get_project(project_id)
        if not project:
            print("Проект не найден")
            wait_for_exit_key()
            clear_console()
            continue
        _project_info_menu(project)
        break


def _create_project():
    clear_console()
    contracts = get_contracts()
    if not any([contract.status == Status.ACTIVE for contract in contracts]):
        print("Невозможно создать проект, если нет хотя бы одного активного договора")
        wait_for_exit_key()
        return
    project_name = input("Введите название проекта: ")
    project_data = ProjectBaseSchema(name=project_name)
    validator = ProjectValidator(project_data)
    try:
        validator.validate()
    except ValidationException as e:
        print(e.details)
    attached_contracts: list[ContractSchema | ContractInProjectSchema] = []
    while True:
        clear_console()
        print("1 • Добавить договор")
        print("2 • Сохранить")
        print("3 • Назад")
        print("Q • Завершить работу с программой")
        key = msvcrt.getch()

        match key:
            case b"q" | b"Q" | b"\xa9" | b"\x89" | b"\x17":
                raise BreakAllLoops
            case b"1":
                active_attached_contracts = [
                    contract for contract in attached_contracts if contract.status == Status.ACTIVE
                ]
                if len(active_attached_contracts) >= 1:
                    clear_console()
                    print("В проекте может быть только один активный договор")
                    wait_for_exit_key()
                else:
                    contract = _get_contracts(only_active=True, exclude_contracts=attached_contracts)
                    if contract:
                        attached_contracts.append(contract)
                        clear_console()
                        print(f"Добавлен договор №{contract.id}")
                        wait_for_exit_key()
            case b"2":
                break
            case b"3":
                return
    if len(attached_contracts) > 0:
        attached_contracts = [
            ContractInProjectSchema(**{k: v for k, v in contract.dict().items() if k != "project"})
            for contract in attached_contracts
        ]
        project_data = ProjectWithContractsSchema(name=project_name, contracts=attached_contracts)
    project = create_project(project_data)
    refresh_projects.flag = True
    clear_console()
    if project:
        print(f'Проект "{project.name}" №{project.id} создан')
    else:
        print("Не удалось создать проект")
    wait_for_exit_key()


def _attach_contract():
    project = _get_projects(return_selected=True)
    if len(list(filter(lambda c: c.status == Status.ACTIVE, project.contracts))):
        clear_console()
        print("В проекте может быть только один активный договор")
        wait_for_exit_key()
        return
    while True:
        clear_console()
        contract = _get_contracts(only_active=True, exclude_projects_with_contracts=True)
        if contract:
            attach_contract_to_project(project.id, contract)
            refresh_projects.flag = True
            refresh_contracts.flag = True
            clear_console()
            print(f"Добавлен договор №{contract.id}")
            wait_for_exit_key()
        break


def _complete_contract_from_project():
    project = _get_projects(return_selected=True)
    if len(list(filter(lambda c: c.status == Status.ACTIVE, project.contracts))) == 0:
        clear_console()
        print("В проекте нет активных договоров")
        wait_for_exit_key()
        return
    while True:
        clear_console()
        contract = _get_contracts(only_active=True, include_project_id=project.id)
        if contract:
            complete_contract(contract.id)
            refresh_projects.flag = True
            refresh_contracts.flag = True
            clear_console()
            print(f"Завершен договор №{contract.id}")
            wait_for_exit_key()
        break
