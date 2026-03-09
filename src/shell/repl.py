import getpass
from pathlib import Path

from shell.eval.line import evaluate_line


def start_repl_session():
    cwd = Path.cwd()

    while True:
        line = input(f"{getpass.getuser()}:{cwd}$ ")
        result = evaluate_line(line)
        try:
            print(result.printable_string())
        except NotImplementedError:
            pass
