# Installation Guide

## Requirements

- Python 3.10 or higher
- Poetry (Python package manager)

## Dependencies

geoterminal requires the following main dependencies:
- geopandas
- shapely
- h3
- pandas
- pyarrow

## Installation Methods

### 1. From PyPI (Recommended)

```bash
pip install geoterminal
```

### 2. From Source (Development)

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone https://github.com/jeronimoluza/geoterminal.git
cd geoterminal
```

3. Install dependencies and create virtual environment:
```bash
poetry install
```

4. Activate the virtual environment:
```bash
poetry shell
```

### Optional Dependencies

For development:
```bash
poetry install --with dev
```

For documentation:
```bash
poetry install --with docs
```

## Verifying Installation

To verify that geoterminal is installed correctly:

```bash
geoterminal --version
```

## Common Installation Issues

### Missing GDAL

If you encounter GDAL-related errors:

1. On Ubuntu/Debian:
```bash
sudo apt-get install gdal-bin libgdal-dev
```

2. On macOS:
```bash
brew install gdal
```

3. On Windows:
   - Use [OSGeo4W](https://trac.osgeo.org/osgeo4w/) installer
   - Or install via conda: `conda install gdal`

### Other Issues

For other installation issues:
1. Check your Python version: `python --version`
2. Ensure pip is up to date: `pip install --upgrade pip`
3. Check the [GitHub issues](https://github.com/jeronimoluza/geoterminal/issues) for similar problems
4. Open a new issue if the problem persists
