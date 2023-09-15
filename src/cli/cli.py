import msvcrt

from cli.contracts_cli import contract_menu
from cli.projects_cli import project_menu
from cli.utils import clear_console
from cli.depenpencies import _get_contracts, _get_projects
from utils.exceptions import BreakAllLoops


def run_cli():
    try:
        while True:
            clear_console()
            print("Главное меню:")
            print("1 • Проект")
            print("2 • Договор")
            print("3 • Список проектов")
            print("4 • Список договоров")
            print("Q • Завершить работу с программой")
            key = msvcrt.getch()

            match key:
                case b"1":
                    project_menu()
                case b"2":
                    contract_menu()
                case b"3":
                    _get_projects()
                case b"4":
                    _get_contracts()
                case b"q" | b"Q" | b"\xa9" | b"\x89" | b"\x17":
                    raise BreakAllLoops

    except BreakAllLoops:
        print("Выход...")
