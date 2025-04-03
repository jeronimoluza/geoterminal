# H3 Operations API

## H3Processor

The `H3Processor` class handles H3 grid operations.

### Constructor

```python
H3Processor(gdf: Optional[gpd.GeoDataFrame] = None)
```

**Parameters:**
- `gdf`: Optional GeoDataFrame to process. If None, can be set later.

### Methods

#### get_hex_geometry

```python
@staticmethod
def get_hex_geometry(hex_id: str) -> Polygon
```

Gets the geometry of an H3 hexagon.

**Parameters:**
- `hex_id`: H3 index as string

**Returns:**
- Shapely Polygon representing the H3 cell

**Raises:**
- `H3OperationError`: If hex_id is invalid

#### polyfill

```python
def polyfill(
    self,
    resolution: int,
    include_geometry: bool = True
) -> Union[gpd.GeoDataFrame, pd.DataFrame]
```

Fills polygons with H3 cells.

**Parameters:**
- `resolution`: H3 resolution (0-15)
- `include_geometry`: Whether to include hex geometries in output

**Returns:**
- GeoDataFrame with H3 cells if include_geometry=True
- DataFrame with only H3 indexes if include_geometry=False

**Raises:**
- `H3OperationError`: If polyfill operation fails

### Properties

#### gdf

```python
@property
def gdf(self) -> Optional[gpd.GeoDataFrame]
```

The current GeoDataFrame being processed.

### Exceptions

#### H3OperationError

```python
class H3OperationError(Exception)
```

Raised when an H3 operation fails. Includes detailed error message.

## Resolution Guidelines

H3 resolution levels and their approximate edge lengths:

| Resolution | Edge Length (km) | Use Case |
|------------|-----------------|-----------|
| 0          | 1107.71        | Continental |
| 1          | 418.68         | Continental |
| 2          | 158.24         | Countries |
| 3          | 59.81          | Regions |
| 4          | 22.61          | Metropolitan |
| 5          | 8.54           | Cities |
| 6          | 3.23           | Neighborhoods |
| 7          | 1.22           | Blocks |
| 8          | 0.46           | Buildings |
| 9          | 0.17           | Large venues |
| 10         | 0.07           | Buildings |
| 11-15      | < 0.07         | High precision |
