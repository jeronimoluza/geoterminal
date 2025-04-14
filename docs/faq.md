# Frequently Asked Questions (FAQ)

## General Questions

### What is geoterminal?
geoterminal is a Python library and command-line tool for geospatial data processing, focusing on geometry operations and H3 grid integration.

### What file formats are supported?
geoterminal supports:

- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV with WKT column
- ORC with WKT column
- Direct WKT string input/output

## Installation

### Why am I getting GDAL-related errors?
GDAL is a required dependency that sometimes needs to be installed separately. See the [Installation Guide](installation.md) for platform-specific instructions.

### Can I use geoterminal with Python 3.7?
No, geoterminal requires Python 3.10 or higher due to type hint features and dependency requirements.

## Usage

### How do I handle large datasets?
For large datasets:

1. Process data in chunks when possible
2. Use appropriate H3 resolution
3. Consider using memory-efficient formats like parquet
4. Set the `GEOTERMINAL_MAX_WORKERS` environment variable for parallel processing

### Why is my WKT input not working?
Common issues with WKT input:

1. Missing CRS specification (use `--mask-crs` for CLI or `crs` parameter in API)
2. Invalid WKT syntax
3. Self-intersecting or invalid geometry

## Contributing

### How can I contribute?
See our [Contributing Guide](contributing.md) for details on:

1. Setting up development environment
2. Running tests
3. Submitting pull requests
4. Code style guidelines

### Where can I report bugs?
Report bugs on our [GitHub Issues](https://github.com/jeronimoluza/geoterminal/issues) page.
