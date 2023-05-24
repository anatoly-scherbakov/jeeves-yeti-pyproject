import logging
import tempfile
from pathlib import Path

import tomlkit
import typer
from sh import ErrorReturnCode_1, poetry
from sh.contrib import git

logger = logging.getLogger('jeeves-yeti-pyproject:flakeheaven')


def construct_config(project_directory: Path):
    """Construct transient TOML config for Flakeheaven."""
    return {
        'tool': {
            'flakeheaven': {
                'base': [
                    str(Path(__file__).parent / 'flakeheaven.toml'),
                    str(project_directory / 'pyproject.toml'),
                ],
            },
        },
    }


def call(project_directory: Path):  # pragma: nocover
    """Execute flakeheaven against the project."""
    with tempfile.TemporaryDirectory() as directory:
        config = Path(directory) / 'flakeheaven.toml'

        config.write_text(
            config_content := tomlkit.dumps(
                construct_config(project_directory),
            ),
        )

        logger.debug('Transient config for flakeheaven: %s', config_content)

        try:
            poetry.run.flakeheaven.lint(
                '--diff',
                '--config',
                config,
                '.',
                _cwd=project_directory,
                _in=git.diff('origin/master'),
            )
        except ErrorReturnCode_1 as err:
            typer.echo(err.stdout)
            raise typer.Exit(code=1) from err
