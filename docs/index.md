# Geoterminal Documentation

Geoterminal is a powerful Python library for geospatial data processing and H3 operations. It provides a simple and efficient interface for working with various geospatial file formats and performing common geometric operations.

## Features

- **Multiple File Format Support**: Work with GeoJSON, Shapefile, CSV, and WKT formats
- **Geometry Operations**: Buffer, clip, and reproject geometries
- **H3 Integration**: Efficient hexagonal hierarchical geospatial indexing
- **Command Line Interface**: Easy-to-use CLI for common operations

## Quick Start

```bash
# Install Geoterminal
pip install geoterminal

# Process a file
geoterminal input.shp output.geojson

# Process a WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson

# Apply a buffer and convert to H3 cells
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 9
```

## Documentation Sections

- [Installation](installation.md)
- [Usage Guide](usage.md)
- [API Reference](api.md)
- [CLI Documentation](cli.md)
- [Contributing](contributing.md)

## Support

If you need help or have questions:

1. Check the [FAQ](faq.md)
2. Open an issue on GitHub
3. Join our community discussions

## License

Geoterminal is released under the MIT License. See the [LICENSE](https://github.com/jeronimoluza/geoterminal/blob/main/LICENSE) file for details.
