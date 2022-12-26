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
