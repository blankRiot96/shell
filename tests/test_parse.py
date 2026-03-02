import pytest

from shell.parser.ast import AST, ModuleNode, PipeNode
from shell.parser.ast import ArgumentNode as AN
from shell.parser.ast import BuiltinCommandNode as BCN
from shell.parser.parse import create_ast_from_code


def test_pipes():
    assert create_ast_from_code("ls|select .date|sort desc") == AST(
        ModuleNode(
            [
                PipeNode(
                    PipeNode(BCN("ls"), BCN("select", [AN(".date")])),
                    BCN("sort", [AN("desc")]),
                )
            ]
        )
    )
