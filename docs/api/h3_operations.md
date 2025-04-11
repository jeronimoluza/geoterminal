# H3 Operations API

Module: `geoterminal.operators.h3_operations`

## Functions

### polyfill

```python
def polyfill(gdf: gpd.GeoDataFrame, resolution: int) -> gpd.GeoDataFrame
```

Convert geometries to H3 hexagons at specified resolution.

## Classes

### H3Processor

Handles H3 grid operations on GeoDataFrames.

```python
class H3Processor:
    def __init__(self, gdf: Optional[gpd.GeoDataFrame] = None)
    def polyfill(self, resolution: int) -> gpd.GeoDataFrame
    def get_hex_geometry(self, h3_address: str) -> Polygon
```

#### Methods

- `polyfill`: Convert geometries to H3 hexagons
- `get_hex_geometry`: Get polygon geometry for H3 address

## Exceptions

### H3OperationError

Raised when H3 operations fail.

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
    resolution: int
) -> gpd.GeoDataFrame
```

Fills polygons with H3 cells. Always includes hexagon geometries.

**Parameters:**

- `resolution`: H3 resolution (0-15)

**Returns:**

- GeoDataFrame with H3 cells including hexagon geometries

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
