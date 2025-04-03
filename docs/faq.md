# Frequently Asked Questions (FAQ)

## General Questions

### What is Geoterminal?
Geoterminal is a Python library and command-line tool for geospatial data processing, focusing on geometry operations and H3 grid integration.

### What file formats are supported?
Geoterminal supports:
- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV with WKT column
- Direct WKT string input

## Installation

### Why am I getting GDAL-related errors?
GDAL is a required dependency that sometimes needs to be installed separately. See the [Installation Guide](installation.md) for platform-specific instructions.

### Can I use Geoterminal with Python 3.7?
No, Geoterminal requires Python 3.8 or higher due to type hint features and dependency requirements.

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

### How do I choose the right H3 resolution?
H3 resolution choice depends on your use case:
- Resolution 0-3: Continental scale
- Resolution 4-7: Regional scale
- Resolution 8-10: City scale
- Resolution 11-15: Building scale

Consider that each increase in resolution approximately septuples the number of cells.

## Common Issues

### Invalid Geometry Errors
1. Check for self-intersecting polygons
2. Ensure geometries are properly closed
3. Use `shapely.is_valid` to validate geometries
4. Consider using `shapely.make_valid()`

### CRS Mismatches
1. Always check input CRS
2. Use appropriate CRS for your region
3. Be careful with lat/lon order in WKT
4. Remember that H3 expects WGS84 (EPSG:4326)

### Performance Issues
1. Use appropriate H3 resolution
2. Enable parallel processing
3. Consider chunking large datasets
4. Profile memory usage

## Contributing

### How can I contribute?
See our [Contributing Guide](contributing.md) for details on:
1. Setting up development environment
2. Running tests
3. Submitting pull requests
4. Code style guidelines

### Where can I report bugs?
Report bugs on our [GitHub Issues](https://github.com/jeronimoluza/geoterminal/issues) page.
