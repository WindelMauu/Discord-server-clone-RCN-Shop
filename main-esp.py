from os import system
import psutil
import os
from pypresence import Presence
import random
import time
import sys
import discord
import json
import traceback
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.panel import Panel as RichPanel
from rich.progress import Progress
import asyncio
from colorama import Fore, init, Style
import platform
import inquirer
from cloner import Clone

version = '1.4'
clones = {'Clones_teste_feitos': 0}
console = Console()


def loading(seconds):
    with Progress() as progress:
        task = progress.add_task("", total=seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)


def clearall():
    system('clear')
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


{Style.RESET_ALL}{Fore.RESET}""")


def get_user_preferences():
    preferences = {}
    preferences['guild_edit'] = True
    preferences['channels_delete'] = True
    preferences['roles_create'] = True
    preferences['categories_create'] = True
    preferences['channels_create'] = True
    preferences['alterarrich'] = True
    preferences['emojis_create'] = False

    def map_boolean_to_string(value):
        return "Si" if value else "No"

    panel_title = "Config BETA"
    panel_content = "\n"
    panel_content += f"- Modificar nombre e ícono del servidor: {map_boolean_to_string(preferences.get('guild_edit', False))}\n"
    panel_content += f"- Remplazar los canales del servidor: {map_boolean_to_string(preferences.get('channels_delete', False))}\n"
    panel_content += f"- Clonar los rangos: {map_boolean_to_string(preferences.get('roles_create', False))}\n"
    panel_content += f"- Clonar las categorías: {map_boolean_to_string(preferences.get('categories_create', False))}\n"
    panel_content += f"- Clonar los canales: {map_boolean_to_string(preferences.get('channels_create', False))}\n"
    panel_content += f"- Clonar los emojis: {map_boolean_to_string(preferences.get('emojis_create', False))}\n"
    panel_content += f"- Rich presence: {map_boolean_to_string(preferences.get('alterarrich', False))}\n"
    console.print(
        RichPanel(panel_content,
                  title=panel_title,
                  style="bold blue",
                  width=70))

    questions = [
        inquirer.List(
            'reconfigure',
            message='¿Quieres poner la configuración predeterminada?',
            choices=['Si', 'No'],
            default='Si')
    ]

    answers = inquirer.prompt(questions)

    reconfigure = answers['reconfigure']
    if reconfigure == 'Sim':
        questions = [
            inquirer.Confirm(
                'guild_edit',
                message='¿Quieres editar el icono y el nombre del servidor?',
                default=False),
            inquirer.Confirm('channels_delete',
                             message='¿Quieres eliminar canales?',
                             default=False),
            inquirer.Confirm(
                'roles_create',
                message=
                '¿Quieres clonar los rangos? (NO SE RECOMIENDA DESHABILITAR)',
                default=False),
            inquirer.Confirm('categories_create',
                             message='¿Quieres clonar las categorías?',
                             default=False),
            inquirer.Confirm('channels_create',
                             message='¿Quieres clonar los canales?',
                             default=False),
            inquirer.Confirm('alterarrich',
                             message='Desea desativar rich presence?',
                             default=False),
            inquirer.Confirm(
                'emojis_create',
                message=
                '¿Quieres clonar los Emojis? (SE RECOMIENDA ACTIVAR ESTA OPCIÓN SOLO (SOLO) PARA EVITAR ERRORES)',
                default=False)
        ]

        answers = inquirer.prompt(questions)
        preferences['guild_edit'] = answers['guild_edit']
        preferences['channels_delete'] = answers['channels_delete']
        preferences['roles_create'] = answers['roles_create']
        preferences['categories_create'] = answers['categories_create']
        preferences['channels_create'] = answers['channels_create']
        preferences['emojis_create'] = answers['emojis_create']
    clearall()
    return preferences


versao_python = sys.version.split()[0]


def restart():
    python = sys.executable
    os.execv(python, [python] + sys.argv)


client = discord.Client()
if os == "Windows":
    system("cls")
else:
    print(chr(27) + "[2J")
    clearall()
while True:
    token = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Inserta tu token para continuar{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild_s = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Ingrese el ID del servidor que desea clonar{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Ingrese el ID del servidor donde se clonara para pegar el servidor copiado{Style.RESET_ALL}{Fore.RESET}\n>'
    )
    clearall()
    print(f'{Style.BRIGHT}{Fore.GREEN}Los valores ingresados son:')
    token_length = len(token)
    hidden_token = "*" * token_length
    print(
        f'{Style.BRIGHT}{Fore.GREEN}Tú token: {Fore.YELLOW}{hidden_token}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID del servidor a clonar: {Fore.YELLOW}{guild_s}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID del servidor en el que desea pegar el servidor clonado: {Fore.YELLOW}{guild}{Style.RESET_ALL}{Fore.RESET}'
    )
    confirm = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}¿Son correctos los valores? {Fore.YELLOW}(Y/N){Style.RESET_ALL}{Fore.RESET}\n >'
    )
    if confirm.upper() == 'Y':
        if not guild_s.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}El ID del servidor a clonar solo debe contener números.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not guild.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}El ID del servidor de destino solo debe contener números.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not token.strip() or not guild_s.strip() or not guild.strip():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}Uno o más campos están en blanco.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if len(token.strip()) < 3 or len(guild_s.strip()) < 3 or len(
                guild.strip()) < 3:
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}Uno o más campos tienen menos de 3 caracteres.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        break
    elif confirm.upper() == 'N':
        clearall()
    else:
        clearall()
        print(
            f'{Style.BRIGHT}{Fore.RED}Opción inválida. Por favor ingrese Y o N.{Style.RESET_ALL}{Fore.RESET}'
        )
input_guild_id = guild_s
output_guild_id = guild
token = token
clearall()


@client.event
async def on_ready():
    try:
        start_time = time.time()
        global clones
        table = Table(title="Versões", style="bold magenta", width=85)
        table.add_column("Componente", width=35)
        table.add_column("Versão", style="cyan", width=35)
        table.add_row("Clonador", version)
        table.add_row("Discord.py", discord.__version__)
        table.add_row("Python", versao_python)
        console.print(RichPanel(table, width=69))
        console.print(
            RichPanel(f" Autenticación exitosa en {client.user.name}",
                      style="bold green",
                      width=69))
        print(f"\n")
        loading(3)
        clearall()
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        preferences = get_user_preferences()

        if not any(preferences.values()):
            preferences = {k: True for k in preferences}
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="WindelMau - Join: https://discord.gg/8DR9XygHtV",
            state="https://discord.gg/8DR9XygHtV")
        if preferences['alterarrich']:
            await client.change_presence(activity=activity)
        if preferences['guild_edit']:
            await Clone.guild_edit(guild_to, guild_from)
        if preferences['channels_delete']:
            await Clone.channels_delete(guild_to)
        if preferences['roles_create']:
            await Clone.roles_create(guild_to, guild_from)
        if preferences['categories_create']:
            await Clone.categories_create(guild_to, guild_from)
        if preferences['channels_create']:
            await Clone.channels_create(guild_to, guild_from)
        if preferences['emojis_create']:
            await Clone.emojis_create(guild_to, guild_from)

        end_time = time.time()
        duration = end_time - start_time
        duration_str = time.strftime("%M:%S", time.gmtime(duration))

        print("\n\n")
        print(
            f"{Style.BRIGHT}{Fore.BLUE} El servidor ha sido clonado exitosamente en {Fore.YELLOW}{duration_str}{Style.RESET_ALL}"
        )
        print(
            f"{Style.BRIGHT}{Fore.BLUE} Visita nuestro servidor de Discord: {Fore.YELLOW}https://discord.gg/8DR9XygHtV{Style.RESET_ALL}"
        )
        with open('saves.json', 'r') as f:
            clones = json.load(f)
        clones['Clones_teste_feitos'] += 1
        with open('saves.json', 'w') as f:
            json.dump(clones, f)
        print(
            f"{Style.BRIGHT}{Fore.BLUE} Finalizado el proceso y sesión cerrada en la cuenta {Fore.YELLOW}{client.user}"
        )
        await asyncio.sleep(30)
        await client.close()  #fecha o codigo

    except discord.LoginFailure:
        print(
            "No se puede autenticar en la cuenta. Compruebe que el token sea correcto."
        )
    except discord.Forbidden:
        print(
            "No se pudo realizar la clonación debido a permisos insuficientes (Admin)."
        )
    except discord.NotFound:
        print(
            "No fue posible encontrar ninguno de los elementos de la copia (canales, categorías, etc.)."
        )
    except discord.HTTPException:
        print(
            "Hubo un error al comunicarse con la API de Discord. En 20 segundos, el código continuará donde se dejó."
        )
        loading(20)

        await Clone.emojis_create(guild_to, guild_from)
    except asyncio.TimeoutError:
        print(f"Ocorreu um erro: TimeOut")
    except Exception as e:

        print(Fore.RED + " Ocorreu um erro:", e)
        print("\n")
        traceback.print_exc()
        panel_text = (
            f"1. ID de servidor incorrecto\n"
            f"2. No estás en el servidor ingresado\n"
            f"3. El servidor ingresado no existe\n"
            f"¿Aún no está resuelto? Por favor contacte al desarrollador en [link=https://discord.gg/8DR9XygHtV]https://discord.gg/8DR9XygHtV[/link]"
        )
        console.print(
            RichPanel(panel_text,
                      title="Posibles causas y soluciones.",
                      style="bold red",
                      width=70))
        print(
            Fore.YELLOW +
            "\nEl código se reiniciará en 20 segundos. Si no quieres esperar, actualiza la página y comienza de nuevo."
        )
        print(Style.RESET_ALL)
        loading(20)
        restart()
        print(Fore.RED + "Reiniciando...")


try:
    client.run(token, bot=False)
except discord.LoginFailure:
    print(Fore.RED + "El token ingresado no es válido")
    print(
        Fore.YELLOW +
        "\n\nEl código se reiniciará en 10 segundos. Si no quieres esperar, actualiza la página y comienza de nuevo."
    )
    print(Style.RESET_ALL)
    loading(10)
    restart()
    clearall()
    print(Fore.RED + "Reiniciando...")
