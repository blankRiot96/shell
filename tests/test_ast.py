import pytest
from shell.parser.parse import produce_ast
from shell.parser.ast import AST, BuiltinCommandNode, ArgumentNode


def test_equality():
    ast_1 = AST(
        head=BuiltinCommandNode(
            command_name="echo", children=[ArgumentNode(argument_literal='"hii"')]
        )
    )
    ast_2 = AST(
        head=BuiltinCommandNode(
            command_name="echo", children=[ArgumentNode(argument_literal='"hii"')]
        )
    )

    assert ast_1 == ast_2


def test_inequality():
    ast_1 = AST(
        head=BuiltinCommandNode(
            command_name="echo", children=[ArgumentNode(argument_literal='"hii"')]
        )
    )
    ast_2 = AST(
        head=BuiltinCommandNode(
            command_name="meow", children=[ArgumentNode(argument_literal='"hii"')]
        )
    )

    assert ast_1 != ast_2


def test_child_inequality():
    ast_1 = AST(
        head=BuiltinCommandNode(
            command_name="echo", children=[ArgumentNode(argument_literal='"hii"')]
        )
    )
    ast_2 = AST(
        head=BuiltinCommandNode(
            command_name="echo", children=[ArgumentNode(argument_literal='"guh"')]
        )
    )

    assert ast_1 != ast_2


def test_inner_deep_child_inequality():
    ast_1 = AST(
        head=BuiltinCommandNode(
            command_name="echo",
            children=[
                ArgumentNode(
                    '"hii"',
                    children=[ArgumentNode("meow", children=[ArgumentNode("guh")])],
                )
            ],
        )
    )
    ast_2 = AST(
        head=BuiltinCommandNode(
            command_name="echo",
            children=[
                ArgumentNode(
                    '"hii"',
                    children=[ArgumentNode("meow", children=[ArgumentNode("grr")])],
                )
            ],
        )
    )

    assert ast_1 != ast_2
