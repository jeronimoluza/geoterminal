import pytest
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from src.h3_operations.h3_operations import get_hex_geometry, polyfill

@pytest.fixture
def sample_hex_id():
    """Return a sample H3 hex ID at resolution 9 near the equator."""
    return "868389177ffffff"

@pytest.fixture
def sample_polygon_gdf():
    """Create a sample GeoDataFrame with a simple polygon."""
    # Create a small polygon near the equator
    polygon = Polygon([(0, 0), (0.01, 0), (0.01, 0.01), (0, 0.01)])
    gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
    return gdf

def test_get_hex_geometry(sample_hex_id):
    """Test getting geometry from H3 hex ID."""
    geometry = get_hex_geometry(sample_hex_id)
    
    # Check if we got a valid polygon
    assert isinstance(geometry, Polygon)
    assert geometry.is_valid
    assert geometry.area > 0
    
    # Check if the polygon has the correct number of vertices (H3 hexagons have 6 sides)
    exterior_coords = list(geometry.exterior.coords)
    assert len(exterior_coords) == 7  # 6 vertices + 1 closing point

def test_polyfill_without_geometry(sample_polygon_gdf):
    """Test H3 polyfill operation without including geometry."""
    resolution = 9
    result = polyfill(sample_polygon_gdf, resolution, include_geometry=False)
    
    # Check that we got a DataFrame (not GeoDataFrame since include_geometry=False)
    assert isinstance(result, pd.DataFrame)
    assert 'hex' in result.columns
    assert 'geometry' not in result.columns
    
    # Check that we got some hexagons
    assert len(result) > 0
    
    # Check that all hex IDs are strings and valid H3 indexes
    for hex_id in result['hex']:
        assert isinstance(hex_id, str)

def test_polyfill_with_geometry(sample_polygon_gdf):
    """Test H3 polyfill operation with geometry included."""
    resolution = 9
    result = polyfill(sample_polygon_gdf, resolution, include_geometry=True)
    
    # Check that we got a GeoDataFrame
    assert isinstance(result, gpd.GeoDataFrame)
    assert 'hex' in result.columns
    assert 'geometry' in result.columns
    
    # Check that we got some hexagons
    assert len(result) > 0
    
    # Check that all geometries are valid polygons
    for geom in result['geometry']:
        assert isinstance(geom, Polygon)
        assert geom.is_valid

def test_polyfill_with_invalid_geometry():
    """Test polyfill with an invalid geometry."""
    # Create an invalid polygon (self-intersecting)
    invalid_polygon = Polygon([(0, 0), (1, 1), (1, 0), (0, 1)])
    invalid_gdf = gpd.GeoDataFrame(geometry=[invalid_polygon], crs="EPSG:4326")
    
    resolution = 9
    result = polyfill(invalid_gdf, resolution)
    
    # Should return an empty DataFrame since the geometry is invalid
    assert len(result) == 0
