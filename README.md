# Geoterminal

[![PyPI version](https://badge.fury.io/py/geoterminal.svg)](https://badge.fury.io/py/geoterminal)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Geoterminal is a powerful Python library and command-line tool designed to streamline geospatial data processing and H3 grid operations. It provides an intuitive interface for common GIS operations, supporting multiple file formats and offering both a Python API and CLI for maximum flexibility.

## Features

- **Flexible Input/Output**
  - Support for GeoJSON, Shapefile, CSV, and WKT formats
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

Alternatively, you can clone the repository and install the dependencies:

```bash
git clone https://github.com/jeronimoluza/geoterminal.git
poetry install
```

## Usage

### Conversion With H3 Resolution Specification

To convert data and apply an H3 resolution, specify the `--h3_res` option followed by the desired resolution level:

```bash
geoterminal input.geojson output.csv --input_crs EPSG:4326 --output_crs EPSG:3857 --h3_res=9
```

This example converts the data to an H3 index at resolution level 9.

### Including H3 Geometry

To include H3 geometries in the output, set the `--h3_geom` option to `True`:

```bash
geoterminal input.geojson output_with_geometry.h3 --input_crs EPSG:4326 --output_crs EPSG:3857 --h3_res=9 --h3_geom=True
```

This command converts the data to an H3 index at resolution level 9 and includes the H3 geometries in the output file.

### Applying Buffer Distance

To apply a buffer distance to the data during conversion, use the `--buffer_size` option followed by the desired buffer distance in meters:

```bash
geoterminal input.geojson output_buffered.geojson --buffer_size=1000
```

This example applies a 1000-degree buffer to the data during conversion.

## Command Line

```bash
# Clip geometries using a mask file
geoterminal clip input.geojson mask.geojson output.geojson

# Clip using WKT string
geoterminal clip input.geojson "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))" output.geojson

# Create buffer
geoterminal buffer input.geojson output.geojson --distance 1000

# Convert to H3 cells
geoterminal h3 input.geojson output.geojson --resolution 9
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
h3_cells = h3_processor.polyfill(resolution=9)

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
