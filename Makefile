# Makefile for a PyPI package to run pytest on all files in tsops

# Variables
PACKAGE_NAME := tsops
SRC_DIR := $(PACKAGE_NAME)
TEST_DIR := tests
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest -s -vvv --pdb tests --cov tsops
PIP_COMPILE := $(PYTHON) -m piptools compile

# Default target
.PHONY: all
all: test

# Compile requirements from reqs.in
.PHONY: compile-requirements
compile-requirements:
	$(PIP_COMPILE) -o requirements.txt reqs.in

# Set up the virtual environment
.PHONY: venv
venv: compile-requirements
	$(PYTHON) -m venv venv
	. venv/bin/activate

# Install dependencies
.PHONY: install
install: venv
	. venv/bin/activate && $(PIP) install -r requirements.txt

# Run tests using pytest
.PHONY: test
test: install
	. venv/bin/activate && PYTHONPATH=. $(PYTEST) $(TEST_DIR)

# Clean the environment
.PHONY: clean
clean:
	rm -rf venv
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Help message
.PHONY: help
help:
	@echo "Makefile for running pytest on all files in tsops"
	@echo ""
	@echo "Usage:"
	@echo "  make            - Run tests (default target)"
	@echo "  make compile-requirements - Compile requirements from reqs.in"
	@echo "  make venv       - Set up the virtual environment"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests using pytest"
	@echo "  make clean      - Clean the environment"
	@echo "  make help       - Show this help message"

publish:
	rm -rf dist build *.egg-info && python3 -m build && python3 -m twine upload dist/* --verbose
