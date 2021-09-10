import subprocess
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level="INFO")

import click

BASE_PATH = Path(__file__).parent


def get_all_wsl():
    cmd = "wsl -l -q"
    res = subprocess.check_output(cmd, shell=True)
    wsl_list = res.decode("utf-16").split("\r\n")
    wsl_list = list(filter(None, wsl_list))
    return wsl_list


@click.command()
@click.option('--name',  help='wsl name.')
@click.option('--file', prompt='Input file path',
              help='file path.')
def export_wsl(name, file):
    wsl_list = get_all_wsl()
    if len(wsl_list) < 1:
        logging.error("Your must input wsl name")

    if not name and len(wsl_list) > 1:
        logging.error("Your must input wsl name")
    name = wsl_list[0]

    subprocess.call("wsl --shutdown", shell=True)
    cmd = f"wsl --export {name} {Path(file).absolute()}"
    logging.info(cmd)
    subprocess.call(cmd, shell=True)


def main():
    export_wsl()


if __name__ == "__main__":
    main()
