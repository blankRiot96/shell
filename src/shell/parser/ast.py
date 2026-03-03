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


@dataclass
class ColumnNode(ArgumentNode):
    column_name: str


@dataclass
class StringLiteralNode(ArgumentNode):
    string_literal: str


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
