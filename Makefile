#################################################################################
# GLOBALS                                                                       #
#################################################################################
include Makefile.include
#################################################################################
# Environment                                                                   #
#################################################################################
include Makefile.envs


ifeq (,$(CONDA_EXE))
HAS_CONDA=False
else
HAS_CONDA=True
endif

.PHONY: build-env build-env-note build-env-dev build-env-docs update-requirements update-requirements-dev
## Build virtualenv for project
build-env:
	@python3 -m venv .venv && \
	source .venv/bin/activate && \
	python3 -m pip install --upgrade pip setuptools && \
	pip3 install -r requirements/requirements.txt

## Build virtualenv for development with jupyter notebook support
build-env-note:
	@python3 -m venv .venv-note && \
	source .venv-note/bin/activate && \
	python3 -m pip install --upgrade pip && \
	python3 -m pip install -r requirements/requirements.txt && \
	python3 -m pip install -r requirements/requirements-notebook.txt

## Build virtualenv for development
build-env-dev:
	@python3 -m venv .venv-dev && \
	source .venv-dev/bin/activate && \
	python3 -m pip install --upgrade pip setuptools && \
	python3 -m pip install -r requirements/requirements.txt && \
	python3 -m pip install -r requirements/requirements-dev.txt

## Build virtualenv for documentation
build-env-docs:
	@python3 -m venv .venv-docs && \
	source .venv-docs/bin/activate && \
	python3 -m pip install --upgrade pip&& \
	python3 -m pip install -r requirements/requirements-docs.txt

## Build virtualenv for dempy
build-env-dempy:
	@python3 -m venv .venv-dempy && \
	source .venv-dempy/bin/activate && \
	python3 -m pip install --upgrade pip&& \
	python3 -m pip install -r requirements/requirements-dempy.txt

## Setup conda and all virtualenvs
setup-all: build-env build-env-note build-env-dev build-env-docs
	@echo "All virtualenvs are setup."

## Update project requirements
update-requirements:
	@source .venv/bin/activate && \
	cp requirements/requirements.txt requirements/requirements-old.txt && \
	pip3 freeze > requirements/requirements.txt && \
	diff requirements/requirements-old.txt requirements/requirements.txt

## Update dev project requirements
update-requirements-dev:
	@source .venv-dev/bin/activate && \
	cp requirements/requirements-dev.txt requirements/requirements-dev-old.txt && \
	pip3 freeze > requirements/requirements-dev.txt && \
	diff requirements/requirements-dev-old.txt requirements/requirements-dev.txt

.PHONY: install-pre-commit uninstall-pre-commit
## Install pre-commit and git hooks
install-pre-commit: build-env-dev
	@source .venv-dev/bin/activate && \
	pre-commit install --install-hooks && \
	pre-commit autoupdate

## Uninstall pre-commit and git hooks
uninstall-pre-commit:
	@source .venv-dev/bin/activate && \
	pre-commit uninstall && \
	pre-commit uninstall --hook-type pre-push && \
	rm -rf .git/hooks/pre-commit

.PHONY: clean clean-test clean-hydra clean-all
## Remove all build, test, coverage and Python artifacts
clean:
	rm -rf .venv*
	find . -type f -name '*.pyc' -delete
	find . -type f -name "*.DS_Store" -ls -delete
	find . -type f -name '*~' -exec rm -f {} +
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

## Remove test and coverage artifacts.
clean-test:
	rm -fr .tox/
	rm -fr .nox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache

## Remove hydra outputs.
clean-hydra:
	rm -rf outputs
	rm -rf runs
	rm -rf multirun

## Remove all artifacts.
clean-all: clean clean-test clean-hydra

.PHONY: test format format-fix coverage lint check-safety
## Run unit tests using pytest.
test: build-env-dev
	@source .venv-dev/bin/activate && \
	pytest

## Check style formatting using isort and black.
format: build-env-dev
	@source .venv-dev/bin/activate && \
	isort --check-only src && \
	black --check src/

