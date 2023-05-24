from pathlib import Path
from typing import List


def directories_with_a_file_in_them(
    pattern: str,
) -> List[Path]:
    """All subdirectories which have a file in them conforming to a pattern."""
    return [   # pragma: nocover
        sub_directory
        for sub_directory in Path.cwd().iterdir()
        if sub_directory.is_dir() and list(sub_directory.glob(pattern))
    ]


def python_directories() -> List[Path]:  # pragma: nocover
    """All subdirectories of the current directory with Python files."""
    return directories_with_a_file_in_them('*.py')


def python_packages() -> List[Path]:  # pragma: nocover
    """All Python packages in current directory."""
    return directories_with_a_file_in_them('__init__.py')
