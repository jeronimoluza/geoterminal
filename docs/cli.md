# Command Line Interface (CLI)

Geoterminal provides a command-line interface for common geospatial operations.

## Global Options

- `--verbose`: Enable verbose logging
- `--version`: Show version information

## Commands

### clip

Clips geometries using a mask.

```bash
geoterminal clip INPUT MASK OUTPUT [OPTIONS]
```

#### Arguments
- `INPUT`: Input file path (GeoJSON, Shapefile, CSV)
- `MASK`: Mask file path or WKT string
- `OUTPUT`: Output file path

#### Options
- `--input-crs`: CRS of input file (default: read from file)
- `--mask-crs`: CRS of mask geometry (required for WKT input)
- `--output-crs`: CRS of output file (default: same as input)

#### Examples
```bash
# Clip using mask file
geoterminal clip input.geojson mask.geojson output.geojson

# Clip using WKT string
geoterminal clip input.geojson "POLYGON((...))" output.geojson --mask-crs EPSG:4326
```

### buffer

Creates a buffer around geometries.

```bash
geoterminal buffer INPUT OUTPUT [OPTIONS]
```

#### Arguments
- `INPUT`: Input file path
- `OUTPUT`: Output file path

#### Options
- `--distance`: Buffer distance in CRS units (required)
- `--input-crs`: CRS of input file (default: read from file)
- `--output-crs`: CRS of output file (default: same as input)

#### Examples
```bash
# Create 1km buffer
geoterminal buffer input.geojson output.geojson --distance 1000
```

### h3

Performs H3 grid operations.

```bash
geoterminal h3 INPUT OUTPUT [OPTIONS]
```

#### Arguments
- `INPUT`: Input file path
- `OUTPUT`: Output file path

#### Options
- `--resolution`: H3 resolution (0-15, required)
- `--include-geometry`: Include hex geometries in output (default: true)
- `--input-crs`: CRS of input file (default: read from file)

#### Examples
```bash
# Convert to H3 cells at resolution 9
geoterminal h3 input.geojson output.geojson --resolution 9

# Get only H3 indexes
geoterminal h3 input.geojson output.csv --resolution 9 --include-geometry false
```

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

## Output Formats

The output format is determined by the file extension:
- `.geojson`: GeoJSON format
- `.shp`: Shapefile format
- `.csv`: CSV format with WKT geometry column
