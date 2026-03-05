from collections import deque
from dataclasses import dataclass
from enum import Enum, auto


def string_to_bytearray(string: str) -> bytearray:
    return bytearray(map(ord, string))


BUILTIN_COMMAND_NAMES = ("echo", "select", "sort", "ls", "exit", "clear")
BUILTIN_COMMAND_NAMES = tuple(map(string_to_bytearray, BUILTIN_COMMAND_NAMES))


class TokenType(Enum):
    BUILTIN_COMMAND = auto()
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
    string_started = False
    for char in code + " ":
        if string_started:
            if char == '"':
                string_started = False
                continue
            segment.append(ord(char))
            continue
        elif char == '"':
            string_started = True
        elif char == "|":
            queue.append(Token(TokenType.PIPE, string_to_bytearray("|")))
        elif char != " ":
            segment.append(ord(char))
            continue

        if not segment:
            tokens.extend(queue)
            queue.clear()
            continue

        if (
            segment in BUILTIN_COMMAND_NAMES
            and (not tokens or tokens[-1].type == TokenType.PIPE)
        ):  # TODO: This is a bit janky... basically only allowing commands to be in the position
            # of the first token. Only two patterns allowed:
            # `<command> ...` or `<command> ... | <command> ...`
            tokens.append(Token(TokenType.BUILTIN_COMMAND, segment))
        elif segment.startswith(b'"'):
            tokens.append(
                Token(TokenType.ARGUMENT, segment.removeprefix(b'"').removesuffix(b'"'))
            )
            continue
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
