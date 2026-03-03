import os
import time
from pathlib import Path

from shell.builtins.objects import Column, RawText, Table


def get_sorted_files(working_directory: Path) -> list[Path]:
    all_files = list(working_directory.iterdir())
    directories = [
        file for file in all_files if file.is_dir() and not file.name.startswith(".")
    ]
    directories.sort(key=lambda p: p.name)

    files = [
        file
        for file in all_files
        if not file.is_dir() and not file.name.startswith(".")
    ]
    files.sort(key=lambda p: p.name)

    return directories + files


def get_printable_date_and_time_string(file: Path) -> tuple[str, str]:
    # https://www.geeksforgeeks.org/python/how-to-get-file-creation-and-modification-date-or-time-in-python/
    ti_m = os.path.getmtime(file)
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti)
    return time.strftime("%Y-%m-%d", t_obj), time.strftime("%H:%M:%S", t_obj)


def get_file_size(file: Path) -> str:
    bytes = file.stat().st_size
    strbytes = str(bytes)
    if len(strbytes) > 6:
        return f"{strbytes[:-6]} MB"
    if len(strbytes) > 3:
        return f"{strbytes[:-3]} KB"

    return f"{strbytes} B"


def eval_ls() -> Table:
    filename_col = Column("name", [])
    date_col = Column("date", [])
    time_col = Column("time", [])
    filesize_col = Column("size", [])
    table = Table([filename_col, date_col, time_col, filesize_col])

    cwd = Path.cwd()
    for file in get_sorted_files(cwd):
        filename_col.objects.append(RawText(file.name))
        date, ttime = get_printable_date_and_time_string(file)
        date_col.objects.append(RawText(date))
        time_col.objects.append(RawText(ttime))
        filesize_col.objects.append(RawText(get_file_size(file)))

    return table
