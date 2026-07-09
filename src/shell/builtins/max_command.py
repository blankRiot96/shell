from shell.builtins.objects import Column, ShellObject, Table
from shell.parser.ast import ArgumentNode, ColumnNode


def eval_max(input_struct: Column | Table, args: list[ArgumentNode]) -> ShellObject:
    if isinstance(input_struct, Column):
        selected_col = input_struct
    else:
        assert len(args) == 1
        assert isinstance(args[0], ColumnNode)
        target_col = args[0].column_name

        selected_col = None
        for col in input_struct.columns:
            if col.name == target_col:
                selected_col = col

        if selected_col is None:
            raise ValueError(
                f"Selected column `{target_col}` does not exist in input table"
            )

    max_index = None
    greatest = selected_col.objects[0]
    for i, obj in enumerate(selected_col.objects):
        if obj > greatest:
            greatest = obj
            max_index = i

    assert max_index is not None
    if isinstance(input_struct, Column):
        return greatest

    result_columns = []
    for col in input_struct.columns:
        result_columns.append(Column(col.name, [col.objects[max_index]]))

    return Table(result_columns)
