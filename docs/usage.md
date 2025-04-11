# Usage Guide

GeoTerminal provides two main modes of operation: Inspect Mode and Transform Mode.

## Inspect Mode

When only an input file is provided, GeoTerminal enters inspect mode, allowing you to quickly examine your data:

```bash
# View data structure
geoterminal input.shp --shape     # Show number of rows and columns
geoterminal input.shp --dtypes    # Show column data types

# View data content
geoterminal input.shp --head 10   # First 10 rows
geoterminal input.shp --tail 5    # Last 5 rows

# Show CRS information
geoterminal input.shp --crs
```

## Transform Mode

When both input and output files are provided, GeoTerminal enters transform mode. Operations are applied in the exact order they appear in the command line:

```bash
# Buffer first, then convert to H3
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 7

# Convert to H3 first, then buffer
geoterminal input.shp output.geojson --h3-res 7 --buffer-size 1000
```

## Logging

Control the verbosity of output with the `--log-level` flag:

```bash
# Default (INFO) - minimal output
geoterminal input.shp output.geojson --buffer-size 1000

# Debug mode - detailed output with timestamps and file info
geoterminal input.shp output.geojson --buffer-size 1000 --log-level DEBUG
```

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

Geoterminal provides various operations that can be used individually:

```bash
# Geometry Operations
geoterminal input.shp output.geojson --buffer-size 1000     # Buffer
geoterminal input.shp output.geojson --unary-union         # Merge all geometries
geoterminal input.shp output.geojson --convex-hull         # Create convex hull
geoterminal input.shp output.geojson --centroid            # Calculate centroid
geoterminal input.shp output.geojson --envelope            # Get bounding box

# Filtering Operations
geoterminal input.shp output.geojson --query "population > 1000000"  # Filter by attribute
geoterminal input.shp output.geojson --intersects other.shp          # Filter by intersection
geoterminal input.shp output.geojson --mask mask.geojson            # Clip by mask

# Coordinate Operations
geoterminal input.shp output.geojson --input-crs 4326 --output-crs 3857  # Reproject

# H3 Operations
geoterminal input.shp output.geojson --h3-res 6  # Convert to H3 hexagons
```

### Advanced Usage

Operations in Geoterminal are applied in the order they appear in the command line. This allows for powerful combinations of operations:

```bash
# Example 1: Find urban centers
# 1. Filter cities with population > 1M
# 2. Create a unary union of all large cities
# 3. Calculate the centroid
geoterminal cities.shp center.wkt \
    --query "population > 1000000" \
    --unary-union \
    --centroid

# Example 2: Create service areas
# 1. Filter points that intersect with a region
# 2. Create buffers around them
# 3. Merge overlapping buffers
# 4. Get a simplified boundary
geoterminal points.shp area.geojson \
    --intersects "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))" \
    --buffer-size 1000 \
    --unary-union \
    --convex-hull

# Example 3: H3 analysis of high-density areas
# 1. Filter high-density areas
# 2. Reproject to equal-area projection
# 3. Convert to H3 cells
geoterminal density.shp h3_zones.geojson \
    --query "density > 1000" \
    --input-crs 4326 --output-crs 3857 \
    --h3-res 8
```

### File Inspection

Geoterminal provides comprehensive inspection capabilities:

```bash
# View data structure
geoterminal input.geojson --shape    # Number of rows and columns
geoterminal input.geojson --dtypes   # Column data types
geoterminal input.geojson --crs      # Coordinate reference system

# View data content
geoterminal input.geojson --head 10  # First 10 rows
geoterminal input.geojson --tail 5   # Last 5 rows
```

### File Format Support

Geoterminal supports multiple file formats:

- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV with WKT column
- ORC with WKT column
- Direct WKT string input

For CSV and ORC files, you can specify which column contains the WKT geometry strings:

```bash
# Use default behavior (looks for columns named: geometry, geom, wkt, the_geom)
geoterminal input.csv output.geojson

# Specify a custom geometry column
geoterminal input.csv output.geojson --geometry-column my_custom_wkt_column

# Same works for ORC files
geoterminal input.orc output.geojson --geometry-column my_custom_wkt_column
```

## Python API

### Geometry Operations

```python
from geoterminal.geometry_operations import GeometryProcessor
import geopandas as gpd

# Load data
gdf = gpd.read_file("input.geojson")
processor = GeometryProcessor(gdf)

# Basic operations
buffered = processor.apply_buffer(distance=1000)
reprojected = processor.reproject("EPSG:3857")

# Advanced operations
union = processor.unary_union()                # Merge all geometries
hull = processor.convex_hull()                 # Create convex hull
centroid = processor.centroid()                # Calculate centroid
envelope = processor.envelope()                # Get bounding box
filtered = processor.intersects(other_gdf)     # Filter by intersection

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

## Examples

Check out our [examples directory](https://github.com/jeronimoluza/geoterminal/tree/main/examples) for more detailed usage examples.
