from shell.parser.ast import (
    AST,
    ArgumentNode,
    BuiltinCommandNode,
    ColumnNode,
    CommandNode,
    Node,
    PipeNode,
    StringLiteralNode,
)
from shell.parser.tokenize import TokenType, create_tokens_from_code


def create_ast_from_code(code: str) -> AST:
    ast = AST(root=CommandNode())
    tokens = create_tokens_from_code(code)

    curr: Node | None = None
    for token in tokens[::-1][1:]:
        if token.type in (
            TokenType.ARGUMENT,
            TokenType.COLUMN_NAME,
            TokenType.STRING_LITERAL,
        ):
            if token.type == TokenType.ARGUMENT:
                resultant_node = ArgumentNode(token.value.decode())
            elif token.type == TokenType.COLUMN_NAME:
                resultant_node = ColumnNode(
                    token.value.decode(), token.value.decode().removeprefix(".")
                )
            elif token.type == TokenType.STRING_LITERAL:
                resultant_node = StringLiteralNode(
                    token.value.decode(), token.value.decode()
                )
            else:
                raise ValueError("Invalid Argument Token")
            if curr is None:
                curr = resultant_node
            elif isinstance(curr, ArgumentNode):
                curr = BuiltinCommandNode("", [curr, resultant_node])
            elif isinstance(curr, BuiltinCommandNode):
                curr.arguments.append(resultant_node)
            elif isinstance(curr, PipeNode):
                curr.input_node = BuiltinCommandNode("", [resultant_node])
        elif token.type == TokenType.BUILTIN_COMMAND:
            if curr is None:
                curr = BuiltinCommandNode(token.value.decode())
            elif isinstance(curr, BuiltinCommandNode):
                curr = BuiltinCommandNode(
                    token.value.decode(), arguments=curr.arguments[::-1]
                )
            elif isinstance(curr, ArgumentNode):
                curr = BuiltinCommandNode(token.value.decode(), arguments=[curr])
            elif isinstance(curr, PipeNode):
                pipe_traversal_curr = curr.input_node
                prev = curr
                while isinstance(pipe_traversal_curr, PipeNode):
                    prev = pipe_traversal_curr
                    pipe_traversal_curr = pipe_traversal_curr.input_node

                if pipe_traversal_curr is None:
                    pipe_traversal_curr = BuiltinCommandNode("")

                assert isinstance(pipe_traversal_curr, BuiltinCommandNode)
                prev.input_node = BuiltinCommandNode(
                    token.value.decode(), pipe_traversal_curr.arguments
                )
        elif token.type == TokenType.PIPE:
            if isinstance(curr, BuiltinCommandNode):
                curr = PipeNode(None, curr)
            elif isinstance(curr, PipeNode):
                curr = PipeNode(PipeNode(None, curr.input_node), curr.output_node)

    ast.root.child = curr
    return ast
