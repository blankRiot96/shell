from abc import ABC
from dataclasses import dataclass


BUILTIN_COMMAND_NAMES = (
    "echo"
)

class Token(ABC):
    pass

@dataclass
class BuiltinCommandToken(Token):
    command_name: str


@dataclass
class StringLiteralToken(Token):
    data: str


def create_tokens_from_code(code: str) -> list[Token]:
    tokens = []
    for segment in code.split():
        segment = segment.strip()
        if segment in BUILTIN_COMMAND_NAMES:
            tokens.append(BuiltinCommandToken(segment))
        elif segment.startswith('"'):
            data = segment.removeprefix('"').removesuffix('"')
            tokens.append(StringLiteralToken(data))

    return tokens
