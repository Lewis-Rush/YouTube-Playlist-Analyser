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
