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

### Examples
```bash
# Process a file
geoterminal input.geojson output.geojson

# Process a WKT string
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson

# Apply buffer and convert to H3
geoterminal input.geojson output.geojson --buffer-size 1000 --h3-res 9

# Convert WKT to H3 with geometries
geoterminal "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))" output.geojson --h3-res 9 --h3-geom
```

## Additional Commands

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
