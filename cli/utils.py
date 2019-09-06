import colorama
from pyfiglet import figlet_format
from pathlib import Path

colorama.init(autoreset=True)

root_dir = Path('__file__').resolve().parent.parent


def get_path_from_root_dir(path: str) -> str:
    return str(root_dir.joinpath(path))


def log(string, color=colorama.Fore.GREEN, font="slant", figlet=False):
    if not figlet:
        print(f'{color}{string}')
    else:
        print(f'{color}{figlet_format(string, font=font)}')
