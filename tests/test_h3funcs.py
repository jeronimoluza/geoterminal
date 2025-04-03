"""Tests for the H3 operations module.

This module contains tests for H3 indexing and geometry operations.
"""

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Polygon

from geoterminal.h3_operations.h3_operations import (
    H3OperationError,
    H3Processor,
)


@pytest.fixture
def sample_hex_id() -> str:
    """Return a sample H3 hex ID at resolution 9 near the equator."""
    return "868389177ffffff"


@pytest.fixture
def sample_polygon_gdf() -> gpd.GeoDataFrame:
    """Create a sample GeoDataFrame with a simple polygon."""
    # Create a small polygon near the equator
    polygon = Polygon([(0, 0), (0.01, 0), (0.01, 0.01), (0, 0.01)])
    gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
    return gdf


def test_get_hex_geometry(sample_hex_id: str) -> None:
    """Test getting geometry from H3 hex ID."""
    geometry = H3Processor.get_hex_geometry(sample_hex_id)

    # Check if we got a valid polygon
    assert isinstance(geometry, Polygon)
    assert geometry.is_valid
    assert geometry.area > 0

    # Check if the polygon has the correct
    # number of vertices (H3 hexagons have 6 sides)
    exterior_coords = list(geometry.exterior.coords)
    assert len(exterior_coords) == 7  # 6 vertices + 1 closing point

    # Test invalid hex ID
    with pytest.raises(H3OperationError):
        H3Processor.get_hex_geometry("invalid_hex_id")


def test_polyfill_without_geometry(
    sample_polygon_gdf: gpd.GeoDataFrame,
) -> None:
    """Test H3 polyfill operation without including geometry."""
    processor = H3Processor(sample_polygon_gdf)
    resolution = 9
    result = processor.polyfill(resolution, include_geometry=False)

    # Check that we got a DataFrame
    # (not GeoDataFrame since include_geometry=False)
    assert isinstance(result, pd.DataFrame)
    assert "hex" in result.columns
    assert "geometry" not in result.columns

    # Check that we got some hexagons
    assert len(result) > 0

    # Check that all hex IDs are strings and valid H3 indexes
    for hex_id in result["hex"]:
        assert isinstance(hex_id, str)

    # Test invalid resolution
    with pytest.raises(H3OperationError):
        processor.polyfill(-1)
    with pytest.raises(H3OperationError):
        processor.polyfill(16)


def test_polyfill_with_geometry(sample_polygon_gdf: gpd.GeoDataFrame) -> None:
    """Test H3 polyfill operation with geometry included."""
    processor = H3Processor(sample_polygon_gdf)
    resolution = 9
    result = processor.polyfill(resolution, include_geometry=True)

    # Check that we got a GeoDataFrame
    assert isinstance(result, gpd.GeoDataFrame)
    assert "hex" in result.columns
    assert "geometry" in result.columns

    # Check that we got some hexagons
    assert len(result) > 0

    # Check that all geometries are valid polygons
    for geom in result["geometry"]:
        assert isinstance(geom, Polygon)
        assert geom.is_valid


def test_polyfill_with_invalid_geometry() -> None:
    """Test polyfill with an invalid geometry."""
    # Create an invalid polygon (self-intersecting)
    invalid_polygon = Polygon([(0, 0), (1, 1), (1, 0), (0, 1)])
    invalid_gdf = gpd.GeoDataFrame(geometry=[invalid_polygon], crs="EPSG:4326")

    processor = H3Processor(invalid_gdf)
    resolution = 9
    result = processor.polyfill(resolution)

    # Should return an empty DataFrame since the geometry is invalid
    assert len(result) == 0


def test_h3processor_validation() -> None:
    """Test H3Processor validation."""
    with pytest.raises(H3OperationError):
        # Should raise error for non-GeoDataFrame input
        H3Processor(pd.DataFrame())

    # Should work with None
    processor = H3Processor()
    assert processor.gdf is None
