import colorama
from pyfiglet import figlet_format
from pathlib import Path
import configparser

colorama.init(autoreset=True)

root_dir = Path('__file__').resolve().parent.parent

config = configparser.ConfigParser()
config.read('config.ini')


def create_cli_conf_section():
    try:
        config.add_section('cli')
    except configparser.DuplicateSectionError:
        pass


create_cli_conf_section()


def set_conf(key, value):
    config.set('cli', key, value)
    save_conf()


def get_conf(key):
    try:
        return config.get('cli', key)
    except configparser.NoOptionError:
        return ''


def save_conf():
    with open('config.ini', 'w') as f:
        config.write(f)


def get_path_from_root_dir(path: str) -> str:
    return str(root_dir.joinpath(path))


def log(string, color=colorama.Fore.GREEN, font="slant", figlet=False):
    if not figlet:
        print(f'{color}{string}')
    else:
        print(f'{color}{figlet_format(string, font=font)}')
