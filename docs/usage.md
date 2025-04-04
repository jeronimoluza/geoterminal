# Usage Guide

## Basic Concepts

Geoterminal provides both a Python API and a command-line interface (CLI) for geospatial operations.

## Command Line Interface

### Basic Usage

Geoterminal accepts both file paths and WKT strings as input:

```bash
# Process a file
geoterminal input.shp output.geojson

# Process a WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson
```

### Processing Options

You can combine multiple processing options:

```bash
# Apply a buffer and convert to H3 cells
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 9

# Convert WKT to H3 cells with geometries
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson --h3-res 9 --h3-geom

# Reproject data
geoterminal input.shp output.geojson --input-crs 4326 --output-crs 3857
```

### Additional Commands

```bash
# Clip geometries using a mask file
geoterminal clip input.shp mask.geojson output.csv

# Clip using WKT string as mask
geoterminal clip input.geojson "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))" output.csv
```

### File Format Support

Geoterminal supports multiple file formats:

- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV with WKT column
- Direct WKT string input

## Python API

### Geometry Operations

```python
from geoterminal.geometry_operations import GeometryProcessor
import geopandas as gpd

# Load data
gdf = gpd.read_file("input.geojson")
processor = GeometryProcessor(gdf)

# Apply buffer
buffered = processor.apply_buffer(distance=1000)

# Reproject
reprojected = processor.reproject("EPSG:3857")

# Export
buffered.to_file("output.geojson")
```

### H3 Operations

```python
from geoterminal.h3_operations import H3Processor
import geopandas as gpd

# Load data
gdf = gpd.read_file("input.geojson")
processor = H3Processor(gdf)

# Convert to H3 cells
h3_cells = processor.polyfill(resolution=9)

# Export with geometries
h3_cells.to_file("output.geojson")
```

### File I/O

```python
from geoterminal.file_io import read_geometry_file, export_data

# Read from various sources
gdf = read_geometry_file("input.geojson")
gdf_wkt = read_geometry_file("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", crs="EPSG:4326")

# Export data
export_data(gdf, "output.geojson")
```

## Best Practices

1. **CRS Management**

   - Always specify the CRS when working with WKT input
   - Use appropriate CRS for your geographic region

2. **Memory Management**
   - For large datasets, consider processing in chunks
   - Use appropriate H3 resolution for your use case

3. **Error Handling**
   - Always check for invalid geometries
   - Handle exceptions appropriately

## Examples

Check out our [examples directory](https://github.com/jeronimoluza/geoterminal/tree/main/examples) for more detailed usage examples.
