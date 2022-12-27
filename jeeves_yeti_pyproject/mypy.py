from typing import Iterable

import more_itertools
import typer
from sh import ErrorReturnCode_1, poetry

from jeeves_yeti_pyproject.diff import list_changed_files

run = poetry.run


def invoke_mypy(directories) -> None:
    """Call mypy and filter its output against git diff."""
    try:
        run.mypy(
            *directories,
            *construct_mypy_flags(),
        )
    except ErrorReturnCode_1 as err:
        changed_files = set(list_changed_files())

        mypy_lines = [
            line for line in err.stdout.decode().split('\n')
            if more_itertools.first(line.split(':', 1)) in changed_files
        ]

        if mypy_lines:
            for line in mypy_lines:
                typer.echo(line)

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
