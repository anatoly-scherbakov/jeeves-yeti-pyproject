from typing import Iterable

import rich
import typer
from sh import ErrorReturnCode_1, poetry

run = poetry.run


def invoke_mypy(directories) -> None:  # pragma: nocover
    """Call mypy and filter its output against git diff."""
    try:
        run.mypy(
            *directories,
            *construct_mypy_flags(),
        )
    except ErrorReturnCode_1 as err:
        rich.print(err.stdout.decode())
        raise typer.Exit(1)


def construct_mypy_flags() -> Iterable[str]:   # noqa: WPS213
    """
    Mypy configuration.

    - http://bit.ly/2zEl9WI
    - Source: wemake-python-package.

    # FIXME: Change to an overridable config file.
    """
    yield '--disallow-redefinition'
    yield '--check-untyped-defs'   # noqa: WPS354
    yield '--disallow-any-explicit'
    yield '--disallow-any-generics'
    yield '--disallow-untyped-calls'
    yield '--ignore-missing-imports'
    yield '--implicit-reexport'
    yield '--local-partial-types'
    yield '--strict-optional'
    yield '--strict-equality'
    yield '--no-implicit-optional'
    yield '--warn-no-return'
    yield '--warn-unused-ignores'
    yield '--warn-redundant-casts'
    yield '--warn-unused-configs'
    yield '--warn-unreachable'
