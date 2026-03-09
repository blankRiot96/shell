from shell.parser.tokenize import Token, TokenType, create_tokens_from_code
from shell.parser.tokenize import string_to_bytearray as stb


def test_builtin_command():
    assert create_tokens_from_code('echo "hii"') == [
        Token(TokenType.BUILTIN_COMMAND, stb("echo")),
        Token(TokenType.ARGUMENT, stb("hii")),
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


def test_false_alarm():
    """
    Tests if in `ls sort`, `sort` should be seen as an argument token
     and not as a builtin command token
    """

    assert create_tokens_from_code("ls sort") == [
        Token(TokenType.BUILTIN_COMMAND, stb("ls")),
        Token(TokenType.ARGUMENT, stb("sort")),
        Token(TokenType.EOF, bytearray()),
    ]


def test_assignment():
    assert create_tokens_from_code('let x = "meow"') == [
        Token(TokenType.KEYWORD, stb("let")),
        Token(TokenType.IDENTIFIER, stb("x")),
        Token(TokenType.ASSIGNMENT_EQUALS, stb("=")),
        Token(TokenType.STRING_LITERAL, stb('"meow"')),
        Token(TokenType.EOF, bytearray()),
    ]
    assert create_tokens_from_code("let result = ls | select .date | sort desc") == [
        Token(TokenType.KEYWORD, stb("let")),
        Token(TokenType.IDENTIFIER, stb("result")),
        Token(TokenType.ASSIGNMENT_EQUALS, stb("=")),
        Token(TokenType.BUILTIN_COMMAND, stb("ls")),
        Token(TokenType.PIPE, stb("|")),
        Token(TokenType.BUILTIN_COMMAND, stb("select")),
        Token(TokenType.COLUMN_NAME, stb(".date")),
        Token(TokenType.PIPE, stb("|")),
        Token(TokenType.BUILTIN_COMMAND, stb("sort")),
        Token(TokenType.ARGUMENT, stb("desc")),
        Token(TokenType.EOF, bytearray()),
    ]


def test_assignment_spaceless():
    assert create_tokens_from_code('let x="meow"') == [
        Token(TokenType.KEYWORD, stb("let")),
        Token(TokenType.IDENTIFIER, stb("x")),
        Token(TokenType.ASSIGNMENT_EQUALS, stb("=")),
        Token(TokenType.STRING_LITERAL, stb('"meow"')),
        Token(TokenType.EOF, bytearray()),
    ]


def test_variable_invocation():
    assert create_tokens_from_code("echo $result") == [
        Token(TokenType.BUILTIN_COMMAND, stb("echo")),
        Token(TokenType.VARIABLE, stb("$result")),
        Token(TokenType.EOF, bytearray()),
    ]
