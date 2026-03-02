from collections import deque
from dataclasses import dataclass
from enum import Enum, auto


def string_to_bytearray(string: str) -> bytearray:
    return bytearray(map(ord, string))


BUILTIN_COMMAND_NAMES = ("echo", "select", "sort", "ls")
BUILTIN_COMMAND_NAMES = tuple(map(string_to_bytearray, BUILTIN_COMMAND_NAMES))


class TokenType(Enum):
    BUILTIN_COMMAND = auto()
    STRING_LITERAL = auto()
    COLUMN_NAME = auto()
    SINGLE_DASH_FLAGS = auto()
    DOUBLE_DASH_FLAGS = auto()
    ARGUMENT = auto()
    PIPE = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: bytearray


def create_tokens_from_code(code: str) -> list[Token]:
    tokens = []
    segment = bytearray()
    queue: deque[Token] = deque()
    for char in code + " ":
        if char == "|":
            queue.append(Token(TokenType.PIPE, string_to_bytearray("|")))
        elif char != " ":
            segment.append(ord(char))
            continue

        if segment in BUILTIN_COMMAND_NAMES:
            tokens.append(Token(TokenType.BUILTIN_COMMAND, segment))
        elif segment.startswith(b'"'):
            tokens.append(Token(TokenType.STRING_LITERAL, segment))
        elif segment.startswith(b"."):
            tokens.append(Token(TokenType.COLUMN_NAME, segment))
        elif segment.startswith(b"--"):
            tokens.append(Token(TokenType.DOUBLE_DASH_FLAGS, segment))
        elif segment.startswith(b"-"):
            tokens.append(Token(TokenType.SINGLE_DASH_FLAGS, segment))
        else:
            tokens.append(Token(TokenType.ARGUMENT, segment))

        tokens.extend(queue)
        queue.clear()
        segment = bytearray()

    tokens.append(Token(TokenType.EOF, bytearray()))
    return tokens
