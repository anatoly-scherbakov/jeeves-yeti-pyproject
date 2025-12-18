# jeeves-yeti-pyproject

This is my personal plugin for [`jeeves-shell`](https://github.com/jeeves-sh/jeeves-shell) that I use for my open source Python projects. If you wish to use it for your projects too, it can be added as easily as:

```shell
poetry add --group dev jeeves-yeti-pyproject
```

and then just run:

```shell
j
```

## Commands

```
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────╮
│ clear-poetry-cache       Clear Poetry cache.                                               │
│ fmt                      Auto format code.                                                 │
│ lint                     Lint code.                                                        │
│ safety                   Check installed Python packages for vulnerabilities.              │
│ test                     Unit test code.                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Features

* `lint`
  * Check Python typing with [`mypy`](https://mypy-lang.org),
  * Run [`ruff`](https://docs.astral.sh/ruff/) for fast linting,
  * Run [`wemake-python-stylguide`](https://github.com/wemake-services/wemake-python-styleguide) via flake8 against your code base;
  * All of these are applied **only to those files which were changed against `origin/master`**, making `j lint` legacy-friendly by default
* `fmt`
  * Format code using [`ruff format`](https://docs.astral.sh/ruff/formatter/);
  * Applied **only to those files which were changed against `origin/master`**, making `j fmt` legacy-friendly by default.
* `test`
  * Run `pytest` against `tests` directory with coverage enabled.

## Opinions

This plugin is very opinionated and reflects my own preferences of how I like my Python projects to be managed. Feel free to create your own plugins. [Mr Jeeves](https://github.com/jeeves-sh/jeeves-shell) is happy to make your life a little bit easier.
