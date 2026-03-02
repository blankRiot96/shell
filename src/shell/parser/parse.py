from shell.parser.ast import AST
from shell.parser.tokenize import create_tokens_from_code


def create_ast_from_code(code: str) -> AST:
    tokens = create_tokens_from_code(code)
    raise NotImplementedError
