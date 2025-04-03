# File I/O API

## Functions

### read_geometry_file

```python
def read_geometry_file(
    file_path: Union[str, Path],
    crs: Optional[int] = None
) -> gpd.GeoDataFrame
```

Reads geometry from file or WKT string.

**Parameters:**
- `file_path`: Path to file or WKT string
- `crs`: CRS for WKT input (required for WKT)

**Returns:**
- GeoDataFrame containing the geometries

**Raises:**
- `FileHandlerError`: If file reading fails

**Supported Formats:**
- GeoJSON (.geojson)
- Shapefile (.shp)
- CSV with WKT column
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
- CSV (.csv)

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
```

### Exporting Files

```python
from geoterminal.file_io import export_data

# Export to GeoJSON
export_data(gdf, "output.geojson")

# Export to CSV
export_data(df, "output.csv")
```
