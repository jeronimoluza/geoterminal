# Command Line Interface

## Overview

GeoTerminal's CLI provides two main modes of operation:

1. **Inspect Mode**: When only INPUT is provided
2. **Transform Mode**: When both INPUT and OUTPUT are provided

## Command Structure

```bash
geoterminal INPUT [OUTPUT] [OPTIONS]
```

## Arguments

- `INPUT`: Required. Input geometry (file path or WKT string)
- `OUTPUT`: Optional. Output file path (format determined by extension)

## Options

### Inspect Mode Options

- `--head N`: Show first N rows in WKT format
- `--tail N`: Show last N rows in WKT format
- `--crs`: Show coordinate reference system information
- `--shape`: Show number of rows and columns
- `--dtypes`: Show column data types

### Transform Mode Options

#### Geometry Operations
- `--buffer-size SIZE`: Apply buffer of SIZE meters
- `--unary-union`: Merge all geometries into one
- `--convex-hull`: Create convex hull of geometries
- `--centroid`: Calculate centroid of geometries
- `--envelope`: Get bounding box of geometries

#### Filtering Operations
- `--query EXPR`: Filter data using pandas query syntax
- `--intersects GEOM`: Filter geometries that intersect with GEOM
- `--mask GEOM`: Clip geometries using mask (file or WKT)

#### Coordinate Operations
- `--input-crs EPSG`: Set input CRS (default: 4326)
- `--output-crs EPSG`: Set output CRS

#### H3 Operations
- `--h3-res RES`: Convert to H3 hexagons at resolution RES

#### File Options
- `--geometry-column COL`: Column name for CSV/ORC files

### General Options

- `--version`: Show version information
- `--log-level {DEBUG,INFO,WARNING,ERROR}`: Set logging level (default: INFO)

## Operation Order

In Transform Mode, operations are applied in the exact order they appear in the command line. For example:

```bash
# These commands produce different results:
geoterminal input.shp out.geojson --buffer-size 1000 --h3-res 7  # Buffer first
geoterminal input.shp out.geojson --h3-res 7 --buffer-size 1000  # H3 first
```

The Geoterminal CLI provides a powerful interface for geospatial operations. It supports both file-based and WKT string input, with various processing options.

## Basic Usage

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

### Examples

#### Basic Operations
```bash
# File conversion
geoterminal input.shp output.geojson

# Process WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson
```

#### Data Inspection
```bash
# View data structure
geoterminal input.geojson --shape    # Show rows × columns
geoterminal input.geojson --dtypes   # Show column types
geoterminal input.geojson --crs      # Show CRS

# View data content
geoterminal input.geojson --head 10  # First 10 rows
geoterminal input.geojson --tail 5   # Last 5 rows
```

#### Single Operations
```bash
# Geometry operations
geoterminal input.shp output.geojson --buffer-size 1000
geoterminal input.shp output.geojson --unary-union
geoterminal input.shp output.geojson --convex-hull
geoterminal input.shp output.geojson --centroid

# Filtering operations
geoterminal input.shp output.geojson --query "population > 1000000"
geoterminal input.shp output.geojson --intersects other.shp

# Coordinate operations
geoterminal input.shp output.geojson --input-crs 4326 --output-crs 3857

# H3 operations
geoterminal input.shp output.geojson --h3-res 6
```

#### Advanced Chaining
```bash
# Find urban centers
geoterminal cities.shp center.wkt \
    --query "population > 1000000" \
    --unary-union \
    --centroid

# Create service areas
geoterminal points.shp area.geojson \
    --intersects "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))" \
    --buffer-size 1000 \
    --unary-union \
    --convex-hull

# Custom CSV processing
geoterminal input.csv output.geojson \
    --geometry-column my_wkt_column \
    --query "status == 'active'" \
    --buffer-size 500
```

## File Format Support

Geoterminal supports multiple file formats:

- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV with WKT column
- ORC with WKT column
- Direct WKT string input

For CSV and ORC files, you can specify which column contains the WKT geometry strings. If not specified, it will look for columns named: geometry, geom, wkt, the_geom.

## Coordinate Reference Systems

- Default CRS: EPSG:4326 (WGS 84)
- Input CRS can be specified using EPSG codes
- Output CRS can be specified using EPSG codes
- Mask CRS defaults to EPSG:4326 but can be overridden

## H3 Options

- Resolution range: 0-15
- Default includes H3 geometries (can be disabled with --h3-geom False)
- Geometries are stored in WKT format

## Best Practices

1. **Input Validation**

   - Always specify CRS when working with WKT input
   - Validate input geometries before processing
   - Use appropriate CRS for your geographic region

2. **Performance**

   - For large datasets, consider processing in chunks
   - Use appropriate H3 resolution based on your use case
   - Buffer size should be appropriate for your CRS units

3. **Error Handling**

   - Check for invalid geometries
   - Handle exceptions appropriately
   - Validate CRS codes before use

## Error Handling

The CLI will exit with non-zero status in case of errors:

- 1: Invalid arguments
- 2: File operation error
- 3: Geometry operation error
- 4: H3 operation error

Error messages are printed to stderr with details about the failure.

## Environment Variables

- `GEOTERMINAL_LOG_LEVEL`: Set logging level (default: INFO)
- `GEOTERMINAL_MAX_WORKERS`: Maximum number of worker processes for parallel operations
