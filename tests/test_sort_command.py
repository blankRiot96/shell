from shell.builtins.objects import Column, FileSize, RawText, Table
from shell.builtins.sort_command import eval_sort
from shell.parser.ast import ArgumentNode, ColumnNode


def test_ascending_sort():
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
        [
            Column(
                "name",
                [RawText("meow"), RawText("purr"), RawText("grr"), RawText("nya")],
            ),
            Column(
                "size", [FileSize(100), FileSize(150), FileSize(200), FileSize(300)]
            ),
        ]
    )

    assert eval_sort(input_struct, [ColumnNode(".size")]) == expected_output


def test_descending_sort():
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
        [
            Column(
                "name",
                [RawText("meow"), RawText("purr"), RawText("grr"), RawText("nya")],
            ),
            Column(
                "size",
                [FileSize(100), FileSize(150), FileSize(200), FileSize(300)],
            ),
        ]
    )
    expected_output.columns[0].objects.reverse()
    expected_output.columns[1].objects.reverse()

    assert (
        eval_sort(input_struct, [ColumnNode(".size"), ArgumentNode("desc")])
        == expected_output
    )
