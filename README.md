# recsys23

[![Python](https://img.shields.io/badge/python-3.7+-informational.svg)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=black)](https://pycqa.github.io/isort)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://mkdocstrings.github.io)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![mlflow](https://img.shields.io/badge/tracking-mlflow-blue)](https://mlflow.org)
[![dvc](https://img.shields.io/badge/data-dvc-9cf)](https://dvc.org)
[![Hydra](https://img.shields.io/badge/Config-Hydra-89b8cd)](https://hydra.cc)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


A short description of the project. No quotes.

## Prerequisites

You will need:

- `python` (see `pyproject.toml` for full version)
- `Make`
- a `.secrets` file with the required secrets and credentials
- load environment variables from `.env`

## Installation

Clone this repository

    git clone --recursive ssh://git@git.fraunhofer.pt/recsys23/recsys23.git
    cd recsys23 && git init

Install dependencies

    conda create -y -n recsys23 python=3.7
    conda activate recsys23

or if environment already exists

    conda env create -f environment.yml
    conda activate recsys23

Use pre-commit hooks to standardize code formatting of your project and save mental energy.
Simply install pre-commit package and pre-commit hooks with:

    make install-pre-commit

After that your code will be automatically reformatted on every new commit.

## Documentation

Full documentation is available here: [`docs/`](docs).

## Dev

See the [Developer](docs/DEVELOPER.md) guidelines for more information. 

## Contributing

Contributions of any kind are welcome. Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md]) for details and 
the process for submitting pull requests to us.

## Changelog

See the [Changelog](CHANGELOG.md) for more information.

## Security

Thank you for improving the security of the project, please see the [Security Policy](docs/SECURITY.md)
for more information.

## License

This project is licensed under the terms of the `No license` license. 
See [LICENSE](LICENSE) for more details.

## Citation

If you publish work that uses recsys23, please cite recsys23 as follows:

```bibtex
@misc{recsys23 recsys23,
  author = {Fraunhofer AICOS},
  title = {A short description of the project. No quotes.},
  year = {2023},
}
```
