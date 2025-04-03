# Geometry Operations API

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
