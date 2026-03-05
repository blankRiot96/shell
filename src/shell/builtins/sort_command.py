from shell.builtins.objects import Column, Table
from shell.parser.ast import ArgumentNode, ColumnNode


def _swap_table_col_entries(table: Table, index_a: int, index_b: int):
    for col in table.columns:
        col.objects[index_a], col.objects[index_b] = (
            col.objects[index_b],
            col.objects[index_a],
        )


def _bubble_sort_in_place(comparison_col: Column, table: Table, descending: bool):
    swapped = False

    for i in range(len(comparison_col.objects) - 1):
        a_col = comparison_col.objects[i]
        b_col = comparison_col.objects[i + 1]

        if descending and a_col < b_col:
            _swap_table_col_entries(table, i, i + 1)
            swapped = True
        elif not descending and a_col > b_col:
            _swap_table_col_entries(table, i, i + 1)
            swapped = True

    if swapped:
        _bubble_sort_in_place(comparison_col, table, descending)


def eval_sort[T: Table | Column](input_struct: T, arguments: list[ArgumentNode]) -> T:
    sort_by_column_names: list[str] = []
    descending = False
    for arg in arguments:
        if isinstance(arg, ColumnNode):
            sort_by_column_names.append(arg.column_name)
        else:
            if arg.argument_literal == "desc":
                descending = True

    assert len(sort_by_column_names) == 1
    selected_col_name = sort_by_column_names[0]

    if isinstance(input_struct, Column):
        if input_struct.name != selected_col_name:
            raise ValueError(
                f"Column `{selected_col_name}` does not match input Column `{input_struct.name}`"
            )
        # TODO: do something about `SupportsRichComparison` here...
        input_struct.objects.sort(key=lambda x: x, reverse=descending)
        return input_struct

    selected_col = None
    for col in input_struct.columns:
        if col.name == selected_col_name:
            selected_col = col

    if selected_col is None:
        raise ValueError(f"Column `{selected_col}` does not exist in input Table")

    # bubble sort... god ill need to optimize so many things later
    # TODO: use something more optimal...
    _bubble_sort_in_place(selected_col, input_struct, descending)
    return input_struct
