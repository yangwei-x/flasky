PYTHON ?= python
REQ_DIR := requirements
IN_FILES := $(wildcard $(REQ_DIR)/*.in)
LOCK_SCRIPT := scripts/update_locks.sh

.PHONY: lock lock-all sync dev prod clean-venv help test test-cov test-one

lock-all: ## Recompile all requirement lock files
	@$(LOCK_SCRIPT)

lock: ## Recompile only specified groups. Usage: make lock TARGETS="base dev"
	@if [ -z "$(TARGETS)" ]; then echo "Specify TARGETS=... (e.g. base dev)"; exit 1; fi
	@$(LOCK_SCRIPT) $(TARGETS)

sync: ## Sync current venv to prod lock (override with FILE=requirements/dev.txt)
	@which pip-sync >/dev/null 2>&1 || $(PYTHON) -m pip install -q pip-tools
	@pip-sync $(FILE)

dev: ## Install dev environment
	$(PYTHON) -m pip install -r $(REQ_DIR)/dev.txt

prod: ## Install prod environment
	$(PYTHON) -m pip install -r $(REQ_DIR)/prod.txt

test: ## Run full test suite
	$(PYTHON) -m flask test

test-cov: ## Run tests with coverage
	FLASK_COVERAGE=1 $(PYTHON) -m flask test --coverage

clean-venv: ## Remove local virtual environment directories
	rm -rf .venv .venv-tmp

help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sed 's/:.*## /\t/'
