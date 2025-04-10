"""Test operation order in geoterminal."""

import os
import tempfile
from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from geoterminal.cli.processor import process_geometries
from geoterminal.operators.geometry_operations import GeometryProcessor


@pytest.fixture
def sample_gdf():
    """Create a sample GeoDataFrame for testing."""
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    return gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")


@pytest.fixture
def temp_files():
    """Create temporary files for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.geojson"
        output1 = Path(tmpdir) / "output1.geojson"
        output2 = Path(tmpdir) / "output2.geojson"
        output3 = Path(tmpdir) / "output3.geojson"
        yield input_file, output1, output2, output3


def test_operation_order(sample_gdf, temp_files):
    """Test that operation order produces the same results when split into steps."""
    input_file, output1, output2, output3 = temp_files
    
    # Save input file
    sample_gdf.to_file(input_file, driver="GeoJSON")

    # Create mock args for different operation orders
    class MockArgs:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    # Test case 1: All operations in one command
    args1 = MockArgs(
        input=str(input_file),
        output=str(output1),
        buffer_size=10,
        h3_res=4,
        h3_geom=True,
        input_crs=4326,
        output_crs=None,
        mask=None,
        mask_crs=4326
    )
    
    # Process with all operations
    processor1 = GeometryProcessor(sample_gdf.copy())
    process_geometries(processor1, args1)
    result1 = processor1.gdf
    result1.to_file(output1, driver="GeoJSON")

    # Test case 2: Split operations into steps
    # Step 1: Apply buffer
    args2_buffer = MockArgs(
        input=str(input_file),
        output=str(output2),
        buffer_size=10,
        h3_res=None,
        h3_geom=True,
        input_crs=4326,
        output_crs=None,
        mask=None,
        mask_crs=4326
    )
    
    processor2 = GeometryProcessor(sample_gdf.copy())
    process_geometries(processor2, args2_buffer)
    processor2.gdf.to_file(output2, driver="GeoJSON")

    # Step 2: Apply H3 to buffered result
    buffered_gdf = gpd.read_file(output2)
    processor3 = GeometryProcessor(buffered_gdf)
    args2_h3 = MockArgs(
        input=str(output2),
        output=str(output3),
        buffer_size=None,
        h3_res=4,
        h3_geom=True,
        input_crs=4326,
        output_crs=None,
        mask=None,
        mask_crs=4326
    )
    
    process_geometries(processor3, args2_h3)
    result2 = processor3.gdf
    result2.to_file(output3, driver="GeoJSON")

    # Compare results
    final1 = gpd.read_file(output1)
    final2 = gpd.read_file(output3)

    # Compare geometries
    assert len(final1) == len(final2), "Different number of features"
    for geom1, geom2 in zip(final1.geometry, final2.geometry):
        assert geom1.equals(geom2), "Geometries are different"
