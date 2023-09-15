import msvcrt
import os


def wait_for_exit_key():
    print("Нажмите любую клавишу для продолжения...")
    msvcrt.getch()


def clear_console():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
