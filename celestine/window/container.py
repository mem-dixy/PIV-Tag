""""""

import enum


class Call(enum.Enum):
    """"""

    NONE = enum.auto()
    VIEW = enum.auto()
    WORK = enum.auto()


class Zone(enum.Enum):
    """"""

    DROP = enum.auto()
    GRID = enum.auto()
    NONE = enum.auto()
    SPAN = enum.auto()


class Image(enum.Enum):
    """"""

    FILL = enum.auto()
    FULL = enum.auto()
