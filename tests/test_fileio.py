"""Tests for the file I/O operations module.

This module contains tests for reading and writing geospatial data in
various formats.
"""

import tempfile
from pathlib import Path
from typing import Generator

import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from geoterminal.file_io.file_io import (
    FileHandlerError,
    export_data,
    read_geometry_file,
    read_wkt,
)


# Test fixtures
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
def test_export_geojson(temp_dir: Path, sample_gdf: gpd.GeoDataFrame) -> None:
    """Test exporting data to GeoJSON format."""
    file_path = temp_dir / "output.geojson"
    export_data(sample_gdf, file_path)
    assert file_path.exists()

    # Verify exported file can be read back
    gdf = gpd.read_file(file_path)
    assert len(gdf) == len(sample_gdf)


def test_export_csv(temp_dir: Path, sample_gdf: gpd.GeoDataFrame) -> None:
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
