import subprocess
import os
from pathlib import Path
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install
import colorama
from colorama import Fore, init, Style

colorama.init
install()

console = Console()


def clear_screen():
    os.system('clear')
    print(f"""{Style.BRIGHT}{Fore.GREEN}
██████╗┼┼█████╗┼███╗┼┼██╗
██╔══██╗██╔══██╗████╗┼██║
██████╔╝██║┼┼╚═╝██╔██╗██║
██╔══██╗██║┼┼██╗██║╚████║
██║┼┼██║╚█████╔╝██║┼╚███║
╚═╝┼┼╚═╝┼╚════╝┼╚═╝┼┼╚══╝
┼██████╗██╗┼┼██╗┼█████╗┼██████╗┼
██╔════╝██║┼┼██║██╔══██╗██╔══██╗
╚█████╗┼███████║██║┼┼██║██████╔╝
┼╚═══██╗██╔══██║██║┼┼██║██╔═══╝┼
██████╔╝██║┼┼██║╚█████╔╝██║┼┼┼┼┼
╚═════╝┼╚═╝┼┼╚═╝┼╚════╝┼╚═╝┼┼┼┼┼


{Style.RESET_ALL}{Fore.MAGENTA}{Fore.RESET}""")


def main():
    clear_screen()
    language = questionary.select("Elige un idioma:",
                                  choices=["esp", "en"]).ask()
    if not is_python_installed():
        clear_screen()
        console.print(
            Panel(f"O Python no está instalado en su sistema.",
                  title="[bold red]Erro[/bold red]"))
        return
    elif not is_main_script_present(language):
        clear_screen()
        console.print(
            Panel(f"Archivo main-{language}.py no encontrado.",
                  title="[bold red]Erro[/bold red]"))

        return
    try:
        subprocess.run([get_python_interpreter(), f"main-{language}.py"])
    except subprocess.CalledProcessError as e:
        clear_screen()
        console.print(
            Panel(f"Error al ejecutar el subproceso: {e}",
                  title="[bold red]Erro[/bold red]"))


def is_python_installed():
    try:
        subprocess.check_output(["python", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False


def is_main_script_present(language):
    return Path(f"main-{language}.py").is_file()


def confirm_execution(language):
    messages = {
        "esp":
        "Está a punto de ejecutar el script main-en.py. ¿Desea continuar?",
        "en":
        "You are about to execute the main-en.py script. Do you want to continue?"
    }
    clear_screen()
    confirmation = questionary.confirm(messages[language]).ask()
    return confirmation


def get_python_interpreter():
    if is_python3_installed():
        return "python3"
    else:
        return "python"


def is_python3_installed():
    try:
        subprocess.check_output(["python3", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    main()