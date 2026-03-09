from shell.builtins.objects import AssignmentResult, RawText
from shell.eval.line import evaluate_line


def test_string_assignment():
    assert evaluate_line('let x = "meow"') == AssignmentResult("x", RawText("meow"))
