PYTHON_INTERPRETER := python3
VENV_DIR := venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip
PYTHONPATH := $(shell pwd)

create-environment:
	@echo ">>> Check Python version"
	$(PYTHON_INTERPRETER) --version
	@echo ">>> Setting up virtual environment"
	$(PYTHON_INTERPRETER) -m venv $(VENV_DIR)

venv-requirements: create-environment
	$(VENV_PIP) install -r requirements.txt

env-setup: venv-requirements 
	@echo "Environment ready. Use $(VENV_PYTHON) to run Python."

run-tests: 
	PYTHONPATH=$(CURDIR) pytest tests

run-black:
	black src
	black tests

run-flake8:
	flake8 test/test_main test/test_utils.py src/main.py src/utils.py \
		--max-line-length=88 \
		--statistics

run-pep8: run-black run-flake8
	@echo "Project is pep8 compliant."

run-bandit:
	bandit -r src -v

run-coverage:
	export PYTHONPATH=$(PWD)/src && \
	coverage erase && \
	coverage run -m pytest && \
	coverage report -m

api-setup:
	@read -p "Enter Google API key: " key; \
	echo "API_KEY=$$key" > .env; \

run-analyser:
	python -m src.main


