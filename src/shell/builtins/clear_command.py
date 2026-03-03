from shell.builtins.objects import RawText


def eval_clear() -> RawText:
    return RawText("\033[2J\033[H")
