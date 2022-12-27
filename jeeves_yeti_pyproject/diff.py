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
            ).stdout.decode().split('\n'),
        ),
    )


def changed_and_existing_files(paths: List[str]) -> List[str]:
    """Files that are in diff and exist."""
    return [
        path
        for path in paths
        if (Path.cwd() / path).exists()
    ]
