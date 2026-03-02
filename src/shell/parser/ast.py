from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from enum import Enum, auto


class Node(ABC):
    children: list[Node]

    def are_children_equal(self, other: list[Node]) -> bool:
        for child_i, other_i in zip(self.children, other):
            if child_i != other_i:
                return False

            if not child_i.are_children_equal(other_i.children):
                return False
        return True


@dataclass
class ModuleNode(Node):
    children: list[Node] = field(default_factory=list)


@dataclass
class BuiltinCommandNode(Node):
    command_name: str
    children: list[Node] = field(default_factory=list)


@dataclass
class ArgumentNode(Node):
    argument_literal: str
    children: list[Node] = field(default_factory=list)


@dataclass
class PipeNode(Node):
    input_node: Node
    output_node: Node
    children: list[Node] = field(default_factory=list)


class AST:
    def __init__(self, head: Node) -> None:
        self.head = head

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, AST):
            return False

        return value.head == self.head and value.head.are_children_equal(
            self.head.children
        )
