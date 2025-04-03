import pytest
import geopandas as gpd
from shapely.geometry import Point, Polygon
from geoterminal.geometry_operations.geometry_operations import GeometryProcessor

@pytest.fixture
def sample_point_gdf():
    """Create a sample GeoDataFrame with point geometry."""
    point = Point(0, 0)
    gdf = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")
    return gdf

@pytest.fixture
def sample_polygon_gdf():
    """Create a sample GeoDataFrame with polygon geometry."""
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
    return gdf

def test_apply_buffer_to_point(sample_point_gdf):
    """Test buffer operation on a point geometry."""
    processor = GeometryProcessor(sample_point_gdf)
    buffer_size = 1.0
    buffered_gdf = processor.apply_buffer(buffer_size)
    
    # Check if the result is still a GeoDataFrame
    assert isinstance(buffered_gdf, gpd.GeoDataFrame)
    
    # Check if the buffer was applied correctly
    assert buffered_gdf.geometry.iloc[0].area > 0
    assert isinstance(buffered_gdf.geometry.iloc[0], Polygon)

def test_apply_buffer_to_polygon(sample_polygon_gdf):
    """Test buffer operation on a polygon geometry."""
    processor = GeometryProcessor(sample_polygon_gdf)
    original_area = sample_polygon_gdf.geometry.iloc[0].area
    buffer_size = 0.5
    buffered_gdf = processor.apply_buffer(buffer_size)
    
    # Check if the buffered area is larger than the original
    assert buffered_gdf.geometry.iloc[0].area > original_area

def test_reproject_gdf(sample_point_gdf):
    """Test reprojection of GeoDataFrame."""
    processor = GeometryProcessor(sample_point_gdf)
    target_crs = "EPSG:3857"  # Web Mercator projection
    reprojected_gdf = processor.reproject(target_crs)
    
    # Check if the CRS was changed
    assert reprojected_gdf.crs == target_crs
    assert reprojected_gdf.crs != sample_point_gdf.crs
    
    # Check if the data structure remains intact
    assert isinstance(reprojected_gdf, gpd.GeoDataFrame)
    assert len(reprojected_gdf) == len(sample_point_gdf)

def test_geometry_processor_validation():
    """Test GeometryProcessor validation."""
    with pytest.raises(Exception):
        # Should raise error for non-GeoDataFrame input
        GeometryProcessor(pd.DataFrame())
    
    # Should work with None
    processor = GeometryProcessor()
    assert processor.gdf is None
