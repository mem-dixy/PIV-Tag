"""
Pylint can't seem to find curses and so gives a bnuch of errors.

Putting alias here to contain errors to this file only.

Hidding everything in the __getattribute__ function.
"""

# https://dearpygui.readthedocs.io/en/latest/
import curses

import _curses

from celestine.typed import A
from celestine.unicode import (
    ESCAPE,
    SPACE,
)

from . import AbstractPackage


class Package(AbstractPackage):
    """"""

    def window(self, column, row, width, height):
        """"""
        nlines = height
        ncols = width
        begin_y = row
        begin_x = column
        return package.newwin(nlines, ncols, begin_y, begin_x)

    def subwindow(self, window, column, row, width, height):
        """"""
        nlines = height
        ncols = width
        begin_y = row
        begin_x = column
        return window.subwin(nlines, ncols, begin_y, begin_x)

    def __getattribute__(self, name) -> A:
        """"""
        one = [
            "noecho",
            "initscr",
            "cbreak",
            "start_color",
            "echo",
            "nocbreak",
            "endwin",
            "newwin",
            "COLORS",
            "COLOR_PAIRS",
            "color_pair",
            "init_color",
            "init_pair",
        ]
        two = [
            "doupdate",
            "KEY_UP",
            "KEY_DOWN",
            "KEY_LEFT",
            "KEY_RIGHT",
        ]

        if name in one:
            return getattr(_curses, name)
        if name in two:
            return getattr(curses, name)

        match name:
            case "KEY_EXIT":
                return ord(ESCAPE)
            case "KEY_CLICK":
                return ord(SPACE)
            case "space":
                return 32
            case "quit":
                return 113
            case "down":
                return 258
            case "up":
                return 259
            case "left":
                return 260
            case "right":
                return 261

            case "window":
                return object.__getattribute__(self, name)
            case "subwindow":
                return object.__getattribute__(self, name)
            case "doupdate":
                return object.__getattribute__(self, name)


package = Package()
