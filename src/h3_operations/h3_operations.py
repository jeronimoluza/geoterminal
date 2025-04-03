import logging
from typing import List, Optional, Set, Tuple, Union

from shapely import Polygon
from shapely.geometry.base import BaseGeometry
import geopandas as gpd
import pandas as pd
import h3

# Configure logging
logger = logging.getLogger(__name__)

class H3OperationError(Exception):
    """Custom exception for H3 operation errors."""
    pass

class H3Processor:
    """Class to handle H3 operations with validation and error handling."""

    def __init__(self, input_gdf: Optional[gpd.GeoDataFrame] = None):
        """Initialize the processor with an optional GeoDataFrame.

        Args:
            input_gdf: Optional GeoDataFrame to process
        """
        self.gdf = input_gdf
        self._validate_gdf()

    def _validate_gdf(self) -> None:
        """Validate the GeoDataFrame."""
        if self.gdf is not None:
            if not isinstance(self.gdf, gpd.GeoDataFrame):
                raise H3OperationError("Input must be a GeoDataFrame")
            if not self.gdf.geometry.is_valid.all():
                logger.warning("Some geometries in the GeoDataFrame are invalid")

    def set_data(self, gdf: gpd.GeoDataFrame) -> None:
        """Set the GeoDataFrame to process.

        Args:
            gdf: GeoDataFrame to process
        """
        self.gdf = gdf
        self._validate_gdf()

    @staticmethod
    def get_hex_geometry(hex_id: str) -> Polygon:
        """Get the geometry of a given hex identifier.

        Args:
            hex_id: H3 hexagon identifier

        Returns:
            Polygon representing the hexagon

        Raises:
            H3OperationError: If hex_id is invalid or conversion fails
        """
        try:
            if not h3.is_valid_cell(hex_id):
                raise H3OperationError(f"Invalid H3 cell identifier: {hex_id}")

            pairs = h3.cell_to_boundary(hex_id)
            pairs_reversed = [(lng, lat) for lat, lng in pairs]
            return Polygon(pairs_reversed)
        except Exception as e:
            raise H3OperationError(f"Failed to get hex geometry: {str(e)}") from e

    def polyfill(self, resolution: int, include_geometry: bool = False) -> gpd.GeoDataFrame:
        """Apply H3 polyfill operation to the GeoDataFrame.

        Args:
            resolution: H3 resolution level (0-15)
            include_geometry: Whether to include hexagon geometries

        Returns:
            GeoDataFrame with H3 hexagons

        Raises:
            H3OperationError: If operation fails or parameters are invalid
        """
        if self.gdf is None:
            raise H3OperationError("No GeoDataFrame set")

        if not 0 <= resolution <= 15:
            raise H3OperationError(f"Invalid H3 resolution: {resolution}. Must be between 0 and 15")

        try:
            logger.info(f"Applying H3 polyfill at resolution {resolution}")
            hexes: List[str] = []
            
            # Explode multipolygons into individual polygons
            self.gdf = self.gdf.explode(index_parts=True).reset_index(drop=True)
            
            for geom in self.gdf.geometry:
                if geom.is_valid:
                    hex_set: Set[str] = h3.geo_to_cells(geom, res=resolution)
                    hexes.extend(list(hex_set))
                else:
                    logger.warning(f"Skipping invalid geometry")

            hex_gdf = pd.DataFrame({"hex": hexes})

            if include_geometry:
                logger.info("Including hexagon geometries in output")
                hex_gdf["geometry"] = hex_gdf["hex"].apply(self.get_hex_geometry)
                hex_gdf = gpd.GeoDataFrame(hex_gdf, crs=4326)

            return hex_gdf

        except Exception as e:
            raise H3OperationError(f"H3 polyfill operation failed: {str(e)}") from e

# For backward compatibility
def get_hex_geometry(hex_id: str) -> Polygon:
    """Legacy function for backward compatibility."""
    return H3Processor.get_hex_geometry(hex_id)

def polyfill(gdf: gpd.GeoDataFrame, resolution: int, include_geometry: bool = False) -> gpd.GeoDataFrame:
    """Legacy function for backward compatibility."""
    processor = H3Processor(gdf)
    return processor.polyfill(resolution, include_geometry)
