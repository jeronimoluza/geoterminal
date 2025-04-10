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

### Transform Mode Options

- `--buffer-size SIZE`: Apply buffer of SIZE meters
- `--h3-res RES`: Convert to H3 hexagons at resolution RES
- `--mask FILE`: Clip geometries using mask file
- `--input-crs EPSG`: Set input CRS (default: 4326)
- `--output-crs EPSG`: Set output CRS
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

- `--buffer-size`: Buffer size to apply (in CRS units)
- `--h3-res`: H3 resolution for polyfilling (0-15)
- `--h3-geom`: Include H3 geometries in output (default: True)
- `--input-crs`: Input CRS (default: 4326)
- `--output-crs`: Output CRS
- `--geometry-column`: Column name containing WKT geometry strings (for CSV/ORC files)
- `--mask`: Mask geometry (file path or WKT string)
- `--mask-crs`: CRS for mask geometry (default: 4326)
- `--head`: Show first n rows of the geometry file
- `--tail`: Show last n rows of the geometry file
- `--rows`: Number of rows to show for head/tail (default: 5)

### Examples

```bash
# Basic file conversion
geoterminal input.shp output.geojson

# Process a WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson

# Apply buffer and convert to H3 cells
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 6

# Convert WKT to H3 cells with geometries
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson --h3-res 6 --h3-geom

# Reproject data
geoterminal input.shp output.geojson --input-crs 4326 --output-crs 3857

# Clip geometries using a mask file
geoterminal input.shp output.geojson --mask mask.geojson --mask-crs 4326

# Clip geometries using a mask WKT
geoterminal input.shp output.geojson --mask "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"

# View first 10 rows of a file
geoterminal input.geojson --head --rows 10

# View last 8 rows of a file
geoterminal input.geojson --tail --rows 8

# Work with CSV/ORC files using custom geometry columns
geoterminal input.csv output.geojson --geometry-column my_wkt_column
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
