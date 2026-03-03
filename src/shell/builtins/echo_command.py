from shell.builtins.objects import RawText
from shell.parser.ast import ArgumentNode


def eval_echo(arguments: list[ArgumentNode]) -> RawText:
    return RawText(" ".join((arg.argument_literal for arg in arguments)))
