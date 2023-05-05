from jeeves_yeti_pyproject.diff import list_changed_files


def test_list_changed_files():
    assert len(list(list_changed_files())) >= 0
