.PHONY: setup test clean lint format docs help

help:
	@echo "Available commands:"
	@echo "  setup      Install project dependencies"
	@echo "  dev-setup  Install development dependencies"
	@echo "  test       Run tests"
	@echo "  coverage   Run tests with coverage report"
	@echo "  lint       Run code linting"
	@echo "  format     Format code"
	@echo "  clean      Clean up build files"
	@echo "  docs       Build documentation"

setup:
	pip install -r requirements.txt

dev-setup: setup
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/

coverage:
	pytest tests/ --cov=geoterminal --cov-report=term-missing

lint:
	flake8 geoterminal/ tests/
	mypy geoterminal/ tests/

format:
	black geoterminal/ tests/
	isort geoterminal/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -delete
	find . -name ".coverage" -delete
	find . -name "coverage.xml" -delete
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/

clean-docs:
	rm -rf docs/_build/

docs:
	mkdocs build

docs-serve:
	mkdocs serve
