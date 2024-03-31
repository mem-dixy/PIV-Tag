""""""


import pathlib

from celestine import (
    bank,
    load,
)
from celestine.data.directory import (
    APPLICATION,
    INTERFACE,
    LANGUAGE,
)
from celestine.package import Package
from celestine.typed import (
    LS,
    B,
    C,
    D,
    N,
    R,
    S,
)

from .magic import Magic


def begin_session(argument_list: LS, exit_on_error: B, **star: R) -> N:
    """

    First load Language so human can read errors.
    Then load Interface so human see errors the way they want.
    """

    magic = Magic(argument_list, exit_on_error)

    with magic:
        magic.parse(LANGUAGE)
        magic.parse(INTERFACE)
        magic.parse(APPLICATION)

        method = load.method("Whale", "session", "session")
        magic.get_parser([method], True)
        path = method.whale  # configuration file: avoid name conflict
        magic.configuration.load(path)

        magic.parse(LANGUAGE)
        magic.parse(INTERFACE)
        magic.parse(APPLICATION)

        session1 = load.method("Session", "session", "session")
        session2 = load.method(
            "Session", APPLICATION, magic.core.application.name
        )
        session3 = load.method("Information", "session", "session")

        magic.get_parser([session1, session2, session3], False)

    # Save values to session object.
    application = magic.core.application.name

    # items = load.python(APPLICATION, application)
    # car = list(items)

    code: D[S, C] = {}
    main: D[S, C] = {}
    view: D[S, C] = {}

    modules = load.modules(APPLICATION, application)
    for module in modules:
        code |= load.decorators(module, "code")
        main |= load.decorators(module, "main")
        view |= load.decorators(module, "scene")

    if not main:
        raise LookupError("No '@main' decorator found.")

    if len(main) > 1:
        raise UserWarning("Expecting only one '@main' decorator.")

    bank.application = load.module(APPLICATION, session1.application)
    bank.attribute = session2
    bank.code = code
    bank.configuration = pathlib.Path()  # unset
    bank.directory = pathlib.Path()  # unset
    bank.interface = load.module(INTERFACE, session1.interface)
    bank.language = load.module(LANGUAGE, session1.language)
    bank.main = next(iter(main))
    bank.package = Package()
    bank.view = view | main
    bank.window = bank.interface.Window(**star)
