from pathlib import Path
from typing import Iterable, Tuple, Union

from jeeves_yeti_pyproject.files_and_directories import python_packages

CLIValue = Union[str, int, Path]
CLIParameter = Union[str, Tuple[str, CLIValue]]


LINE_LENGTH = 80


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


def construct_pytest_args() -> Iterable[str]:   # noqa: WPS213
    """
    Args for pytest.

    # FIXME:
    #   title: Replace `construct_pytest_args` with an overridable config
    #   description: Arguments for pytest are hardcoded. A few of them are
    #   generated and will stay that way, but at least partially we should be
    #   able to override the arguments.
    """
    yield '--strict-markers'
    yield '--strict-config'
    yield '--tb=short'
    yield '--doctest-modules'
    yield '--cov={}'.format(
        ','.join(
            map(str, python_packages()),
        ),
    )
    yield '--cov-report=term:skip-covered'
    yield '--cov-report=html'
    yield '--cov-report=xml'
    yield '--cov-branch'
    yield '--cov-fail-under=100'


def construct_isort_args() -> Iterable[CLIParameter]:
    """
    Isort configuration.

    https://github.com/timothycrosley/isort/wiki/isort-Settings
    See https://github.com/timothycrosley/isort#multi-line-output-modes

    Source: wemake-python-styleguide.
    """
    yield '--trailing-comma'
    yield '--use-parentheses'
    yield '--multi-line', 'VERTICAL_HANGING_INDENT'
    yield '--line-length', LINE_LENGTH
