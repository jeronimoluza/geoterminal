# Command Reference

## Global Options

- `--verbose`: Enable verbose logging
- `--version`: Show version information
- `--help`: Show help message

## Core Commands

### clip

Clips geometries using a mask file or WKT string.

```bash
geoterminal clip INPUT MASK OUTPUT [OPTIONS]
```

#### Options
- `--input-crs`: Input CRS (default: read from file)
- `--mask-crs`: Mask CRS (required for WKT)
- `--output-crs`: Output CRS

#### Examples
```bash
# Using mask file
geoterminal clip input.geojson mask.geojson output.geojson

# Using WKT string
geoterminal clip input.geojson "POLYGON((...))" output.geojson --mask-crs EPSG:4326
```

### buffer

Creates a buffer around geometries.

```bash
geoterminal buffer INPUT OUTPUT [OPTIONS]
```

#### Options
- `--distance`: Buffer distance (required)
- `--input-crs`: Input CRS
- `--output-crs`: Output CRS

#### Examples
```bash
geoterminal buffer input.geojson output.geojson --distance 1000
```

### h3

Converts geometries to H3 cells.

```bash
geoterminal h3 INPUT OUTPUT [OPTIONS]
```

#### Options
- `--resolution`: H3 resolution (0-15)
- `--include-geometry`: Include hex geometries
- `--input-crs`: Input CRS

#### Examples
```bash
geoterminal h3 input.geojson output.geojson --resolution 9
```

## Error Codes

- 1: Invalid arguments
- 2: File operation error
- 3: Geometry operation error
- 4: H3 operation error
