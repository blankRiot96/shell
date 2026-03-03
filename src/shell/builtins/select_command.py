from shell.builtins.objects import Column, Table
from shell.parser.ast import ArgumentNode, ColumnNode


def eval_select(input_table: Table, arguments: list[ArgumentNode]) -> Table | Column:
    if len(arguments) == 1:
        assert isinstance(arguments[0], ColumnNode)
        for col in input_table.columns:
            if col.name == arguments[0].column_name:
                return col
    elif len(arguments) == 0:
        raise ValueError("Need to select at least one column")

    result_columns: list[Column] = []
    for col in input_table.columns:
        for arg in arguments:
            if isinstance(arg, ColumnNode):
                if arg.column_name == col.name:
                    result_columns.append(col)

    return Table(result_columns)
