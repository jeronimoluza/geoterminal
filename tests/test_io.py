"""Tests for the file I/O operations module.

This module contains tests for reading and writing geospatial data in
various formats.
"""

import tempfile
from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import Point, Polygon

from geoterminal.io.file import (
    FileHandlerError,
    export_data,
    read_geometry_file,
    read_wkt,
)

from typing import Generator


# Test fixtures
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


@pytest.fixture
def sample_wkt() -> str:
    """Create a sample WKT string for testing.

    Returns:
        A WKT string representing a polygon.
    """
    return "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"


@pytest.fixture
def sample_gdf() -> gpd.GeoDataFrame:
    """Create a sample GeoDataFrame for testing.

    Returns:
        A GeoDataFrame containing a single polygon.
    """
    polygon = Polygon([(30, 10), (40, 40), (20, 40), (10, 20), (30, 10)])
    return gpd.GeoDataFrame(geometry=[polygon], crs=4326)


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing.

    Returns:
        Path to a temporary directory that will be cleaned up after the test.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


# Test WKT reading
def test_read_wkt(sample_wkt: str) -> None:
    """Test reading a WKT string into a GeoDataFrame."""
    gdf = read_wkt(sample_wkt)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert gdf.crs.to_epsg() == 4326
    assert len(gdf) == 1
    assert isinstance(gdf.geometry.iloc[0], Polygon)


def test_read_wkt_invalid() -> None:
    """Test that reading an invalid WKT string raises an error."""
    with pytest.raises(FileHandlerError):
        read_wkt("INVALID WKT")


# Test file reading
def test_read_geometry_file_wkt(sample_wkt: str) -> None:
    """Test reading a WKT string using the geometry file reader."""
    gdf = read_geometry_file(sample_wkt)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert gdf.crs.to_epsg() == 4326


def test_read_geometry_file_geojson(
    temp_dir: Path, sample_gdf: gpd.GeoDataFrame
) -> None:
    """Test reading a GeoJSON file."""
    file_path = temp_dir / "test.geojson"
    sample_gdf.to_file(file_path, driver="GeoJSON")

    gdf = read_geometry_file(file_path)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == len(sample_gdf)


def test_read_geometry_file_csv(
    temp_dir: Path, sample_gdf: gpd.GeoDataFrame
) -> None:
    """Test reading a CSV file with WKT geometry."""
    file_path = temp_dir / "test.csv"
    # Convert geometry to WKT for CSV export
    df = sample_gdf.copy()
    df["geometry"] = df["geometry"].apply(lambda x: x.wkt)
    df.to_csv(file_path, index=False)

    gdf = read_geometry_file(file_path)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == len(sample_gdf)


def test_read_geometry_file_invalid() -> None:
    """Test that reading a non-existent file raises an error."""
    with pytest.raises(FileHandlerError):
        read_geometry_file("nonexistent.file")


# Test file exporting
def test_export_csv(
    tmp_path: Path, sample_point_gdf: gpd.GeoDataFrame
) -> None:
    """Test CSV export."""
    output_file = tmp_path / "test.csv"
    export_data(sample_point_gdf, output_file)
    assert output_file.exists()


def test_export_wkt_single_geometry(
    tmp_path: Path, sample_point_gdf: gpd.GeoDataFrame
) -> None:
    """Test WKT export with a single geometry."""
    output_file = tmp_path / "test.wkt"
    export_data(sample_point_gdf, output_file)

    # Check if file exists and contains valid WKT
    assert output_file.exists()
    with open(output_file) as f:
        wkt = f.read().strip()

    # Should be a single point WKT
    assert wkt.startswith("POINT")

    # Parse WKT to verify it's valid
    from shapely import wkt as wkt_parser

    geom = wkt_parser.loads(wkt)
    assert geom.geom_type == "Point"


def test_export_wkt_multiple_geometries(
    tmp_path: Path, sample_polygon_gdf: gpd.GeoDataFrame
) -> None:
    """Test WKT export with multiple geometries."""
    output_file = tmp_path / "test.wkt"
    export_data(sample_polygon_gdf, output_file)

    # Check if file exists and contains valid WKT
    assert output_file.exists()
    with open(output_file) as f:
        wkt = f.read().strip()

    # Should be a GEOMETRYCOLLECTION
    assert wkt.startswith("GEOMETRYCOLLECTION")

    # Parse WKT to verify it's valid
    from shapely import wkt as wkt_parser

    geom = wkt_parser.loads(wkt)
    assert geom.geom_type == "GeometryCollection"
    assert len(geom.geoms) == len(
        sample_polygon_gdf
    )  # Should have same number of geometries


def test_export_geojson(temp_dir: Path, sample_gdf: gpd.GeoDataFrame) -> None:
    """Test exporting data to GeoJSON format."""
    file_path = temp_dir / "output.geojson"
    export_data(sample_gdf, file_path)
    assert file_path.exists()

    # Verify exported file can be read back
    gdf = gpd.read_file(file_path)
    assert len(gdf) == len(sample_gdf)


def test_export_csv_with_wkt_geometry(temp_dir: Path, sample_gdf: gpd.GeoDataFrame) -> None:
    """Test exporting data to CSV format with WKT geometry."""
    file_path = temp_dir / "output.csv"
    export_data(sample_gdf, file_path)
    assert file_path.exists()

    # Verify exported file contains WKT geometry
    gdf = read_geometry_file(file_path)
    assert len(gdf) == len(sample_gdf)


def test_export_invalid_format(
    temp_dir: Path, sample_gdf: gpd.GeoDataFrame
) -> None:
    """Test that exporting to an invalid format raises an error."""
    with pytest.raises(FileHandlerError):
        export_data(sample_gdf, temp_dir / "output.invalid")
