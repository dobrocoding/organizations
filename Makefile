#!make
.DEFAULT_GOAL := docker-test

# Makefile target args
args = $(filter-out $@,$(MAKECMDGOALS))

# Command shortcuts
mypy = poetry run mypy ./app
pyright = $(shell cat .env_example | xargs) poetry run pyright
pytest = poetry run pytest
ruff = poetry run ruff
spec = $(shell cat .env_example | xargs) poetry run python -m app.cli api spec


.PHONY: format
format:
	$(ruff) format .
	$(ruff) check --fix .


.PHONY: docker-lint
docker-lint:
	docker run --rm -i -v $(shell pwd)/.hadolint.yaml:/.config/hadolint.yaml hadolint/hadolint < Dockerfile


.PHONY: generate-spec
generate-spec: artefacts
	$(spec) --filename artefacts/spec.yaml


.PHONY: spec-lint
spec-lint: generate-spec
	docker run --rm -v $(shell pwd):/tmp stoplight/spectral \
		lint --fail-severity info --ruleset "/tmp/.spectral.yaml" /tmp/artefacts/spec.yaml


.PHONY: python-lint
python-lint:
	$(ruff) check . --preview
	$(mypy)
	$(pyright)


.PHONY: lint
lint: docker-lint spec-lint python-lint


.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf dist *.egg-info
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -f .coverage
	rm -f .coverage.*
	rm -rf artefacts
	rm -rf .hypothesis


.PHONY: docker-test
docker-test:
	docker compose -f docker-compose.test.yaml up --build --exit-code-from tests


.PHONY: test-local
test-local:
	$(pytest) --no-header --no-cov -vv tests


.PHONY: artefacts
artefacts:
	mkdir -p artefacts
