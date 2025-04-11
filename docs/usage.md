# Usage Guide

geoterminal provides both a command-line interface (CLI) and a Python API for geospatial operations.

## Command Line Interface

### Basic Usage

geoterminal has two main modes:

1. **Inspect Mode** (single input file):
```bash
# View data structure
geoterminal input.shp --shape     # Show rows and columns
geoterminal input.shp --dtypes    # Show column types
geoterminal input.shp --crs       # Show CRS information

# View data content
geoterminal input.shp --head 10   # First 10 rows
geoterminal input.shp --tail 5    # Last 5 rows
```

2. **Transform Mode** (input and output files):
```bash
# Process a file
geoterminal input.shp output.geojson

# Process a WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson
```

### Supported Formats

- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV/ORC with WKT column
- Direct WKT string input/output

For CSV/ORC files, specify the geometry column (default is "geometry"):

```bash
geoterminal input.csv output.geojson --geometry-column my_wkt_column
```

### Operations

#### Basic Operations
```bash
# Geometry Operations
geoterminal input.shp output.geojson --buffer-size 1000     # Buffer
geoterminal input.shp output.geojson --unary-union         # Merge geometries
geoterminal input.shp output.geojson --convex-hull         # Create hull
geoterminal input.shp output.geojson --centroid            # Get centroid
geoterminal input.shp output.geojson --simplify 0.001      # Simplify

# Filtering
geoterminal input.shp output.geojson --query "population > 1000000"  # By attribute

geoterminal input.shp output.geojson --intersects other.shp          # By intersection
geoterminal input.shp output.geojson --intersects "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"  # By intersection with WKT

geoterminal input.shp output.geojson --mask mask.geojson            # By mask
geoterminal input.shp output.geojson --mask "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"  # By mask with WKT

# Coordinate Systems
geoterminal input.shp output.geojson --input-crs 4326 --output-crs 3857

# H3 Grid
geoterminal input.shp output.geojson --h3-res 6
```

#### Operation Order

Operations are applied in sequence. Compare:
```bash
# Different results:
geoterminal input.shp out.geojson --buffer-size 1000 --h3-res 7  # Buffer first
geoterminal input.shp out.geojson --h3-res 7 --buffer-size 1000  # H3 first
```

#### Advanced Examples
```bash
# Generate metropolitan areas
geoterminal cities.shp centers.geojson \
    --query "population > 1000000" \
    --centroid \
    --buffer-size 1000

# Generate areas of interest in H3 hexagons
geoterminal density.shp h3_zones.geojson \
    --centroid \
    --buffer-size 5000 \
    --h3-res 8
```

## Python API

### Geometry Processing
```python
from geoterminal.geometry_operations import GeometryProcessor
import geopandas as gpd

# Initialize
gdf = gpd.read_file("input.geojson")
processor = GeometryProcessor(gdf)

# Operations
buffered = processor.apply_buffer(distance=1000)
union = processor.unary_union()
hull = processor.convex_hull()
filtered = processor.intersects(other_gdf)

# Export
buffered.to_file("output.geojson")
```

### H3 Grid Operations
```python
from geoterminal.h3_operations import H3Processor

# Convert to H3
processor = H3Processor(gdf)
h3_cells = processor.polyfill(resolution=9)
h3_cells.to_file("output.geojson")
```

### File Operations
```python
from geoterminal.file_io import read_geometry_file, export_data

# Read/Write
gdf = read_geometry_file("input.geojson")
export_data(gdf, "output.geojson")
```

For more examples, check our [examples directory](https://github.com/jeronimoluza/geoterminal/tree/main/examples).
