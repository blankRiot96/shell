from shell.parser.ast import AST, ArgumentNode, BuiltinCommandNode, ModuleNode
from shell.parser.tokenize import TokenType, create_tokens_from_code


def create_ast_from_code(code: str) -> AST:
    ast = AST(head=ModuleNode())
    tokens = create_tokens_from_code(code)
    # TODO

    return ast
