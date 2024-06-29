
.PHONY: lint-fix
lint-fix:  ## Runs linting in the local environment, updates files in place
	black --version
	black --config ./pyproject.toml .
	isort . --resolve-all-configs --config-root .
	flake8 --config ./.flake8 .

.PHONY: test
test:  ## Runs pytest in the local environment and lint checks
	pytest -v -s