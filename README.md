# GeoTerminal

[![PyPI version](https://img.shields.io/pypi/v/geoterminal.svg)](https://pypi.python.org/pypi/geoterminal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

GeoTerminal is a command-line tool designed to simplify common GIS tasks that you may encounter in your daily work.

## Features

- File format conversion (GeoJSON, Shapefile, CSV, ORC)
- Geometry operations (buffer, clip)
- H3 integration (polyfill)
- CRS transformations
- Inspect mode for quick data viewing
- Operation order preservation and offering both a Python API and CLI for maximum flexibility.



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

# Activate the virtual environment
poetry shell
```

## Usage

### Basic Usage

GeoTerminal accepts both file paths and WKT strings as input. The input and output file formats are automatically detected based on their extensions.

```bash
# Inspect data (show first 10 rows)
geoterminal input.shp --head 10

# Show CRS information
geoterminal input.shp --crs

# Convert formats
geoterminal input.shp output.geojson

# Operations are applied in the order specified
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 7  # Buffer first, then H3
geoterminal input.shp output.geojson --h3-res 7 --buffer-size 1000  # H3 first, then buffer

# Set log level for detailed output
geoterminal input.shp output.geojson --buffer-size 1000 --log-level DEBUG
```

### Processing Options

You can combine multiple processing options with your conversion commands:

```bash
# Apply a buffer of 1000 meters and convert to H3 cells
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 6

# Convert WKT to H3 cells with geometries
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson --h3-res 6 --h3-geom

# Reproject data
geoterminal input.shp output.csv --input-crs 4326 --output-crs 3857

# Clip geometries using a mask file
geoterminal input.shp output.geojson --mask mask.geojson --mask-crs 4326

# Clip geometries using a mask WKT
geoterminal input.shp output.geojson --mask "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"
```

### File Inspection

View the contents of your files using the head and tail commands:

```bash
# View first 10 rows of a file
geoterminal input.geojson --head --rows 10

# View last 8 rows of a file
geoterminal input.geojson --tail --rows 8
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