## Fix formatting with black and isort. This updates files.
format-fix: build-env-dev
	@source .venv-dev/bin/activate && \
	black src && \
	isort src/

## Generate test coverage reports.
coverage: build-env-dev
	@source .venv-dev/bin/activate && \
	pytest --cov='src/.' tests/ && \
	coverage report

## Opens coverage html report
coverage-html: coverage
	@source .venv-dev/bin/activate && \
	coverage html

## Check code for lint errors using flake8.
lint: build-env-dev
	@source .venv-dev/bin/activate && \
	flake8 src

## Check for package vulnerabilities
check-safety: build-env-dev
	@source .venv-dev/bin/activate && \
	safety check --full-report && \
	bandit -ll --recursive hooks

.PHONY: commit push dvc-download dvc-upload change-version release
## Commit project, eg. make commit t="Title" m="Commit Message"
commit:
	@echo "Commit with title: $t and message: $m"
	@git commit -am $title $message

## Git push code and tags and dvc push new data.
push:
	git push && \
	git push --tags && \
	dvc push

## Get data from remote using dvc.
dvc-download:
	dvc pull

## Send data from remote using dvc
dvc-upload:
	dvc push

## Change to previous model + data version, eg make change-version v="0.1.0"
change-version:
	git checkout v$v && \
	dvc checkout

## Release new version.
release:
	git commit -am "Release code version $(VERSIONFILE)"
	git tag -a v$(VERSIONFILE) -m "Release tag for version $(VERSIONFILE)"
	git push
	git push --tags

.PHONY: build-docs-md mkdocs-build mkdocs-serve mkdocs-clean
build-docs-md: build-env-docs
	cp README.md docs/index.md && \
	source .venv-docs/bin/activate && \
	pip3 install -r requirements/requirements-docs.txt

## generate mkdocs HTML documentation, including API docs
mkdocs-build: build-docs-md
	source .venv-docs/bin/activate && \
	mkdocs build

## serve HTML documentation on localhost:8000.
mkdocs-serve: build-docs-md
	source .venv-docs/bin/activate && \
	mkdocs serve

## clean HTML documentation
mkdocs-clean:
	rm -rf site/*

.PHONY: project_version version-major version-minor version-micro
## current project version
project_version:
	@echo $(VERSIONFILE)

version-major:
	@echo "$(CURRENT_VERSION_MAJOR)"

version-minor:
	@echo "$(CURRENT_VERSION_MINOR)"

version-micro:
	@echo "$(CURRENT_VERSION_MICRO)"

.PHONY: tag-major tag-minor tag-micro
tag-major:
	@echo "$(CURRENT_TAG_MAJOR)"

tag-minor:
	@echo "$(CURRENT_TAG_MINOR)"

tag-micro:
	@echo "$(CURRENT_TAG_MICRO)"

#################################################################################
.PHONY: bump_major bump_minor bump_micro jenkins_bump
## Bump to next major version X+1.Y.Y
bump_major: tag-major
	echo "$(CURRENT_VERSION_MAJOR)" > VERSION.txt

## Bump to next minor version Y.X+1.Y
bump_minor: tag-minor
	@echo "$(CURRENT_VERSION_MINOR)" > VERSION.txt

## Bump to next micro version Y.Y.X+1
bump_micro: tag-micro
	@echo "$(CURRENT_VERSION_MICRO)" > VERSION.txt

## Version bump for Jenkins
jenkins_bump:
	@git config --global user.email "-"
	@git config --global user.name "Jenkins"
	@(git tag --sort=-creatordate | grep -E '^\d+\.\d+\.\d+$$' || echo '0.0.0') | head -n 1 > VERSION.txt
	@/scripts/bump $$(git log -1 --pretty=%B)
	@git tag $$(cat VERSION.txt)
	@git push origin $$(cat VERSION.txt)

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)              ** Available rules: ** $$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=25 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf " - %s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

# EOF
