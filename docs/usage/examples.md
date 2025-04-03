# Usage Examples

## Basic Operations

### Clipping Geometries

```python
from geoterminal.geometry_operations import GeometryProcessor
from geoterminal.file_io import read_geometry_file

# Read input and mask
input_gdf = read_geometry_file("input.geojson")
mask_gdf = read_geometry_file("mask.geojson")

# Create processor and clip
processor = GeometryProcessor(input_gdf)
clipped = processor.clip(mask_gdf)

# Save result
clipped.to_file("output.geojson")
```

### Creating Buffers

```python
from geoterminal.geometry_operations import GeometryProcessor
from geoterminal.file_io import read_geometry_file

# Read input
gdf = read_geometry_file("input.geojson")

# Create buffer
processor = GeometryProcessor(gdf)
buffered = processor.apply_buffer(distance=1000)  # meters

# Save result
buffered.to_file("output.geojson")
```

## H3 Integration

### Converting to H3 Cells

```python
from geoterminal.h3_operations import H3Processor
from geoterminal.file_io import read_geometry_file

# Read input
gdf = read_geometry_file("input.geojson")

# Convert to H3 cells
processor = H3Processor(gdf)
h3_cells = processor.polyfill(resolution=9)

# Save with geometries
h3_cells.to_file("output.geojson")

# Save only H3 indexes
h3_cells[["hex"]].to_csv("output.csv")
```

### Working with H3 Geometries

```python
from geoterminal.h3_operations import H3Processor

# Get geometry for specific H3 index
hex_geom = H3Processor.get_hex_geometry("8928308280fffff")

# Convert multiple indexes to geometries
hex_ids = ["8928308280fffff", "8928308280bffff"]
geometries = [H3Processor.get_hex_geometry(h) for h in hex_ids]
```

## Advanced Usage

### Custom CRS Handling

```python
from geoterminal.geometry_operations import GeometryProcessor
from geoterminal.file_io import read_geometry_file

# Read with specific CRS
gdf = read_geometry_file("input.geojson", crs="EPSG:4326")

# Process
processor = GeometryProcessor(gdf)
result = processor.reproject("EPSG:3857")

# Save with new CRS
result.to_file("output.geojson")
```

### Error Handling

```python
from geoterminal.geometry_operations import GeometryProcessor, GeometryOperationError
from geoterminal.file_io import read_geometry_file, FileHandlerError

try:
    # Read input
    gdf = read_geometry_file("input.geojson")
    
    # Process
    processor = GeometryProcessor(gdf)
    result = processor.apply_buffer(distance=1000)
    
    # Save
    result.to_file("output.geojson")
except FileHandlerError as e:
    print(f"File error: {e}")
except GeometryOperationError as e:
    print(f"Geometry error: {e}")
```
