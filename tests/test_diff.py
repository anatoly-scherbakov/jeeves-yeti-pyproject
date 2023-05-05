import more_itertools

from jeeves_yeti_pyproject.diff import list_changed_files


def test_list_changed_files():
    """Git returns changed files list and does not crash."""
    more_itertools.consume(list_changed_files())
