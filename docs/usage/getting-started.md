# Getting Started

## Installation

### From PyPI (Recommended)

```bash
pip install geoterminal
```

### From Source

```bash
git clone https://github.com/jeronimoluza/geoterminal.git
cd geoterminal
pip install -e .
```

## Basic Usage

### Command Line Interface

The quickest way to get started with Geoterminal is through its command-line interface:

```bash
# Check installation
geoterminal --version

# Get help
geoterminal --help
```

### Python API

You can also use Geoterminal as a Python library:

```python
from geoterminal.geometry_operations import GeometryProcessor
from geoterminal.file_io import read_geometry_file

# Read a geometry file
gdf = read_geometry_file("input.geojson")

# Create a processor
processor = GeometryProcessor(gdf)

# Perform operations
buffered = processor.apply_buffer(distance=1000)
buffered.to_file("output.geojson")
```

## Next Steps

- Check out the [Commands](commands.md) section for detailed CLI usage
- See [Examples](examples.md) for common use cases
- Read the [API Reference](../api.md) for detailed Python API documentation
