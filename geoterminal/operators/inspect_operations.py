"""Inspection operations module.

This module provides classes and functions for inspecting GeoDataFrames,
including viewing data samples, structure information, and metadata.
"""

from typing import Any, Dict, Optional, Tuple

import geopandas as gpd
import pandas as pd
from loguru import logger
from shapely import wkt

pd.set_option("display.max_columns", 100)


def simplify_geom_repr(geom_wkt: str) -> str:
    """Convert WKT geometry to a simplified string representation.

    Args:
        geom_wkt: WKT string representation of geometry

    Returns:
        Simplified string representation (e.g. 'POLYGON(...)')
    """
    if geom_wkt is None:
        return "None"
    return f"{wkt.loads(geom_wkt).geom_type.upper()}(...)"


class InspectOperationError(Exception):
    """Custom exception for inspection operation errors."""

    pass


class InspectProcessor:
    """Handle inspection operations with validation and error handling.

    This class provides methods for common
    inspection operations on GeoDataFrames,
    including head, tail, and metadata inspection.
    """

    def __init__(self, input_gdf: Optional[gpd.GeoDataFrame] = None):
        """Initialize the processor with an optional GeoDataFrame."""
        self.gdf = input_gdf
        self._validate_gdf()

    def _validate_gdf(self) -> None:
        """Validate the GeoDataFrame."""
        if self.gdf is not None:
            if not isinstance(self.gdf, gpd.GeoDataFrame):
                raise InspectOperationError("Input must be a GeoDataFrame")

    def set_data(self, gdf: gpd.GeoDataFrame) -> None:
        """Set the GeoDataFrame to process."""
        self.gdf = gdf
        self._validate_gdf()

    def head(self, n: int = 5) -> gpd.GeoDataFrame:
        """Get the first n rows of the GeoDataFrame.

        Args:
            n: Number of rows to return (default: 5)

        Returns:
            First n rows of the GeoDataFrame

        Raises:
            InspectOperationError: If operation fails
        """
        if self.gdf is None:
            raise InspectOperationError("No GeoDataFrame set")

        try:
            logger.info(f"Getting first {n} rows")
            result = self.gdf.head(n).to_wkt()
            result["geometry"] = result["geometry"].apply(simplify_geom_repr)
            return result
        except Exception as e:
            raise InspectOperationError(
                f"Head operation failed: {str(e)}"
            ) from e

    def tail(self, n: int = 5) -> gpd.GeoDataFrame:
        """Get the last n rows of the GeoDataFrame.

        Args:
            n: Number of rows to return (default: 5)

        Returns:
            Last n rows of the GeoDataFrame

        Raises:
            InspectOperationError: If operation fails
        """
        if self.gdf is None:
            raise InspectOperationError("No GeoDataFrame set")

        try:
            logger.info(f"Getting last {n} rows")
            result = self.gdf.tail(n).to_wkt()
            result["geometry"] = result["geometry"].apply(simplify_geom_repr)
            return result
        except Exception as e:
            raise InspectOperationError(
                f"Tail operation failed: {str(e)}"
            ) from e

    def get_crs(self) -> Optional[str]:
        """Get the Coordinate Reference System of the GeoDataFrame.

        Returns:
            CRS information as a string, or None if not set

        Raises:
            InspectOperationError: If operation fails
        """
        if self.gdf is None:
            raise InspectOperationError("No GeoDataFrame set")

        try:
            logger.info("Getting CRS information")
            return str(self.gdf.crs) if self.gdf.crs else None
        except Exception as e:
            raise InspectOperationError(
                f"CRS operation failed: {str(e)}"
            ) from e

    def get_shape(self) -> Tuple[int, int]:
        """Get the shape (dimensions) of the GeoDataFrame.

        Returns:
            Tuple of (number of rows, number of columns)

        Raises:
            InspectOperationError: If operation fails
        """
        if self.gdf is None:
            raise InspectOperationError("No GeoDataFrame set")

        try:
            logger.info("Getting shape information")
            return self.gdf.shape
        except Exception as e:
            raise InspectOperationError(
                f"Shape operation failed: {str(e)}"
            ) from e

    def get_dtypes(self) -> Dict[str, Any]:
        """Get the data types of all columns in the GeoDataFrame.

        Returns:
            Dictionary of column names and their data types

        Raises:
            InspectOperationError: If operation fails
        """
        if self.gdf is None:
            raise InspectOperationError("No GeoDataFrame set")

        try:
            logger.info("Getting data types")
            return self.gdf.dtypes.to_dict()
        except Exception as e:
            raise InspectOperationError(
                f"Data types operation failed: {str(e)}"
            ) from e
