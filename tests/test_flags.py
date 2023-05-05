from jeeves_yeti_pyproject.flags import construct_isort_args


def test_isort():
    assert list(construct_isort_args())
