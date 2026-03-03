from shell.builtins.clear_command import eval_clear
from shell.builtins.echo_command import eval_echo
from shell.builtins.exit_command import run_exit
from shell.builtins.ls_command import eval_ls
from shell.builtins.objects import ShellObject, Table
from shell.builtins.select_command import eval_select
from shell.parser.ast import (
    ArgumentNode,
    BuiltinCommandNode,
    ColumnNode,
    CommandNode,
    Node,
    PipeNode,
    StringLiteralNode,
)
from shell.parser.parse import create_ast_from_code


def traverse_ast(curr: Node, input_object: ShellObject | None = None) -> ShellObject:
    if isinstance(curr, CommandNode):
        assert curr.child is not None
        return traverse_ast(curr.child)
    elif isinstance(curr, BuiltinCommandNode):
        if curr.command_name == "select":
            assert isinstance(input_object, Table)
            return eval_select(input_object, curr.arguments)
        elif curr.command_name == "ls":
            return eval_ls()
        elif curr.command_name == "exit":
            run_exit()
        else:
            raise ValueError(f"Unknown command `{curr.command_name}`")
    elif isinstance(curr, PipeNode):
        assert curr.input_node is not None
        assert curr.output_node is not None

        if isinstance(curr.output_node, BuiltinCommandNode):
            return traverse_ast(curr.output_node, traverse_ast(curr.input_node))
        else:
            raise ValueError("Pipes need an input and output command")
    else:
        raise ValueError(f"Unknown Node `{type(curr)}`")


def evaluate_line(line: str) -> ShellObject:
    ast = create_ast_from_code(line)
    return traverse_ast(ast.root)
