from pathlib import Path
from typing import List

from sh.contrib import git


def list_changed_files() -> List[str]:
    """Files changed against origin/master."""
    return list(
        filter(
            bool,
            git.diff(
                '--name-only',
                'origin/master',
            ).split('\n'),
        ),
    )


def existing_files_only(
    paths: List[str],
) -> List[str]:   # pragma: nocover
    """Files that are in diff and exist."""
    return [
        path
        for path in paths
        if (Path.cwd() / path).exists()
    ]


def python_files_only(paths: list[str]) -> list[str]:
    """Only .py files."""
    return [path for path in paths if path.endswith('.py')]
