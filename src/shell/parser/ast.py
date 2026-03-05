from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field


class Node(ABC):
    pass
    # child: Node | None

    # def are_children_equal(self, other: list[Node]) -> bool:
    #     for child_i, other_i in zip(self.children, other):
    #         if child_i != other_i:
    #             return False

    #         if not child_i.are_children_equal(other_i.children):
    #             return False
    #     return True


@dataclass
class CommandNode(Node):
    child: Node | None = None


@dataclass
class ArgumentNode(Node):
    argument_literal: str


class FlagNode(ArgumentNode):
    def __init__(self, argument_literal: str):
        super().__init__(argument_literal)

        self.flag_value = None
        single_dash = False
        if not argument_literal:
            raise ValueError("Cannot have empty flag")
        elif argument_literal.count("-") > 2:
            raise ValueError("Invalid flag usage. Cannot have more than 2 dashes")
        elif argument_literal.startswith("--"):
            self.flag_name = argument_literal.removeprefix("--")
        elif argument_literal.startswith("-"):
            self.flag_name = argument_literal.removeprefix("-")
            single_dash = True
        else:
            raise ValueError("Invalid flag format")

        equals_index = argument_literal.find("=")
        if equals_index != -1:
            if single_dash:
                raise ValueError("Invalid format `-C=value`, use double dash")
            self.flag_value = argument_literal[equals_index + 1 :]
            if not self.flag_value:
                raise ValueError("Invalid format `--flag=`, value is missing")


class ColumnNode(ArgumentNode):
    def __init__(self, argument_literal: str):
        super().__init__(argument_literal)
        self.column_name = argument_literal.removeprefix(".")


@dataclass
class BuiltinCommandNode(Node):
    command_name: str
    arguments: list[ArgumentNode] = field(default_factory=list)


@dataclass
class PipeNode(Node):
    input_node: Node | None = None
    output_node: Node | None = None


@dataclass
class AST:
    root: CommandNode
