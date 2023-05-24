from pathlib import Path

from jeeves_yeti_pyproject.flakeheaven.integration import construct_config


def test_construct_config():
    assert construct_config(Path.cwd())
