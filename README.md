# Geoterminal

Geoterminal is a command line interface (CLI) made in Python, and designed to automate common operations in the field of Geographic Information Systems (GIS) data development. As a GIS Data Developer, you often find yourself performing tasks like data transformation, geometry loading, and format conversion. Geoterminal streamlines these processes, allowing you to focus on higher-level tasks rather than repetitive operations.

## Main Features

- **File Conversion**: Convert files from and to different formats, such as CSV, ORC, GeoJSON and Shapefiles.
- **WKT Dumping**: Converts a Well-Known Text (WKT) representation of a geometry to any of the mentioned file formats.
- **H3 Hexagon Transformation**: Converts geometries to Uber's H3 cells in the desired resolution.
- **Geospatial Data Conversion**: Convert geospatial data between different CRSs.
- **H3 Hexagonal Grid Resolution**: Apply H3 hexagonal grid resolutions to the converted data.
- **Geometry Inclusion**: Optionally include H3 geometries in the output.
- **Buffering Support**: Apply a buffer distance to the data during conversion.

## Installation

To get started with Geoterminal, follow these steps:

1. Clone the repository:

   ```bash
   git clone <repository_url>
   ```

2. Install the required dependencies. Ensure you have Python 3.9 or later installed.

   ```bash
   pip install geopandas fire
   ```

# Usage

Geoterminal offers a variety of functionalities through its command-line interface. Here are some examples of how to use its features:

## Command Structure

- `input`: Path to the input geospatial file.
- `output`: Path where the converted data should be saved.
- `--h3_res`: H3 hexagon resolution to convert to.
- `--h3_geom`: Whether to include the H3 geometry or not.
- `--input_crs`: Input file projection (EPSG code).
- `--output_crs`: Output file projection (EPSG code).
- `--buffer_size`: Buffer distance to apply.

### Basic Conversion

To perform a basic conversion between file formats:

```bash
geoterminal input.csv output.geojson
```

### Basic Reprojection

Perform reprojections using the following command:

```bash
geoterminal input.geojson output.geojson --input_crs EPSG:4326 --output_crs EPSG:3857
```

This command converts data from WGS84 (EPSG:4326) to Web Mercator (EPSG:3857).

### Conversion With H3 Resolution Specification

To convert data and apply an H3 resolution, specify the `--h3_res` option followed by the desired resolution level:

```bash
geoterminal input.geojson output.h3 --input_crs EPSG:4326 --output_crs EPSG:3857 --h3_res=9
```

This example converts the data to an H3 index at resolution level 9.

### Including H3 Geometry

To include H3 geometries in the output, set the `--h3_geom` option to `True`:

```bash
geoterminal input.geojson output_with_geometry.h3 --input_crs EPSG:4326 --output_crs EPSG:3857 --h3_res=9 --h3_geom=True
```

This command converts the data to an H3 index at resolution level 9 and includes the H3 geometries in the output file.

### Applying Buffer Distance

To apply a buffer distance to the data during conversion, use the `--buffer_size` option followed by the desired buffer distance in meters:

```bash
geoterminal input.geojson output_buffered.geojson --input_crs EPSG:4326 --output_crs EPSG:3857 --buffer_size=1000
```

This example applies a 1000-meter buffer to the data during conversion.

## Contribution

Contributions to Geoterminal are welcome! If you have any ideas for new features, improvements, or bug fixes, feel free to submit a pull request.

## License

Geoterminal is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
