import msvcrt
from copy import copy

from cli.flags import RefreshContractsFlag, RefreshProjectsFlag
from cli.utils import clear_console, wait_for_exit_key
from config import Config
from contracts.models import Status
from contracts.schemas import ContractSchema
from projects.schemas import ProjectSchema
from services.contracts import get_contracts, get_contract, print_contract
from services.projects import get_projects, get_project, print_project
from utils.exceptions import BreakAllLoops

config = Config.load()
projects = None
contracts = None
refresh_contracts: RefreshContractsFlag = RefreshContractsFlag()
refresh_projects: RefreshProjectsFlag = RefreshProjectsFlag()


def _get_projects(return_selected: bool = False):
    # Variables
    global projects
    page_size = config.console.page_size
    current_page = 1

    while True:
        clear_console()
        if projects is None or refresh_projects.flag:
            projects = get_projects()
            refresh_projects.flag = False

        # Info
        if not projects:
            print("Нет проектов")
            wait_for_exit_key()
            return

        # Header
        if not return_selected:
            print("Нажмите на порядковый номер проекта в списке для просмотра подробной информации о нем\n")
        else:
            print("Нажмите на порядковый номер проекта в списке для его выбора\n")

        # Pagination
        num_projects = len(projects)
        start_index = (current_page - 1) * page_size
        end_index = current_page * page_size
        current_projects = projects[start_index:end_index]

        # List
        for i, contract in enumerate(current_projects, start=start_index + 1):
            print(f"{i % page_size if i != page_size * current_page else page_size} • {contract}")

        # Navigation
        if num_projects > page_size:
            print(f"Страница {current_page}/{(num_projects + page_size - 1) // page_size}")
            print("Назад ← | → Вперед | Q Вернуться")
        else:
            print("\nQ Вернуться")

        # Key pressing handling
        while True:
            key = msvcrt.getch()

            if key in (b"q", b"Q", b"\xa9", b"\x89", b"\x17"):
                clear_console()
                return
            elif key == b"M" and current_page < (num_projects + page_size - 1) // page_size:
                current_page += 1
                break
            elif key == b"K" and current_page > 1:
                current_page -= 1
                break
            elif key.isdigit():
                project = get_project(current_projects[int(key) - 1].id)
                clear_console()
                if not return_selected:
                    _project_info_menu(project)
                else:
                    return project
                break
        clear_console()


def _project_info_menu(project: ProjectSchema):
    while True:
        clear_console()
        print_project(project)

        while True:
            key = msvcrt.getch()

            if key in (b"q", b"Q", b"\xa9", b"\x89", b"\x17"):
                clear_console()
                return
            elif key == b"\r":
                _get_contracts(include_project_id=project.id)
                break


def _get_contracts(
    only_draft: bool = False,
    only_active: bool = False,
    include_project_id: int = None,
    exclude_project_id: int = None,
    exclude_contracts: list[ContractSchema] | None = None,
    exclude_projects_with_contracts: bool = False,
):
    # Variables
    global contracts
    page_size = config.console.page_size
    current_page = 1

    while True:
        clear_console()
        if contracts is None or refresh_contracts.flag:
            contracts = get_contracts()
            refresh_contracts.flag = False
        contracts_copy = copy(contracts)

        description_text = ""
        if (
            only_draft,
            only_active,
            include_project_id,
            exclude_project_id,
            exclude_contracts,
            exclude_projects_with_contracts,
        ):
            description_text += "Представлены договоры"
        # Filters
        if only_draft:
            contracts_copy = list(filter(lambda c: c.status == Status.DRAFT, contracts_copy))
            description_text += ', имеющие статус "Черновик"'
        if only_active:
            contracts_copy = list(filter(lambda c: c.status == Status.ACTIVE, contracts_copy))
            description_text += ', имеющие статус "Активен"'
        if include_project_id:
            contracts_copy = list(
                filter(lambda c: c.project.id == include_project_id if c.project else False, contracts_copy)
            )
            description_text += f", привязанные к текущему проекту №{include_project_id}"
        if exclude_project_id:
            contracts_copy = list(
                filter(lambda c: c.project.id != exclude_project_id if c.project else False, contracts_copy)
            )
            description_text += f", не привязанные к текущему проекту №{exclude_project_id}"
        if exclude_contracts:
            contracts_copy = list(filter(lambda c: c not in exclude_contracts, contracts_copy))
        if exclude_projects_with_contracts:
            contracts_copy = list(filter(lambda c: not c.project, contracts_copy))

        # Info
        if not contracts_copy:
            print("Нет договоров")
            wait_for_exit_key()
            return
        if len(description_text) > 0:
            print(description_text)

        # Pagination
        num_contracts = len(contracts_copy)
        start_index = (current_page - 1) * page_size
        end_index = current_page * page_size
        current_contracts = contracts_copy[start_index:end_index]

        # Header
        print("⟳ – Активен | ✓ – Завершен")
        print("––––––––––––––––––––––––––")
        if not (
            only_draft,
            only_active,
            include_project_id,
            exclude_project_id,
            exclude_contracts,
            exclude_projects_with_contracts,
        ):
            print("Нажмите на порядковый номер договора в списке для просмотра подробной информации о нем\n")
        else:
            print("Нажмите на порядковый номер договора в списке для его выбора\n")

        # List
        for i, contract in enumerate(current_contracts, start=start_index + 1):
            print(f"{i % page_size if i != page_size * current_page else page_size} • {contract}")

        # Navigation
        if num_contracts > page_size:
            print(f"Страница {current_page}/{(num_contracts + page_size - 1) // page_size}")
            print("Назад ← | → Вперед | Q Вернуться")
        else:
            print("\nQ Вернуться")

        # Key pressing handling
        while True:
            key = msvcrt.getch()

            if key in (b"q", b"Q", b"\xa9", b"\x89", b"\x17"):
                clear_console()
                return
            elif key == b"M" and current_page < (num_contracts + page_size - 1) // page_size:
                current_page += 1
                break
            elif key == b"K" and current_page > 1:
                current_page -= 1
                break
            elif key.isdigit():
                contract = get_contract(current_contracts[int(key) - 1].id)
                clear_console()
                if not (
                    only_draft,
                    only_active,
                    include_project_id,
                    exclude_project_id,
                    exclude_contracts,
                    exclude_projects_with_contracts,
                ):
                    print_contract(contract)
                else:
                    return contract
                wait_for_exit_key()
                break
        clear_console()


def _get_contract_info():
    while True:
        while True:
            clear_console()
            contract_id = input("Введите номер договора (для завершения программы введите q): ")
            try:
                if contract_id in ("q", "Q"):
                    raise BreakAllLoops
                contract_id = int(contract_id)
                break
            except ValueError:
                print("Неверный ввод. Введите число")
        contract = get_contract(contract_id)
        if not contract:
            print("Договор не найден")
            wait_for_exit_key()
            clear_console()
            continue
        print_contract(contract)
        wait_for_exit_key()
        break
