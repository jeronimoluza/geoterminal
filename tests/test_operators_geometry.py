"""Tests for the geometry operations module.

This module contains tests for geometry operations like buffering and
reprojection.
"""

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

from geoterminal.operators.geometry_operations import GeometryProcessor


@pytest.fixture
def sample_point_gdf() -> gpd.GeoDataFrame:
    """Create a sample GeoDataFrame with point geometry."""
    point = Point(0, 0)
    gdf = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")
    return gdf


@pytest.fixture
def sample_polygon_gdf() -> gpd.GeoDataFrame:
    """Create a sample GeoDataFrame with polygon geometry."""
    polygon1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    polygon2 = Polygon([(1, 0), (2, 0), (2, 1), (1, 1)])
    gdf = gpd.GeoDataFrame(geometry=[polygon1, polygon2], crs="EPSG:4326")
    return gdf


def test_apply_buffer_to_point(sample_point_gdf: gpd.GeoDataFrame) -> None:
    """Test buffer operation on a point geometry."""
    processor = GeometryProcessor(sample_point_gdf)
    buffer_size = 1.0
    buffered_gdf = processor.apply_buffer(buffer_size)

    # Check if the result is still a GeoDataFrame
    assert isinstance(buffered_gdf, gpd.GeoDataFrame)

    # Check if the buffer was applied correctly
    assert buffered_gdf.geometry.iloc[0].area > 0
    assert isinstance(buffered_gdf.geometry.iloc[0], Polygon)


def test_apply_buffer_to_polygon(sample_polygon_gdf: gpd.GeoDataFrame) -> None:
    """Test buffer operation on a polygon geometry."""
    processor = GeometryProcessor(sample_polygon_gdf)
    original_area = sample_polygon_gdf.geometry.iloc[0].area
    buffer_size = 0.5
    buffered_gdf = processor.apply_buffer(buffer_size)

    # Check if the buffered area is larger than the original
    assert buffered_gdf.geometry.iloc[0].area > original_area


def test_reproject_gdf(sample_point_gdf: gpd.GeoDataFrame) -> None:
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


def test_geometry_processor_validation() -> None:
    """Test GeometryProcessor validation."""
    with pytest.raises(Exception):
        # Should raise error for non-GeoDataFrame input
        GeometryProcessor(pd.DataFrame())

    # Should work with None
    processor = GeometryProcessor()
    assert processor.gdf is None


def test_unary_union(sample_polygon_gdf: gpd.GeoDataFrame) -> None:
    """Test unary union operation on multiple geometries."""
    processor = GeometryProcessor(sample_polygon_gdf)
    result = processor.unary_union()

    # Check if the result is a GeoDataFrame
    assert isinstance(result, gpd.GeoDataFrame)
    # Should have only one row after union
    assert len(result) == 1
    # Area should be equal to sum of original areas
    assert (
        abs(
            result.geometry.iloc[0].area
            - sum(sample_polygon_gdf.geometry.area)
        )
        < 1e-10
    )


def test_convex_hull(sample_polygon_gdf: gpd.GeoDataFrame) -> None:
    """Test convex hull operation on multiple geometries."""
    processor = GeometryProcessor(sample_polygon_gdf)
    result = processor.convex_hull()

    # Check if the result is a GeoDataFrame
    assert isinstance(result, gpd.GeoDataFrame)
    # Should have only one row after convex hull
    assert len(result) == 1
    # Convex hull area should be >= original area
    assert result.geometry.iloc[0].area >= sum(
        sample_polygon_gdf.geometry.area
    )


def test_centroid(sample_polygon_gdf: gpd.GeoDataFrame) -> None:
    """Test centroid operation on multiple geometries."""
    processor = GeometryProcessor(sample_polygon_gdf)
    result = processor.centroid()

    # Check if the result is a GeoDataFrame
    assert isinstance(result, gpd.GeoDataFrame)
    # Should have only one row for centroid
    assert len(result) == len(sample_polygon_gdf)
    # Result should be a Point
    assert isinstance(result.geometry.iloc[0], Point)
    # Centroid should be within the bounds of original geometries
    bounds = sample_polygon_gdf.total_bounds
    point = result.geometry.iloc[0]
    assert bounds[0] <= point.x <= bounds[2]  # within x bounds
    assert bounds[1] <= point.y <= bounds[3]  # within y bounds


