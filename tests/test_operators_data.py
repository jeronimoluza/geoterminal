"""Tests for the data operations module."""

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point

from geoterminal.operators.data_operations import (
    DataOperationError,
    DataProcessor,
)


@pytest.fixture
def sample_data_gdf() -> gpd.GeoDataFrame:
    """Create a sample GeoDataFrame for testing data operations."""
    data = {
        "id": [1, 2, 3, 4],
        "name": ["A", "B", "C", "D"],
        "value": [10.5, 20.0, 15.7, 25.2],
        "category": ["X", "Y", "X", "Y"],
        "geometry": [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)],
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")


def test_data_processor_initialization(
    sample_data_gdf: gpd.GeoDataFrame,
) -> None:
    """Test DataProcessor initialization."""
    # Test with valid GeoDataFrame
    processor = DataProcessor(sample_data_gdf)
    assert processor.gdf is not None
    assert isinstance(processor.gdf, gpd.GeoDataFrame)

    # Test with no GeoDataFrame
    processor = DataProcessor()
    assert processor.gdf is None

    # Test with invalid input
    with pytest.raises(DataOperationError):
        DataProcessor(pd.DataFrame())


def test_query_operation(sample_data_gdf: gpd.GeoDataFrame) -> None:
    """Test query operation with various conditions."""
    processor = DataProcessor(sample_data_gdf)

    # Test numeric comparison
    result = processor.query("value > 15")
    assert len(result) == 3
    assert all(v > 15 for v in result["value"])

    processor = DataProcessor(sample_data_gdf)

    # Test string equality
    result = processor.query('category == "X"')
    assert len(result) == 2
    assert all(c == "X" for c in result["category"])

    processor = DataProcessor(sample_data_gdf)

    # Test multiple conditions
    result = processor.query('value > 15 and category == "Y"')
    assert len(result) == 2
    assert all(
        v > 15 and c == "Y"
        for v, c in zip(result["value"], result["category"])
    )

    processor = DataProcessor(sample_data_gdf)

    # Test with no matches
    result = processor.query("value > 100")
    assert len(result) == 0

    processor = DataProcessor(sample_data_gdf)

    # Test invalid query
    with pytest.raises(DataOperationError):
        processor.query("invalid column > 10")

    # Test with no data
    processor = DataProcessor()
    with pytest.raises(DataOperationError):
        processor.query("value > 10")
