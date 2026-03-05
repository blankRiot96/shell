import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


class ShellObject(ABC):
    @abstractmethod
    def printable_string(self) -> str:
        """
        Return the string representation of this
        object to be displayed
        """
        raise NotImplementedError


@dataclass
class RawText(ShellObject):
    raw_string: str

    def printable_string(self) -> str:
        return self.raw_string


@dataclass
class Date(ShellObject):
    year: int
    month: int
    day: int

    @classmethod
    def from_epoch_time(cls, epoch: float) -> Date:
        # https://www.geeksforgeeks.org/python/how-to-get-file-creation-and-modification-date-or-time-in-python/
        m_ti = time.ctime(epoch)
        t_obj = time.strptime(m_ti)
        year, month, day = t_obj.tm_year, t_obj.tm_mon, t_obj.tm_mday
        return cls(year, month, day)

    def printable_string(self) -> str:
        return f"{self.day}-{self.month}-{self.year}"


@dataclass
class Time(ShellObject):
    hours: int
    minutes: int
    seconds: int

    @classmethod
    def from_epoch_time(cls, epoch: float) -> Time:
        # https://www.geeksforgeeks.org/python/how-to-get-file-creation-and-modification-date-or-time-in-python/
        m_ti = time.ctime(epoch)
        t_obj = time.strptime(m_ti)
        hours, minutes, seconds = t_obj.tm_hour, t_obj.tm_min, t_obj.tm_sec
        return cls(hours, minutes, seconds)

    def printable_string(self) -> str:
        attrs = (self.hours, self.minutes, self.seconds)

        def left_pad(num: int) -> str:
            """Convert '9' to '09' but let '12' stay '12'"""
            return str(num).zfill(2)

        return ":".join(map(left_pad, attrs))


@dataclass
class FileSize(ShellObject):
    n_bytes: int

    def __gt__(self, other: FileSize) -> bool:
        return self.n_bytes > other.n_bytes

    def printable_string(self) -> str:
        strbytes = str(self.n_bytes)
        if len(strbytes) > 12:
            return f"{strbytes[:-12]} TB"
        elif len(strbytes) > 9:
            return f"{strbytes[:-9]} GB"
        elif len(strbytes) > 6:
            return f"{strbytes[:-6]} MB"
        elif len(strbytes) > 3:
            return f"{strbytes[:-3]} KB"

        return f"{strbytes} B"


@dataclass
class Column(ShellObject):
    name: str
    objects: list[ShellObject]

    def printable_string(self) -> str:
        longest_row = len(
            max(
                self.objects, key=lambda obj: len(obj.printable_string())
            ).printable_string()
        )
        output_lines = [
            self.name.ljust(longest_row, " "),
            "-" * longest_row,
            *(obj.printable_string().ljust(longest_row, " ") for obj in self.objects),
        ]

        return "\n".join(output_lines)


@dataclass
class Table(ShellObject):
    columns: list[Column]

    def printable_string(self) -> str:
        output_lines = []
        column_lines = [col.printable_string().splitlines() for col in self.columns]

        for lines in zip(*column_lines):
            output_lines.append(" | ".join(lines))

        return "\n".join(output_lines)
