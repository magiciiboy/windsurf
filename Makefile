.PHONY: help venv install test clean build lint format check develop

help:
	@echo "Available commands:"
	@echo "  make venv    - Create a Python 3.11 virtual environment"
	@echo "  make install - Install dependencies in development mode"
	@echo "  make lint    - Run linting checks"
	@echo "  make test    - Run all tests with pytest"
	@echo "  make build   - Build distribution packages"
	@echo "  make clean   - Clean up build artifacts and caches"

venv:
	@echo "Creating Python 3.11 virtual environment..."
	python3.11 -m venv .venv
	@echo "Virtual environment created."
	@echo "Activate with: source .venv/bin/activate"

install: venv
	@echo "Installing dependencies in development mode..."
	source .venv/bin/activate && pip install -e .
	@echo "Dependencies installed."

lint:
	# Run type checking
	mypy src tests
	
	# Run code analysis
	pylint src tests
	
	# Run style checking
	black --check src tests

format:
	# Format code with black
	black src tests

check: lint test

test:
	python -m pytest tests/ --cov=python_standards_checker --cov-report=term-missing

build: install
	@echo "Building distribution packages..."
	source .venv/bin/activate && python -m build .
	@echo "Build completed."

develop:
	pip install -e .[dev]

clean:
	@echo "Cleaning up build artifacts and caches..."
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf python_standards_checker.egg-info
	@echo "Cleanup completed."
