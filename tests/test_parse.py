from shell.parser.ast import AST, CommandNode, PipeNode
from shell.parser.ast import ArgumentNode as AN
from shell.parser.ast import BuiltinCommandNode as BCN
from shell.parser.ast import ColumnNode as CN
from shell.parser.ast import FlagNode as FN
from shell.parser.parse import create_ast_from_code


def test_builtin_command_node():
    assert create_ast_from_code("ls") == AST(CommandNode(BCN("ls")))


def test_args():
    assert create_ast_from_code("sort desc") == AST(
        CommandNode(BCN("sort", [AN("desc")]))
    )
    assert create_ast_from_code("select .date") == AST(
        CommandNode(BCN("select", [CN(".date")]))
    )
    assert create_ast_from_code('echo "hii"') == AST(
        CommandNode(BCN("echo", [AN("hii")]))
    )
    assert create_ast_from_code('echo "multiple words as one"') == AST(
        CommandNode(BCN("echo", [AN("multiple words as one")]))
    )


def test_multiple_args():
    assert create_ast_from_code("select .name .size") == AST(
        CommandNode(BCN("select", [CN(".name"), CN(".size")]))
    )


def test_argless_pipe():
    assert create_ast_from_code("ls|sort") == AST(
        CommandNode(PipeNode(BCN("ls"), BCN("sort")))
    )


def test_pipes():
    assert create_ast_from_code("ls|select .date|sort desc") == AST(
        CommandNode(
            PipeNode(
                PipeNode(BCN("ls"), BCN("select", [CN(".date")])),
                BCN("sort", [AN("desc")]),
            )
        )
    )


def test_compound_selection():
    assert create_ast_from_code("ls | select .name .size | sort .size") == AST(
        CommandNode(
            PipeNode(
                PipeNode(BCN("ls"), BCN("select", [CN(".name"), CN(".size")])),
                BCN("sort", [CN(".size")]),
            )
        )
    )


def test_flags():
    assert create_ast_from_code(
        'ls -a --color=yes ~/p/shell ~/t ~/ "~/my spaced folder"'
    ) == AST(
        CommandNode(
            BCN(
                "ls",
                arguments=[
                    FN("-a"),
                    FN("--color=yes"),
                    AN("~/p/shell"),
                    AN("~/t"),
                    AN("~/"),
                    AN("~/my spaced folder"),
                ],
            )
        )
    )
