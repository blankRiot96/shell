import pytest

from shell.parser.ast import AST, CommandNode, PipeNode
from shell.parser.ast import ArgumentNode as AN
from shell.parser.ast import BuiltinCommandNode as BCN
from shell.parser.ast import ColumnNode as CN
from shell.parser.ast import StringLiteralNode as SLN
from shell.parser.parse import create_ast_from_code


def test_builtin_command_node():
    assert create_ast_from_code("ls") == AST(CommandNode(BCN("ls")))


def test_args():
    assert create_ast_from_code("sort desc") == AST(
        CommandNode(BCN("sort", [AN("desc")]))
    )
    assert create_ast_from_code("select .date") == AST(
        CommandNode(BCN("select", [CN(".date", "date")]))
    )
    assert create_ast_from_code('echo "hii"') == AST(
        CommandNode(BCN("echo", [SLN('"hii"', '"hii"')]))
    )


def test_multiple_args():
    assert create_ast_from_code("select .name .size") == AST(
        CommandNode(BCN("select", [CN(".name", "name"), CN(".size", "size")]))
    )


def test_argless_pipe():
    assert create_ast_from_code("ls|sort") == AST(
        CommandNode(PipeNode(BCN("ls"), BCN("sort")))
    )


def test_pipes():
    assert create_ast_from_code("ls|select .date|sort desc") == AST(
        CommandNode(
            PipeNode(
                PipeNode(BCN("ls"), BCN("select", [CN(".date", "date")])),
                BCN("sort", [AN("desc")]),
            )
        )
    )
