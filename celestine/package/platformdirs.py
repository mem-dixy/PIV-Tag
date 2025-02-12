"""A package for determining appropriate platform-specific dirs."""

from celestine.data import (
    wrap,
    wrapper,
)
from celestine.package import Abstract
from celestine.typed import (
    R,
    S,
)


class Package(Abstract):
    """"""


@wrapper(__name__)
def user_data_dir(**star: R) -> S:
    """"""
    result = wrap(
        appname="celestine",
        appauthor=False,
        version=None,
        roaming=False,
        ensure_exists=True,
        **star,
    )
    return result
