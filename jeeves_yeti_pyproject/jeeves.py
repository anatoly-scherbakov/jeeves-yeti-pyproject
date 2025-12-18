import itertools
import json
import logging
import re
from pathlib import Path
from typing import Annotated, Iterable

import rich
import sh
import typer
from jeeves_shell import Jeeves
from pydantic import TypeAdapter
from rich.console import Console
from rich.table import Table
from yarl import URL

from jeeves_yeti_pyproject.diff import (
    existing_files_only,
    list_changed_files,
    python_files_only,
)
from jeeves_yeti_pyproject.errors import BranchNameError
from jeeves_yeti_pyproject.files_and_directories import python_packages
from jeeves_yeti_pyproject.flags import (
    construct_flake8_args,
    construct_pytest_args,
)
from jeeves_yeti_pyproject.mypy import invoke_mypy
from jeeves_yeti_pyproject.notifications import (
    Notification,
    SubjectType,
    ViewPullRequest,
)

logger = logging.getLogger(__name__)

run = sh.poetry.run

jeeves = Jeeves(
    help="Manage a Python project.",
    no_args_is_help=True,
)

console = Console()

gh_json = sh.gh.bake(_tty_out=False)


@jeeves.command()
def lint():  # noqa: WPS213  # pragma: nocover
    """Lint code."""
    files_to_lint = python_files_only(
        existing_files_only(
            list_changed_files(),
        ),
    )
    if files_to_lint:
        try:
            run("ruff", "check", *files_to_lint)
        except sh.ErrorReturnCode_1 as err:
            typer.echo(err.stdout)
            typer.echo(err.stderr)
            raise typer.Exit(code=1) from err

        # Run flake8 with WPS rules for strict style checks
        try:
            run.flake8(
                *itertools.chain(construct_flake8_args()),
                *files_to_lint,
            )
        except sh.ErrorReturnCode_1 as err:
            typer.echo(err.stdout)
            typer.echo(err.stderr)
            raise typer.Exit(code=1) from err

    invoke_mypy(python_packages())

    sh.poetry.check()

    # We do not write anything to stdout here
    run.pip.check()


@jeeves.command()
def safety():  # pragma: nocover
    """Check installed Python packages for vulnerabilities."""
    run.safety.check(full_report=True)


@jeeves.command()
def test(
    paths: Annotated[
        list[Path] | None,
        typer.Argument(),
    ] = None,
):  # pragma: nocover
    """Unit test code."""
    is_granular = True
    if not paths:
        is_granular = False
        paths = [Path.cwd() / "tests"]

    try:
        run("pytest", *construct_pytest_args(is_granular=is_granular), *paths)
    except sh.ErrorReturnCode as err:
        typer.echo(err.stdout)
        typer.echo(err.stderr)

        coverage_path = Path.cwd() / "htmlcov/index.html"
        rich.print(f"See [link=file://{coverage_path}]coverage[/link].")

        raise typer.Exit(err.exit_code)


@jeeves.command()
def fmt():  # pragma: nocover
    """Auto format code."""
    files_to_format = python_files_only(
        existing_files_only(
            list_changed_files(),
        ),
    )
    if files_to_format:
        run.ruff.format(*files_to_format)


@jeeves.command()
def clear_poetry_cache():  # pragma: nocover
    """Clear Poetry cache."""
    sh.poetry.cache.clear("PyPI", "--all", "--no-interaction")


@jeeves.command()
def commit(  # noqa: WPS210  # pragma: nocover
    words: list[str],
    add: Annotated[
        bool,
        typer.Option(
            ...,
            "-a",
            help="Add all files when committing.",
        ),
    ] = False,
):
    """Commit staged files."""
    message = " ".join(words)

    branch = str(sh.git.branch("--show-current"))

    match = re.match(r"(?P<issue_id>\d+)-.+", branch)
    if match is None:
        raise BranchNameError(branch=branch)
    else:
        issue_id = match.groups()[0]

    prefix = f"#{issue_id} "

    message = typer.prompt(
        text=prefix,
        default=message or "",
        prompt_suffix="",
    )

    formatted_message = f"{prefix}{message}"
    typer.echo(formatted_message)

    git_commit = sh.git.commit

    if add:
        git_commit = git_commit.bake("-a")

    git_commit("-m", formatted_message)


def _notification_for_pull_request_still_relevant(  # pragma: nocover
    notification,
) -> bool:
    pull_request = notification.subject
    pull_request_id = int(URL(pull_request.url).name)

    repo_specification = notification.repository.full_name
    raw_pull_request_details = json.loads(
        gh_json.pr.view(
            pull_request_id,
            repo=repo_specification,
            json=",".join(["closed"]),
        ),
    )
    pull_request_details = TypeAdapter(ViewPullRequest).validate_python(
        raw_pull_request_details,
    )
    return not pull_request_details.closed


def _mark_notification_as_read(notification: Notification):  # pragma: nocover
    title = notification.subject.title
    console.print(
        f"Notification has been auto marked as read: [b]{title}[/b]",
        style="yellow",
    )
    gh_json.api(
        f"/notifications/threads/{notification.id}",
        "-F",
        "read=true",
        method="PATCH",
    )


def _exclude_merged_pull_requests(  # noqa: WPS210   # pragma: nocover
    notifications: list[Notification],
) -> Iterable[Notification]:
    for notification in notifications:
        if (
            notification.subject.type == SubjectType.pull_request
            and not _notification_for_pull_request_still_relevant(notification)
        ):
            _mark_notification_as_read(notification)

        elif notification.subject.type in {
            SubjectType.release,
            SubjectType.check_suite,
        }:
            _mark_notification_as_read(notification)

        else:
            yield notification


@jeeves.command()
def news():  # noqa: WPS210   # pragma: nocover
    """GitHub notifications."""  # noqa: D403
    raw_notifications = json.loads(gh_json.api("/notifications"))
    notifications = TypeAdapter(list[Notification]).validate_python(
        raw_notifications,
    )
    notifications = list(_exclude_merged_pull_requests(notifications))

    table = Table("Notification", "Repository")

    for notification in notifications:
        pull_request = notification.subject
        repository = notification.repository
        if pull_request.url:
            github_ui_url = URL(
                pull_request.url.replace("/repos", "").replace("pulls", "pull"),
            ).with_host("github.com")
        else:
            github_ui_url = None

        repository_url = URL(
            repository.url.replace("/repos", ""),
        ).with_host("github.com")

        table.add_row(
            f"[link={github_ui_url}]{pull_request.title}[/]",
            f"[link={repository_url}]{repository.full_name}[/]",
        )

    console.print(table)
