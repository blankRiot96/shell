from shell.parser.tokenize import (
    create_tokens_from_code,
    BuiltinCommandToken,
    StringLiteralToken,
)
import pytest


def test_builtin_command():
    assert create_tokens_from_code('echo "hii"') == [
        BuiltinCommandToken("echo"),
        StringLiteralToken("hii"),
    ]
