# Geoterminal

[![PyPI version](https://img.shields.io/pypi/v/geoterminal.svg)](https://pypi.python.org/pypi/geoterminal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Geoterminal is a powerful Python library and command-line tool designed to streamline geospatial data processing and H3 grid operations. It provides an intuitive interface for common GIS operations, supporting multiple file formats and offering both a Python API and CLI for maximum flexibility.

## Features

- **Flexible Input/Output**
  - Support for GeoJSON, Shapefile, CSV, ORC, and WKT formats
  - Direct WKT string input for quick operations
  - Automatic format detection and conversion

- **Geometry Operations**
  - Buffer creation with customizable distance
  - Geometry clipping with file or WKT mask
  - CRS transformation and validation

- **H3 Integration**
  - Convert geometries to H3 cells
  - Configurable resolution (0-15)
  - Optional geometry inclusion
  - Efficient spatial indexing

- **Developer-Friendly**
  - Clean Python API
  - Comprehensive CLI
  - Extensive documentation
  - Type hints and error handling

## Quick Start

### Installation

```bash
# Install from PyPI
pip install geoterminal
```

For development, we use Poetry. First install Poetry if you haven't already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or if you have Homebrew installed, you can do:

```bash
brew install poetry
```

Then clone and install the project:

```bash
# Clone the repository
git clone https://github.com/jeronimoluza/geoterminal.git
cd geoterminal

# Install dependencies and create virtual environment
poetry install

# Install with development dependencies
poetry install --with dev

# Install with documentation dependencies
poetry install --with docs

# Activate the virtual environment
poetry shell
```

## Usage

### Basic Usage

Geoterminal accepts both file paths and WKT strings as input:

```bash
# Convert between different formats
geoterminal input.shp output.geojson
geoterminal input.geojson output.csv
geoterminal input.csv output.orc

# Generate from WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson

# Work with CSV/ORC files using custom geometry columns
geoterminal input.csv output.geojson --geometry-column my_wkt_column
geoterminal input.orc output.shp --geometry-column my_wkt_column
```

### Processing Options

You can combine multiple processing options:

```bash
# Apply a buffer and convert to H3 cells
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 6

# Convert WKT to H3 cells with geometries
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson --h3-res 6 --h3-geom

# Reproject data
geoterminal input.shp output.csv --input-crs 4326 --output-crs 3857
```

### Additional Commands

```bash
# View first 10 rows of a file
geoterminal head -n 10 input.geojson

# View last 8 rows of a file
geoterminal tail -n 8 input.geojson

# Clip geometries using a mask file
geoterminal clip input.shp mask.geojson output.geojson

# Clip using WKT string as mask
geoterminal clip input.shp "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))" output.geojson
```

## Python API

```python
from geoterminal.geometry_operations import GeometryProcessor
from geoterminal.h3_operations import H3Processor
from geoterminal.file_io import read_geometry_file

# Read data
gdf = read_geometry_file("input.geojson")

# Geometry operations
processor = GeometryProcessor(gdf)
buffered = processor.apply_buffer(distance=1000)

# H3 operations
h3_processor = H3Processor(gdf)
h3_cells = h3_processor.polyfill(resolution=6)

# Export
h3_cells.to_file("output.geojson")
```

## Documentation

Comprehensive documentation is available:

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [API Reference](docs/api.md)
- [CLI Documentation](docs/cli.md)
- [FAQ](docs/faq.md)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