def test_envelope(sample_polygon_gdf: gpd.GeoDataFrame) -> None:
    """Test envelope (bounding box) operation on multiple geometries."""
    processor = GeometryProcessor(sample_polygon_gdf)
    result = processor.envelope()

    # Check if the result is a GeoDataFrame
    assert isinstance(result, gpd.GeoDataFrame)
    # Should have only one row for envelope
    assert len(result) == 1
    # Result should be a Polygon
    assert isinstance(result.geometry.iloc[0], Polygon)
    # Envelope area should be >= sum of original areas
    assert result.geometry.iloc[0].area >= sum(
        sample_polygon_gdf.geometry.area
    )
    # Check if it's actually rectangular (4 vertices)
    assert (
        len(result.geometry.iloc[0].exterior.coords) == 5
    )  # 5 because first/last are same


def test_intersects_with_wkt(sample_polygon_gdf: gpd.GeoDataFrame) -> None:
    """Test intersects operation with WKT input."""
    processor = GeometryProcessor(sample_polygon_gdf)

    # Test with intersecting point
    point_wkt = "POINT(0.5 0.5)"  # Point inside first polygon
    result = processor.intersects(point_wkt)
    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1  # Should return one geometry

    # Test with non-intersecting point
    far_point = "POINT(10 10)"  # Point far from polygons
    result = processor.intersects(far_point)
    assert len(result) == 0  # Should return no geometries


def test_intersects_with_geodataframe(
    sample_polygon_gdf: gpd.GeoDataFrame,
) -> None:
    """Test intersects operation with GeoDataFrame input."""
    processor = GeometryProcessor(sample_polygon_gdf)

    # Create intersecting GeoDataFrame
    point = Point(0.5, 0.5)  # Point inside first polygon
    intersecting_gdf = gpd.GeoDataFrame(
        geometry=[point], crs=sample_polygon_gdf.crs
    )

    result = processor.intersects(intersecting_gdf)
    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1  # Should return one geometry

    # Test with non-intersecting GeoDataFrame
    far_point = Point(10, 10)  # Point far from polygons
    non_intersecting_gdf = gpd.GeoDataFrame(
        geometry=[far_point], crs=sample_polygon_gdf.crs
    )
    result = processor.intersects(non_intersecting_gdf)
    assert len(result) == 0  # Should return no geometries


def test_intersects_error_handling(
    sample_polygon_gdf: gpd.GeoDataFrame,
) -> None:
    """Test error handling in intersects operation."""
    processor = GeometryProcessor(sample_polygon_gdf)

    # Test with invalid WKT
    with pytest.raises(Exception):
        processor.intersects("INVALID WKT")

    # Test with GeoDataFrame having no CRS
    no_crs_gdf = gpd.GeoDataFrame(geometry=[Point(0, 0)])
    with pytest.raises(Exception):
        processor.intersects(no_crs_gdf)


def test_simplify(sample_point_gdf: gpd.GeoDataFrame) -> None:
    """Test simplify operation on polygon geometries."""
    # Create a point and buffer it to create a complex circular polygon
    point = Point(0, 0)
    point_gdf = gpd.GeoDataFrame(
        geometry=[point], crs="EPSG:4326"
    )  # Use projected CRS for meters
    processor = GeometryProcessor(point_gdf)

    # Buffer by 1000 meters to create a circle with many vertices
    buffered = processor.apply_buffer(10)
    original_vertices = len(buffered.unary_union.exterior.coords)

    # Test with reasonable tolerance
    processor = GeometryProcessor(buffered)
    result = processor.simplify(tolerance=2)
    print(buffered)
    print(result)
    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1  # Should maintain number of geometries
    assert (
        len(result.geometry.iloc[0].exterior.coords) < original_vertices
    )  # Should have fewer vertices


def test_simplify_error_handling() -> None:
    """Test error handling in simplify operation."""
    processor = GeometryProcessor()

    # Test with no GeoDataFrame set
    with pytest.raises(Exception):
        processor.simplify(0.1)

    # Test with negative tolerance (should raise error)
    processor = GeometryProcessor(
        gpd.GeoDataFrame(
            geometry=[Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])],
            crs="EPSG:4326",
        )
    )
    with pytest.raises(Exception):
        processor.simplify(-0.1)  # Should raise error
