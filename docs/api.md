# API Reference

## Geometry Operations

### GeometryProcessor

The `GeometryProcessor` class provides methods for geometric operations on GeoDataFrames.

```python
from geoterminal.geometry_operations import GeometryProcessor
```

#### Constructor

```python
GeometryProcessor(gdf: Optional[gpd.GeoDataFrame] = None)
```

- `gdf`: Optional GeoDataFrame to process

#### Methods

##### apply_buffer
```python
def apply_buffer(self, distance: float) -> gpd.GeoDataFrame
```
Creates a buffer around geometries.
- `distance`: Buffer distance in the units of the GeoDataFrame's CRS

##### reproject
```python
def reproject(self, target_crs: Union[str, int]) -> gpd.GeoDataFrame
```
Reprojects the GeoDataFrame to a new CRS.
- `target_crs`: Target CRS as EPSG code or string

## H3 Operations

### H3Processor

The `H3Processor` class handles H3 grid operations.

```python
from geoterminal.h3_operations import H3Processor
```

#### Constructor

```python
H3Processor(gdf: Optional[gpd.GeoDataFrame] = None)
```

- `gdf`: Optional GeoDataFrame to process

#### Methods

##### get_hex_geometry
```python
@staticmethod
def get_hex_geometry(hex_id: str) -> Polygon
```
Gets the geometry of an H3 hexagon.

- `hex_id`: H3 index as string

##### polyfill
```python
def polyfill(self, resolution: int, include_geometry: bool = True) -> Union[gpd.GeoDataFrame, pd.DataFrame]
```
Fills polygons with H3 cells.

- `resolution`: H3 resolution (0-15)
- `include_geometry`: Whether to include hex geometries in output

## File I/O

### Functions

#### read_geometry_file
```python
def read_geometry_file(file_path: Union[str, Path], crs: Optional[int] = None) -> gpd.GeoDataFrame
```
Reads geometry from file or WKT string.

- `file_path`: Path to file or WKT string
- `crs`: CRS for WKT input

#### export_data
```python
def export_data(data: Union[gpd.GeoDataFrame, pd.DataFrame], output_path: Union[str, Path]) -> None
```
Exports data to file.

- `data`: Data to export
- `output_path`: Output file path

## Exceptions

### GeometryOperationError
Raised when geometry operations fail.

### H3OperationError
Raised when H3 operations fail.

### FileHandlerError
Raised when file operations fail.
