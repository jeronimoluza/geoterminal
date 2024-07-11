# Geoterminal

Geoterminal is a command line interface (CLI) made in Python, and designed to automate common operations in the field of Geographic Information Systems (GIS) data development. As a GIS Data Developer, you often find yourself performing tasks like data transformation, geometry loading, and format conversion. Geoterminal streamlines these processes, allowing you to focus on higher-level tasks rather than repetitive operations.

## Main Features

- **File Conversion**: Convert files from and to different formats, such as CSV, ORC, GeoJSON and Shapefiles.
- **WKT Dumping**: Converts a Well-Known Text (WKT) representation of a geometry to any of the mentioned file formats.
- **H3 Hexagon Transformation**: Converts geometries to Uber's H3 cells in the desired resolution.

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

## Usage

Geoterminal offers a variety of functionalities through its command-line interface. Here are some examples of how to use its features:

### CSV to GeoJSON Conversion

Convert a CSV file containing geographical data into a GeoJSON file:

```bash
geoterminal convert somefile.csv convertedfile.geojson
```

## Contribution

Contributions to Geoterminal are welcome! If you have any ideas for new features, improvements, or bug fixes, feel free to submit a pull request.

## License

Geoterminal is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

