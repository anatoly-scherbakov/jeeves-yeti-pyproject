from pathlib import Path
from typing import Iterable, Tuple, Union

from jeeves_yeti_pyproject.files_and_directories import python_packages

CLIValue = Union[str, int, Path]
CLIParameter = Union[str, int, Tuple[str, CLIValue]]


LINE_LENGTH = 80


def construct_pytest_args(is_granular: bool) -> Iterable[str]:   # noqa: WPS213
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

    if is_granular:
        yield '-vv'

    else:
        # We only measure coverage if the whole test suite is being executed.
        yield '--cov={}'.format(
            ','.join(
                str(python_package)
                for python_package in python_packages()
                if python_package.name != 'tests'
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

    yield '--multi-line'
    yield 'VERTICAL_HANGING_INDENT'

    yield '--line-length'
    yield LINE_LENGTH
