""""""

from celestine.data import VERSION_NUMBER
from celestine.session.data import (
    ACTION,
    CHOICES,
    HELP,
    NARGS,
    VERSION,
)
from celestine.typed import (
    AT,
    LS,
    N,
    R,
    S,
)


class Attribute:
    """"""

    def dictionary(self) -> AT:
        """"""
        return {}

    def __init__(self, **star: R) -> N:
        """"""
        super().__init__(**star)


class Action(Attribute):
    """"""

    def dictionary(self) -> AT:
        """"""
        return super().dictionary() | {ACTION: self.action}

    def __init__(self, *, action: S, **star: R) -> N:
        """"""
        self.action = action
        super().__init__(**star)


class Choices(Attribute):
    """"""

    def dictionary(self) -> AT:
        """"""
        return super().dictionary() | {CHOICES: self.choices}

    def __init__(self, *, choices: LS, **star: R) -> N:
        """"""
        self.choices = choices
        super().__init__(**star)


class Help(Attribute):
    """"""

    def dictionary(self) -> AT:
        """"""
        return super().dictionary() | {HELP: self.help}

    # pylint: disable-next=redefined-builtin
    def __init__(self, *, help: S, **star: R) -> N:
        """"""
        self.help = help
        super().__init__(**star)


class Nargs(Attribute):
    """"""

    def dictionary(self) -> AT:
        """"""
        return super().dictionary() | {NARGS: self.nargs}

    def __init__(self, *, nargs: S, **star: R) -> N:
        """"""
        self.nargs = nargs
        super().__init__(**star)


class Version(Attribute):
    """"""

    def dictionary(self) -> AT:
        """"""
        return super().dictionary() | {VERSION: VERSION_NUMBER}
