# ADR: Flake8 pyproject.toml Configuration Support

## Status
Rejected

## Context
Flake8 does not natively support configuration via `pyproject.toml`. It reads from `.flake8`, `setup.cfg`, or `tox.ini`. To align with modern Python tooling and consolidate configuration, we evaluated solutions to enable `pyproject.toml` support.

## Decision
Use `setup.cfg` for flake8 configuration as recommended by [wemake-python-styleguide](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/configuration.html).

## Options

| Library | Type | Command | Configuration Section | Notes |
|---------|------|---------|----------------------|-------|
| [Flake8-pyproject](https://pypi.org/project/Flake8-pyproject/) | Plugin | `flake8` | `[tool.flake8]` | Requires plugin in all environments |
| [pyproject-flake8](https://pypi.org/project/pyproject-flake8/) | Wrapper | `pflake8` | `[tool.flake8]` | Requires command change |
| [flake8-pyprojecttoml](https://pypi.org/project/flake8-pyprojecttoml/) | Extension | `flake8` | `[tool.flake8]` | Monkey-patches flake8 config |
| `setup.cfg` | Native | `flake8` | `[flake8]` | Works everywhere without plugins |

## Consequences
- `setup.cfg` works with all flake8 installations (system, poetry, etc.)
- No additional dependencies required
- Standard approach recommended by wemake-python-styleguide
- Format: `ignore = DAR` in `[flake8]` section
