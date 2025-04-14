# Contributing Guide

Thank you for your interest in contributing to geoterminal! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/geoterminal.git
cd geoterminal
```

2. Create a virtual environment:
```bash
poetry install
poetry shell
```

3. Install development dependencies:
```bash
pip install -e .
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Development Workflow

1. Create a new branch:
```bash
git checkout -b feature-name
```

2. Make your changes and write tests

3. Run tests:
```bash
pytest
```

4. Run pre-commit checks:
```bash
pre-commit run --all-files
```

5. Commit your changes:
```bash
git add .
git commit -m "Description of changes"
```

6. Push to your fork and create a pull request

## Code Style

We use:

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

## Testing

- Write tests for new features
- Maintain or improve coverage
- Use pytest fixtures when appropriate
- Test both success and error cases

## Documentation

- Update docstrings (Google style)
- Update relevant documentation files
- Include doctest examples where helpful
- Update CHANGELOG.md

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Update CHANGELOG.md
4. Ensure CI checks pass
5. Request review from maintainers

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## Get Help

If you need help, you can:
- Open an issue with your question
- Join our community discussions
- Reach out to maintainers

Thank you for contributing to geoterminal!
