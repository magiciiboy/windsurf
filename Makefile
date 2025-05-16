.PHONY: help venv install test clean

help:
	@echo "Available commands:"
	@echo "  make venv    - Create a Python 3.11 virtual environment"
	@echo "  make install - Install dependencies in development mode"
	@echo "  make test    - Run all tests with pytest"
	@echo "  make clean   - Clean up build artifacts and caches"

venv:
	@echo "Creating Python 3.11 virtual environment..."
	python3.11 -m venv .venv
	@echo "Virtual environment created."
	@echo "Activate with: source .venv/bin/activate"

install:
	@echo "Installing dependencies in development mode..."
	source .venv/bin/activate && pip install -e .
	@echo "Dependencies installed."

test:
	@echo "Running tests with pytest..."
	source .venv/bin/activate && pytest -v
	@echo "Tests completed."

clean:
	@echo "Cleaning up build artifacts and caches..."
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	@echo "Cleanup completed."
