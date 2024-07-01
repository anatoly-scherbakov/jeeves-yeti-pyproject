import itertools
import re
from pathlib import Path
from typing import List, Optional, Annotated

import rich
import typer
from jeeves_shell import Jeeves
from sh import ErrorReturnCode, add_trailing_comma, git, isort, poetry

from jeeves_yeti_pyproject import flakeheaven
from jeeves_yeti_pyproject.diff import (
    existing_files_only,
    list_changed_files, python_files_only,
)
from jeeves_yeti_pyproject.errors import BranchNameError
from jeeves_yeti_pyproject.files_and_directories import (
    python_directories,
    python_packages,
)
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
def lint():  # pragma: nocover
    """Lint code."""
    directories = python_packages()

    invoke_mypy(directories)

    flakeheaven.call(
        project_directory=Path.cwd(),
    )

    poetry.check()

    # We do not write anything to stdout here
    run.pip.check()


@jeeves.command()
def safety():  # pragma: nocover
    """Check installed Python packages for vulnerabilities."""
    run.safety.check(full_report=True)


@jeeves.command()
def test(
    paths: Annotated[
        Optional[List[Path]],
        typer.Argument(),
    ] = None,
):  # pragma: nocover
    """Unit test code."""
    is_granular = True
    if not paths:
        is_granular = False
        paths = [Path.cwd() / 'tests']

    try:
        run('pytest', *construct_pytest_args(is_granular=is_granular), *paths)
    except ErrorReturnCode as err:
        typer.echo(err.stdout)
        typer.echo(err.stderr)

        coverage_path = Path.cwd() / 'htmlcov/index.html'
        rich.print(f'See [link=file://{coverage_path}]coverage[/link].')

        raise typer.Exit(err.exit_code)


@jeeves.command()
def fmt():   # pragma: nocover
    """Auto format code."""
    isort(
        *itertools.chain(construct_isort_args()),
        '.',
    )

    files_to_format = python_files_only(
        existing_files_only(
            list_changed_files(),
        ),
    )
    add_trailing_comma(
        '--py36-plus',
        *files_to_format,
    )


@jeeves.command()
def clear_poetry_cache():  # pragma: nocover
    """Clear Poetry cache."""
    poetry.cache.clear('PyPI', '--all', '--no-interaction')


@jeeves.command()
def commit(message: str):   # noqa: WPS210  # pragma: nocover
    """Create a commit."""
    branch = str(git.branch('--show-current'))

    match = re.match(r'issue-(?P<issue_id>\d+)-.+', branch)
    if match is None:
        raise BranchNameError(branch=branch)
    else:
        issue_id = match.groups()[0]

    prefix = f'#{issue_id} '

    message = typer.prompt(
        text=prefix,
        default=message or '',
        prompt_suffix='',
    )

    formatted_message = f'{prefix}{message}'
    typer.echo(formatted_message)
    git.commit('-a', '-m', formatted_message)
