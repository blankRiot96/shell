from shell.builtins.max_command import eval_max
from shell.builtins.objects import Column, FileSize, RawText, Table
from shell.parser.ast import ColumnNode


def test_column():
    target = FileSize(15)
    assert eval_max(Column("size", [FileSize(10), target, FileSize(5)]), []) == target


def test_table():
    input_struct = Table(
        [
            Column(
                "name",
                [RawText("meow"), RawText("nya"), RawText("purr"), RawText("grr")],
            ),
            Column(
                "size", [FileSize(100), FileSize(300), FileSize(150), FileSize(200)]
            ),
        ]
    )
    expected_output = Table(
        [Column("name", [RawText("nya")]), Column("size", [FileSize(300)])]
    )

    assert eval_max(input_struct, [ColumnNode(".size")]) == expected_output
