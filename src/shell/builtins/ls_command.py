from pathlib import Path

from shell.builtins.objects import Column, Date, FileSize, RawText, Table, Time


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


def eval_ls() -> Table:
    filename_col = Column("name", [])
    date_col = Column("date", [])
    time_col = Column("time", [])
    filesize_col = Column("size", [])
    table = Table([filename_col, date_col, time_col, filesize_col])

    cwd = Path.cwd()
    for file in get_sorted_files(cwd):
        stat = file.stat()
        filename_col.objects.append(RawText(file.name))
        date_col.objects.append(Date.from_epoch_time(stat.st_mtime))
        time_col.objects.append(Time.from_epoch_time(stat.st_mtime))
        filesize_col.objects.append(FileSize(stat.st_size))

    return table
