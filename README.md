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
  * Run [`wemake-python-stylguide`](https://github.com/wemake-services/wemake-python-styleguide) against your code base;
  * Both of these are applied **only to those files which were changed against `origin/master`** (thanks [`flakeheaven`](https://github.com/flakeheaven/flakeheaven)!), making `j lint` legacy-friendly by default
* `fmt`
  * Add trailing commas automatically;
  * Apply [`isort`](https://github.com/pycqa/isort);
  * By design — no `black` here.
* `test`
  * Run `pytest` against `tests` directory with coverage enabled.

## Opinions

This plugin is very opinionated and reflects my own preferences of how I like my Python projects to be managed. Feel free to create your own plugins. [Mr Jeeves](https://github.com/jeeves-sh/jeeves-shell) is happy to make your life a little bit easier.
