import pytest

from shell.parser.tokenize import Token, TokenType, create_tokens_from_code
from shell.parser.tokenize import string_to_bytearray as stb


def test_builtin_command():
    assert create_tokens_from_code('echo "hii"') == [
        Token(TokenType.BUILTIN_COMMAND, stb("echo")),
        Token(TokenType.STRING_LITERAL, stb('"hii"')),
        Token(TokenType.EOF, bytearray()),
    ]


def test_queue_mechanism():
    assert create_tokens_from_code("ls|select .date|sort desc") == [
        Token(TokenType.BUILTIN_COMMAND, stb("ls")),
        Token(TokenType.PIPE, stb("|")),
        Token(TokenType.BUILTIN_COMMAND, stb("select")),
        Token(TokenType.COLUMN_NAME, stb(".date")),
        Token(TokenType.PIPE, stb("|")),
        Token(TokenType.BUILTIN_COMMAND, stb("sort")),
        Token(TokenType.ARGUMENT, stb("desc")),
        Token(TokenType.EOF, bytearray()),
    ]


def test_whitespace():
    assert create_tokens_from_code("ls | select .date | sort desc") == [
        Token(TokenType.BUILTIN_COMMAND, stb("ls")),
        Token(TokenType.PIPE, stb("|")),
        Token(TokenType.BUILTIN_COMMAND, stb("select")),
        Token(TokenType.COLUMN_NAME, stb(".date")),
        Token(TokenType.PIPE, stb("|")),
        Token(TokenType.BUILTIN_COMMAND, stb("sort")),
        Token(TokenType.ARGUMENT, stb("desc")),
        Token(TokenType.EOF, bytearray()),
    ]
