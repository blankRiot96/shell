import getpass
from pathlib import Path

from shell.eval.line import evaluate_line


def start_repl_session():
    cwd = Path.cwd()

    while True:
        line = input(f"{getpass.getuser()}:{cwd}$ ")
        print(evaluate_line(line).printable_string())
