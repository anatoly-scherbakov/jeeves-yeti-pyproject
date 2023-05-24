from jeeves_yeti_pyproject.flags import (
    construct_isort_args,
    construct_pytest_args,
)
from jeeves_yeti_pyproject.mypy import construct_mypy_flags


def test_isort():
    assert list(construct_isort_args())


def test_pytest():
    assert list(construct_pytest_args())


def test_mypy():
    assert list(construct_mypy_flags())
