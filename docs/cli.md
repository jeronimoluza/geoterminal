# Command Line Interface (CLI)

Geoterminal provides a command-line interface for common geospatial operations. It accepts both file paths and WKT strings as input.

## Basic Usage

```bash
geoterminal INPUT OUTPUT [OPTIONS]
```

### Arguments
- `INPUT`: Input geometry (file path or WKT string)
- `OUTPUT`: Output file path

### Options
- `--buffer-size`: Buffer size to apply (in CRS units)
- `--h3-res`: H3 resolution for polyfilling (0-15)
- `--h3-geom`: Include H3 geometries in output
- `--input-crs`: Input CRS (default: 4326)
- `--output-crs`: Output CRS
- `--geometry-column`: Column name containing WKT geometry strings (for CSV/ORC files)

### Examples
```bash
# Process a file
geoterminal input.shp output.geojson

# Process a WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson

# Apply buffer and convert to H3
geoterminal input.shp output.geojson --buffer-size 1000 --h3-res 6

# Convert WKT to H3 with geometries
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson --h3-res 6 --h3-geom
```

## Additional Commands

### head

Displays the first n rows of a geometry file.

```bash
geoterminal head INPUT [-n ROWS] [OPTIONS]
```

#### Arguments
- `INPUT`: Input file path (GeoJSON, Shapefile, CSV)

#### Options
- `-n, --rows`: Number of rows to display (default: 5)
- `--input-crs`: CRS of input file (default: 4326)

#### Examples
```bash
# Show first 5 rows
geoterminal head input.geojson

# Show first 10 rows
geoterminal head -n 10 input.geojson
```

### tail

Displays the last n rows of a geometry file.

```bash
geoterminal tail INPUT [-n ROWS] [OPTIONS]
```

#### Arguments

- `INPUT`: Input file path (GeoJSON, Shapefile, CSV)

#### Options

- `-n, --rows`: Number of rows to display (default: 5)
- `--input-crs`: CRS of input file (default: 4326)

#### Examples

```bash
# Show last 5 rows
geoterminal tail input.geojson

# Show last 8 rows
geoterminal tail -n 8 input.geojson
```

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
geoterminal clip input.shp mask.geojson output.csv

# Clip using WKT string
geoterminal clip input.geojson "POLYGON((...))" output.csv --mask-crs EPSG:4326
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
- `.orc`: ORC format with WKT geometry column

For CSV and ORC files, you can specify which column contains the WKT geometry strings using `--geometry-column`. If not specified, the tool will look for standard column names (geometry, geom, wkt, the_geom).

```bash
# Use custom geometry column
geoterminal input.csv output.geojson --geometry-column my_wkt_column
geoterminal input.orc output.geojson --geometry-column my_wkt_column
```
