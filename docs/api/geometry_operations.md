# Geometry Operations API

Module: `geoterminal.operators.geometry_operations`

## Classes

### GeometryProcessor

Handles geometry operations on GeoDataFrames.

```python
class GeometryProcessor:
    def __init__(self, gdf: Optional[gpd.GeoDataFrame] = None)
    def apply_buffer(self, size: float) -> None
    def clip(self, mask_gdf: gpd.GeoDataFrame) -> None
    def reproject(self, target_crs: int) -> None
    def unary_union(self) -> None
    def convex_hull(self) -> None
    def centroid(self) -> None
    def envelope(self) -> None
    def intersects(self, other: Union[str, gpd.GeoDataFrame]) -> None
    def simplify(self, tolerance: float) -> None
```

#### Methods

Basic Operations:
- `apply_buffer`: Apply a buffer of specified size in meters
- `clip`: Clip geometries using a mask GeoDataFrame
- `reproject`: Reproject geometries to target CRS

Advanced Operations:
- `unary_union`: Merge all geometries into one
- `convex_hull`: Create convex hull of geometries
- `centroid`: Calculate centroid of geometries
- `envelope`: Get bounding box of geometries
- `intersects`: Filter geometries that intersect with another geometry
- `simplify`: Simplify geometries using Douglas-Peucker algorithm

## Exceptions

### GeometryOperationError

Raised when geometry operations fail.

## GeometryProcessor

The `GeometryProcessor` class is the main interface for geometric operations.

### Constructor

```python
GeometryProcessor(gdf: Optional[gpd.GeoDataFrame] = None)
```

**Parameters:**

- `gdf`: Optional GeoDataFrame to process. If None, can be set later.

### Methods

#### apply_buffer

```python
def apply_buffer(self, distance: float) -> gpd.GeoDataFrame
```

Creates a buffer around geometries.

**Parameters:**

- `distance`: Buffer distance in the units of the GeoDataFrame's CRS

**Returns:**

- GeoDataFrame with buffered geometries

**Raises:**
- `GeometryOperationError`: If buffer operation fails

#### unary_union

```python
def unary_union(self) -> gpd.GeoDataFrame
```

Merges all geometries into a single geometry.

**Returns:**

- GeoDataFrame with a single merged geometry

**Raises:**
- `GeometryOperationError`: If union operation fails

#### convex_hull

```python
def convex_hull(self) -> gpd.GeoDataFrame
```

Creates a convex hull containing all geometries.

**Returns:**

- GeoDataFrame with convex hull geometry

**Raises:**
- `GeometryOperationError`: If convex hull operation fails

#### centroid

```python
def centroid(self) -> gpd.GeoDataFrame
```

Calculates the centroid of each geometry.

**Returns:**

- GeoDataFrame with centroid points

**Raises:**
- `GeometryOperationError`: If centroid calculation fails

#### envelope

```python
def envelope(self) -> gpd.GeoDataFrame
```

Creates a bounding box (envelope) for each geometry.

**Returns:**

- GeoDataFrame with envelope polygons

**Raises:**
- `GeometryOperationError`: If envelope operation fails

#### intersects

```python
def intersects(self, other: Union[str, gpd.GeoDataFrame]) -> gpd.GeoDataFrame
```

Filters geometries that intersect with another geometry.

**Parameters:**

- `other`: WKT string or GeoDataFrame to test intersection against

**Returns:**

- GeoDataFrame with geometries that intersect with the input

**Raises:**
- `GeometryOperationError`: If intersection operation fails

#### simplify

```python
def simplify(self, tolerance: float) -> gpd.GeoDataFrame
```

Simplify geometries using Douglas-Peucker algorithm.

**Parameters:**

- `tolerance`: Maximum allowed deviation from original geometry.
              Should be in the same units as the geometry's coordinates.

**Returns:**

- GeoDataFrame with simplified geometries

**Raises:**
- `GeometryOperationError`: If simplification fails

#### clip

```python
def clip(self, mask: Union[gpd.GeoDataFrame, Polygon]) -> gpd.GeoDataFrame
```

Clips geometries using a mask.

**Parameters:**

- `mask`: GeoDataFrame or Polygon to use as clip mask

**Returns:**

- GeoDataFrame with clipped geometries

**Raises:**

- `GeometryOperationError`: If clip operation fails

#### reproject

```python
def reproject(self, target_crs: Union[str, int]) -> gpd.GeoDataFrame
```

Reprojects the GeoDataFrame to a new CRS.

**Parameters:**

- `target_crs`: Target CRS as EPSG code or string

**Returns:**

- Reprojected GeoDataFrame

**Raises:**

- `GeometryOperationError`: If reprojection fails

### Properties

#### gdf

```python
@property
def gdf(self) -> Optional[gpd.GeoDataFrame]
```

The current GeoDataFrame being processed.

#### crs

```python
@property
def crs(self) -> Optional[str]
```

The CRS of the current GeoDataFrame.

### Exceptions

#### GeometryOperationError

```python
class GeometryOperationError(Exception)
```

Raised when a geometry operation fails. Includes detailed error message.
