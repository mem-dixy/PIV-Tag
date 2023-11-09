""""""

from celestine.typed import N
from celestine.window.container import View


def main(view: View) -> N:
    """"""
    language = view.hold.language
    with view.zone("main_head") as line:
        line.new("main_title", text=language.SCAN_MAIN_TITLE)
        line.new(
            "main_A",
            text=language.SCAN_MAIN_BUTTON,
            code="cow",
            say="Hello!",
        )
