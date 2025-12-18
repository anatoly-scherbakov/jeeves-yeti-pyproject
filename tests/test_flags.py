from jeeves_yeti_pyproject.flags import (
    construct_pytest_args,
)
from jeeves_yeti_pyproject.mypy import construct_mypy_flags


def test_pytest():
    assert list(construct_pytest_args(is_granular=True))
    assert list(construct_pytest_args(is_granular=False))


def test_mypy():
    assert list(construct_mypy_flags())
