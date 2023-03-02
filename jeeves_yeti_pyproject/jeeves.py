import itertools
from pathlib import Path
from typing import List, Optional

import typer
from jeeves_shell import Jeeves
from sh import ErrorReturnCode, add_trailing_comma, isort, poetry

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
def test(
    paths: Optional[List[Path]] = typer.Argument(None),   # noqa: B008, WPS404
):
    """Unit test code."""
    if paths is None:
        paths = [Path.cwd() / 'tests']

    try:
        run('pytest', *construct_pytest_args(), *paths)
    except ErrorReturnCode as err:
        typer.echo(err.stdout)
        typer.echo(err.stderr)
        raise typer.Exit(err.exit_code)


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


@jeeves.command()
def clear_poetry_cache():
    """Clear Poetry cache."""
    poetry('cache', 'clear', 'PyPI', '--all', '--no-interaction')
