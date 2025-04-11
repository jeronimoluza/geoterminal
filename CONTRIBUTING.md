# Contributing to geoterminal

Thank you for your interest in contributing to geoterminal! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/geoterminal.git
   cd geoterminal
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Style Guidelines

- Follow PEP 8 style guide for Python code
- Use type hints for function arguments and return values
- Write docstrings for all public functions, classes, and methods
- Keep functions focused and single-purpose
- Add tests for new functionality

## Making Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure all tests pass:
   ```bash
   pytest
   ```

3. Commit your changes with a descriptive message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

4. Push to your fork and create a pull request

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Add tests for new functionality
3. Update documentation if needed
4. Ensure all CI checks pass
5. Request review from maintainers

## Reporting Issues

- Use the issue templates when reporting bugs or requesting features
- Provide clear steps to reproduce bugs
- Include relevant system information and package versions

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## Get Help

If you need help, you can:
- Open an issue with your question
- Join our community discussions
- Reach out to maintainers

Thank you for contributing to geoterminal!
