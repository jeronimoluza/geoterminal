# Command Line Interface

## Overview

geoterminal's CLI provides two main modes of operation:

1. **Inspect Mode**: When only INPUT is provided
2. **Transform Mode**: When both INPUT and OUTPUT are provided

## Command Structure

```bash
geoterminal INPUT OUTPUT [OPTIONS]
```

### Arguments

- `INPUT`: Input geometry (file path or WKT string)
- `OUTPUT`: Output file path (optional; format determined by extension)

### Options

#### Inspection Options
- `--head N`: Show first N rows
- `--tail N`: Show last N rows
- `--shape`: Show number of rows and columns
- `--dtypes`: Show column data types
- `--crs`: Show coordinate reference system

#### Geometry Operations
- `--buffer-size SIZE`: Buffer size in CRS units
- `--unary-union`: Merge all geometries
- `--convex-hull`: Create convex hull
- `--centroid`: Calculate centroid
- `--envelope`: Get bounding box
- `--simplify TOL`: Simplify geometries with tolerance level

#### Filtering Operations
- `--query EXPR`: Filter using pandas query syntax
- `--intersects GEOM`: Filter by intersection
- `--mask GEOM`: Clip using mask geometry

#### Coordinate Operations
- `--input-crs EPSG`: Input CRS (default: 4326)
- `--output-crs EPSG`: Output CRS
- `--mask-crs EPSG`: Mask CRS (default: 4326)

#### H3 Operations
- `--h3-res RES`: H3 resolution (0-15)

#### File Options
- `--geometry-column COL`: WKT column name for CSV/ORC

### General Options

- `--version`: Show version information
- `--log-level {DEBUG,INFO,WARNING,ERROR}`: Set logging level (default: INFO)

## Error Handling

The CLI will exit with non-zero status in case of errors:

- 1: Invalid arguments
- 2: File operation error
- 3: Geometry operation error
- 4: H3 operation error

Error messages are printed to stderr with details about the failure.
