import pytest

from shell.parser.ast import (
    AST,
    ArgumentNode,
    BuiltinCommandNode,
    CommandNode,
    PipeNode,
)
from shell.parser.ast import ArgumentNode as AN
from shell.parser.ast import BuiltinCommandNode as BCN
from shell.parser.ast import ColumnNode as CN


def test_equality():
    ast_1 = AST(
        CommandNode(
            BuiltinCommandNode("echo", [ArgumentNode(argument_literal='"hii"')])
        )
    )
    ast_2 = AST(
        CommandNode(
            BuiltinCommandNode("echo", [ArgumentNode(argument_literal='"hii"')])
        )
    )

    assert ast_1 == ast_2


def test_inequality():
    ast_1 = AST(
        CommandNode(
            BuiltinCommandNode("echo", [ArgumentNode(argument_literal='"hii"')])
        )
    )
    ast_2 = AST(
        CommandNode(BuiltinCommandNode("ls", [ArgumentNode(argument_literal='"hii"')]))
    )

    assert ast_1 != ast_2


def test_child_inequality():
    ast_1 = AST(
        CommandNode(
            BuiltinCommandNode("echo", [ArgumentNode(argument_literal='"hii"')])
        )
    )
    ast_2 = AST(
        CommandNode(
            BuiltinCommandNode("echo", [ArgumentNode(argument_literal='"byee"')])
        )
    )

    assert ast_1 != ast_2


def test_inner_deep_child_inequality():
    ast_1 = AST(
        CommandNode(
            PipeNode(
                PipeNode(BCN("ls"), BCN("select", [CN(".date")])),
                BCN("sort", [AN("desc")]),
            )
        )
    )
    ast_2 = AST(
        CommandNode(
            PipeNode(
                PipeNode(BCN("ls"), BCN("select", [CN(".date")])),
                BCN("echo", [AN("desc")]),
            )
        )
    )

    assert ast_1 != ast_2
