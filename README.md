# geoterminal

[![PyPI version](https://img.shields.io/pypi/v/geoterminal.svg)](https://pypi.python.org/pypi/geoterminal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

geoterminal is a command-line interface tool to quickly inspect and transform geospatial data.

## Features

- File format conversion (GeoJSON, Shapefile, CSV, ORC, WKT)
- Geometry operations:
  - Buffer and clip
  - Unary union
  - Convex hull
  - Centroid
  - Envelope (bounding box)
  - Simplify geometries
  - Intersect with other geometries
  - More to come!
- H3 integration (polyfill)
- CRS transformations
- Data operations:
  - Query filtering using pandas syntax
- Inspect operations:
  - View first/last N rows
  - Get CRS information
  - Get shape (rows × columns)
  - Get column data types
- Operation order preservation



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

geoterminal accepts both file paths and WKT strings as input. The input and output file formats are automatically detected based on their extensions.

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
# Geometry Operations
# Apply a buffer
geoterminal input.shp output.geojson --buffer-size 1000

# Create a unary union of all geometries
geoterminal input.shp output.geojson --unary-union

# Create a convex hull
geoterminal input.shp output.geojson --convex-hull

# Calculate centroid
geoterminal input.shp output.geojson --centroid

# Get envelope (bounding box)
geoterminal input.shp output.geojson --envelope

# Simplify geometries
geoterminal input.shp output.geojson --simplify 0.001

# Filter geometries that intersect with another file or WKT
geoterminal input.shp output.geojson --intersects other.shp
geoterminal input.shp output.geojson --intersects "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"

# H3 Operations
# Convert to H3 cells (includes hexagon geometries)
geoterminal input.shp output.geojson --h3-res 6

# Reprojection
# Reproject data to a different CRS
geoterminal input.shp output.csv --input-crs 4326 --output-crs 3857

# Clipping
# Clip geometries using a mask file
geoterminal input.shp output.geojson --mask mask.geojson --mask-crs 4326

# Clip geometries using a mask WKT
geoterminal input.shp output.geojson --mask "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"

# Data Operations
# Filter data using pandas query syntax
geoterminal input.shp output.geojson --query "population > 1000000"
```

### Chaining Operations

Operations are applied in the order they appear in the command line. Here are some practical examples:

```bash
# Example 1: Find the center of a region's urban areas
# 1. Filter cities with population > 1M
# 2. Calculate the centroids
# 3. Buffer the centroids by 1000 meters
geoterminal cities.shp center.geojson \
    --query "population > 1000000" \
    --centroid \
    --buffer-size 1000

# Example 2: Create a simplified boundary around intersecting features
# 1. Filter features that intersect with a region of interest
# 2. Create a buffer around them
# 3. Merge all buffers into one
# 4. Get the convex hull as a simplified boundary
geoterminal features.shp boundary.geojson \
    --intersects "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))" \
    --buffer-size 1000 \
    --convex-hull
```

### File Inspection

Inspect your geospatial data with various commands:

```bash
# View first/last N rows
geoterminal input.geojson --head 10  # First 10 rows
geoterminal input.geojson --tail 5   # Last 5 rows

# Get information about the data
geoterminal input.geojson --crs      # Show coordinate reference system
geoterminal input.geojson --shape    # Show number of rows and columns
geoterminal input.geojson --dtypes   # Show column data types
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

# Export (supports various formats)
h3_cells.to_file("output.geojson")  # GeoJSON
h3_cells.to_file("output.shp")      # Shapefile
h3_cells.to_file("output.csv")      # CSV with WKT geometry
h3_cells.to_file("output.wkt")      # WKT (single geometry or GEOMETRYCOLLECTION)
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
