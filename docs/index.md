# Geoterminal Documentation

Geoterminal is a powerful Python library for geospatial data processing and H3 operations. It provides a simple and efficient interface for working with various geospatial file formats and performing common geometric operations.

## Key Features

- **File Format Support**: GeoJSON, Shapefile, CSV, ORC, and WKT
- **Geometry Operations**: Buffer, union, convex hull, centroid, envelope, and more
- **Data Operations**: Query filtering using pandas syntax
- **H3 Integration**: Efficient hexagonal hierarchical geospatial indexing
- **Command Line Interface**: Easy-to-use CLI with operation chaining
- **Inspection Tools**: Shape, data types, and CRS information

## Quick Start

```bash
# Install Geoterminal
pip install geoterminal

# Process a file
geoterminal input.shp output.geojson

# Process a WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson

# Apply a buffer of 1000 meters and convert to H3 cells
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 6

# Chain operations to find urban centers
geoterminal cities.shp centers.wkt \
    --query "population > 1000000" \
    --unary-union \
    --centroid
```

## Documentation Sections

- [Installation](installation.md)
- [Usage Guide](usage.md)
- [API Reference](usage.md#python-api)
- [CLI Documentation](cli.md)
- [Contributing](contributing.md)

## Support

If you need help or have questions:

1. Check the [FAQ](faq.md)
2. Open an issue on GitHub
3. Join our community discussions

## License

Geoterminal is released under the MIT License. See the [LICENSE](https://github.com/jeronimoluza/geoterminal/blob/main/LICENSE) file for details.
