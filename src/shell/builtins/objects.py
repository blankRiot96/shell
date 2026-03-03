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
            "- " * int(longest_row / 2),
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
