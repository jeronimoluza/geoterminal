"""Test suite for inspection operations."""

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

from geoterminal.operators.inspect_operations import (
    InspectOperationError,
    InspectProcessor,
    simplify_geom_repr,
)


@pytest.fixture
def sample_gdf() -> gpd.GeoDataFrame:
    """Create a sample GeoDataFrame for testing."""
    # Create a simple GeoDataFrame with different geometry types
    data = {
        "id": [1, 2, 3, 4],
        "name": ["A", "B", "C", "D"],
        "value": [10.5, 20.0, 15.7, 25.2],
        "geometry": [
            Point(0, 0),
            Point(1, 1),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Point(2, 2),
        ],
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")


@pytest.fixture
def inspect_processor(sample_gdf: gpd.GeoDataFrame) -> InspectProcessor:
    """Create an InspectProcessor instance with sample data."""
    return InspectProcessor(sample_gdf)


def test_simplify_geom_repr() -> None:
    """Test geometry representation simplification."""
    # Test point simplification
    point_wkt = "POINT (0.000000 0.000000)"
    assert simplify_geom_repr(point_wkt) == "POINT(...)"

    # Test polygon simplification
    polygon_wkt = "POLYGON ((0.000000 0.000000, 1.000000 0.000000, \
    1.000000 1.000000, 0.000000 1.000000, 0.000000 0.000000))"
    expected = "POLYGON(...)"
    assert simplify_geom_repr(polygon_wkt) == expected


def test_inspect_processor_initialization(
    sample_gdf: gpd.GeoDataFrame,
) -> None:
    """Test InspectProcessor initialization."""
    # Test with valid GeoDataFrame
    processor = InspectProcessor(sample_gdf)
    assert processor.gdf is not None
    assert isinstance(processor.gdf, gpd.GeoDataFrame)

    # Test with no GeoDataFrame
    processor = InspectProcessor()
    assert processor.gdf is None

    # Test with invalid input
    with pytest.raises(InspectOperationError):
        InspectProcessor(pd.DataFrame())


def test_head_operation(
    inspect_processor: InspectProcessor, sample_gdf: gpd.GeoDataFrame
) -> None:
    """Test head operation."""
    # Test default head (5 rows)
    result = inspect_processor.head()
    assert isinstance(
        result, pd.DataFrame
    )  # Result is a DataFrame with WKT geometries
    assert len(result) == len(
        sample_gdf
    )  # Since sample has fewer rows than default
    assert "geometry" in result.columns
    assert isinstance(
        result["geometry"].iloc[0], str
    )  # Geometry should be WKT string

    # Test custom number of rows
    result = inspect_processor.head(2)
    assert len(result) == 2

    # Test with no data
    processor = InspectProcessor()
    with pytest.raises(InspectOperationError):
        processor.head()


def test_tail_operation(
    inspect_processor: InspectProcessor, sample_gdf: gpd.GeoDataFrame
) -> None:
    """Test tail operation."""
    # Test default tail (5 rows)
    result = inspect_processor.tail()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == len(
        sample_gdf
    )  # Since sample has fewer rows than default
    assert "geometry" in result.columns
    assert isinstance(result["geometry"].iloc[0], str)

    # Test custom number of rows
    result = inspect_processor.tail(2)
    assert len(result) == 2

    # Test with no data
    processor = InspectProcessor()
    with pytest.raises(InspectOperationError):
        processor.tail()


def test_get_crs(inspect_processor: InspectProcessor) -> None:
    """Test CRS retrieval."""
    crs = inspect_processor.get_crs()
    assert crs == "EPSG:4326"

    # Test with no data
    processor = InspectProcessor()
    with pytest.raises(InspectOperationError):
        processor.get_crs()


def test_get_shape(
    inspect_processor: InspectProcessor, sample_gdf: gpd.GeoDataFrame
) -> None:
    """Test shape retrieval."""
    shape = inspect_processor.get_shape()
    assert isinstance(shape, tuple)
    assert len(shape) == 2
    assert shape[0] == len(sample_gdf)  # Number of rows
    assert shape[1] == len(sample_gdf.columns)  # Number of columns

    # Test with no data
    processor = InspectProcessor()
    with pytest.raises(InspectOperationError):
        processor.get_shape()


def test_get_dtypes(inspect_processor: InspectProcessor) -> None:
    """Test data types retrieval."""
    dtypes = inspect_processor.get_dtypes()
    assert isinstance(dtypes, dict)
    assert "geometry" in dtypes
    assert "id" in dtypes
    assert "name" in dtypes
    assert "value" in dtypes

    # Test with no data
    processor = InspectProcessor()
    with pytest.raises(InspectOperationError):
        processor.get_dtypes()


def test_set_data(sample_gdf: gpd.GeoDataFrame) -> None:
    """Test setting data after initialization."""
    processor = InspectProcessor()
    assert processor.gdf is None

    processor.set_data(sample_gdf)
    assert processor.gdf is not None
    assert isinstance(processor.gdf, gpd.GeoDataFrame)

    # Test with invalid input
    with pytest.raises(InspectOperationError):
        processor.set_data(pd.DataFrame())
