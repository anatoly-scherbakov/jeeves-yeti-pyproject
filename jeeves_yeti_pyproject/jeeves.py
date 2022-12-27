import itertools
from pathlib import Path

import typer
from jeeves_shell import Jeeves
from sh import ErrorReturnCode_1, add_trailing_comma, isort, poetry

from jeeves_yeti_pyproject import flakeheaven
from jeeves_yeti_pyproject.diff import (
    changed_and_existing_files,
    list_changed_files,
)
from jeeves_yeti_pyproject.files_and_directories import python_directories
from jeeves_yeti_pyproject.flags import (
    construct_isort_args,
    construct_pytest_args,
)
from jeeves_yeti_pyproject.mypy import invoke_mypy

run = poetry.run

jeeves = Jeeves(
    help='Manage a Python project.',
    no_args_is_help=True,
)


@jeeves.command()
def lint():
    """Lint code."""
    directories = python_directories()

    invoke_mypy(directories)

    flakeheaven.call(
        project_directory=Path.cwd(),
    )

    poetry.check()

    # We do not write anything to stdout here
    run.pip.check()


@jeeves.command()
def safety():
    """Check installed Python packages for vulnerabilities."""
    run.safety.check(full_report=True)


@jeeves.command()
def test():
    """Unit test code."""
    try:
        run('pytest', *construct_pytest_args(), 'tests')
    except ErrorReturnCode_1 as err:
        typer.echo(err.stdout)


@jeeves.command()
def fmt():
    """Auto format code."""
    isort(
        *itertools.chain(construct_isort_args()),
        '.',
    )

    files_to_format = changed_and_existing_files(
        list_changed_files(),
    )
    add_trailing_comma(
        '--py36-plus',
        *files_to_format,
    )
