# Geoterminal

Geoterminal is a Python tool designed to automate common operations in the field of Geographic Information Systems (GIS) data development. As a GIS Data Developer, you often find yourself performing tasks like data transformation, geometry loading, and format conversion. Geoterminal streamlines these processes, allowing you to focus on higher-level tasks rather than repetitive operations.

## Features

- **CSV to GeoJSON Conversion:** Geoterminal provides a convenient method for converting CSV files containing geographical data into GeoJSON format. This is particularly useful when you need to visualize or work with geographic data in various mapping tools.

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

### Hello Command

Print a greeting message:

```bash
python run.py hello --name <your_name>
```

### CSV to GeoJSON Conversion

Convert a CSV file containing geographical data into a GeoJSON file:

```bash
python run.py csv_to_geojson --path <csv_file_path> --outfile <output_geojson_file>
```

## Customization

Geoterminal is designed with extensibility in mind. You can easily add more functionalities by creating new methods within the `TerminalTool` class defined in `run.py`.

## Example Scripts

### `file1.py`

This script showcases how to use Geoterminal's features:

- Importing the necessary modules
- Creating an instance of the `TerminalTool` class
- Using the `fire.Fire()` command to enable command-line execution

### `file2.py`

This script demonstrates the implementation of loading geometries from a CSV file using Geoterminal:

- Reading a CSV file using `pandas`
- Loading geometries using the `load_geometries` function
- Converting the data to a `GeoDataFrame` and saving it to a GeoJSON file

### `utils.py`

This script contains utility functions for handling geometry data:

- The `load_wkt` function converts a Well-Known Text (WKT) string into a Shapely geometry object.

## Contribution

Contributions to Geoterminal are welcome! If you have any ideas for new features, improvements, or bug fixes, feel free to submit a pull request.

## License

Geoterminal is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

