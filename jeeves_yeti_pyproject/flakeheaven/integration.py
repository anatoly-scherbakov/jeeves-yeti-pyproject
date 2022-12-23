import logging
import tempfile
from pathlib import Path

import sh
import tomlkit
import typer
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


def call(project_directory: Path):
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
            sh.poetry.run.flakeheaven.lint(
                git.diff('origin/master'),
                '--diff',
                '--config',
                config,
                '.',
                _cwd=project_directory,
            )
        except sh.ErrorReturnCode_1 as err:
            typer.echo(err.stdout)
            raise typer.Exit(code=1) from err
