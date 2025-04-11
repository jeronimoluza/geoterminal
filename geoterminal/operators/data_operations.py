"""Data operations module.

This module provides classes and functions for performing
non-geometric operations on GeoDataFrames, such as filtering and querying.
"""

from typing import Optional

import geopandas as gpd
from loguru import logger


class DataOperationError(Exception):
    """Custom exception for data operation errors."""

    pass


class DataProcessor:
    """Handle data operations with validation and error handling.

    This class provides methods for common data operations on GeoDataFrames,
    including filtering and querying.
    """

    def __init__(self, input_gdf: Optional[gpd.GeoDataFrame] = None):
        """Initialize the processor with an optional GeoDataFrame."""
        self.gdf = input_gdf
        self._validate_gdf()

    def _validate_gdf(self) -> None:
        """Validate the GeoDataFrame."""
        if self.gdf is not None:
            if not isinstance(self.gdf, gpd.GeoDataFrame):
                raise DataOperationError("Input must be a GeoDataFrame")

    def set_data(self, gdf: gpd.GeoDataFrame) -> None:
        """Set the GeoDataFrame to process."""
        self.gdf = gdf
        self._validate_gdf()

    def query(self, query_string: str) -> gpd.GeoDataFrame:
        """Filter the GeoDataFrame using a pandas query string.

        Args:
            query_string: Query string in pandas query format
            (e.g., "column > value")

        Returns:
            Filtered GeoDataFrame

        Raises:
            DataOperationError: If query operation fails
        """
        if self.gdf is None:
            raise DataOperationError("No GeoDataFrame set")

        try:
            logger.info(f"Applying query: {query_string}")
            self.gdf = self.gdf.query(query_string)
            return self.gdf
        except Exception as e:
            raise DataOperationError(
                f"Query operation failed: {str(e)}"
            ) from e
