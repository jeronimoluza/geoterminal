# File I/O API

Module: `geoterminal.io.file`

## Functions

### read_geometry_file

```python
def read_geometry_file(input_path: Union[str, Path], crs: Optional[int] = None, geometry_column: Optional[str] = None) -> gpd.GeoDataFrame
```

Read geometry data from various file formats or WKT string.

### export_data

```python
def export_data(gdf: gpd.GeoDataFrame, output_file: Union[str, Path]) -> None
```

Export GeoDataFrame to various file formats.

### Supported Formats

- GeoJSON (.geojson, .json)
- Shapefile (.shp)
- CSV (.csv) with WKT geometry
- ORC (.orc)

## Exceptions

### FileHandlerError

Raised when file operations fail.

## Functions

### read_geometry_file

```python
def read_geometry_file(
    file_path: Union[str, Path],
    crs: Optional[int] = None,
    geometry_column: Optional[str] = None
) -> gpd.GeoDataFrame
```

Reads geometry from file or WKT string.

**Parameters:**

- `file_path`: Path to file or WKT string
- `crs`: CRS for WKT input (required for WKT)
- `geometry_column`: Column name containing WKT geometry strings (for CSV/ORC files)

**Returns:**

- GeoDataFrame containing the geometries

**Raises:**

- `FileHandlerError`: If file reading fails

**Supported Formats:**

- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV with WKT column
- ORC with WKT column
- WKT string

### export_data

```python
def export_data(
    data: Union[gpd.GeoDataFrame, pd.DataFrame],
    output_path: Union[str, Path]
) -> None
```

Exports data to file.

**Parameters:**

- `data`: Data to export (GeoDataFrame or DataFrame)
- `output_path`: Output file path

**Raises:**

- `FileHandlerError`: If export fails

**Supported Formats:**

- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV (.csv) with WKT geometry
- ORC (.orc) with WKT geometry
- WKT (.wkt) - Single geometry or GEOMETRYCOLLECTION

## Exceptions

### FileHandlerError

```python
class FileHandlerError(Exception)
```

Raised when file operations fail. Includes detailed error message.

## Examples

### Reading Files

```python
from geoterminal.file_io import read_geometry_file

# Read GeoJSON
gdf = read_geometry_file("input.geojson")

# Read WKT with CRS
wkt = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
gdf = read_geometry_file(wkt, crs="EPSG:4326")

# Read CSV/ORC with custom geometry column
gdf = read_geometry_file("input.csv", geometry_column="my_wkt_column")
gdf = read_geometry_file("input.orc", geometry_column="my_wkt_column")
```

### Exporting Files

```python
from geoterminal.file_io import export_data

# Export to GeoJSON
export_data(gdf, "output.geojson")

# Export to CSV with WKT geometry
export_data(gdf, "output.csv")

# Export to WKT
export_data(gdf, "output.wkt")  # Single geometry or GEOMETRYCOLLECTION
```
