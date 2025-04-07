"""File I/O operations for geospatial data.

This module provides functions for reading and writing geospatial data in
various formats, including GeoJSON, Shapefile, CSV with WKT,
and direct WKT strings.
"""

import logging
from pathlib import Path
from typing import Optional, Union

import geopandas as gpd
import pandas as pd
import pyarrow as pa
import pyarrow.orc as orc
from shapely import wkt

logger = logging.getLogger(__name__)


class FileHandlerError(Exception):
    """Custom exception for file handling errors."""

    pass


# Supported file formats and geometry types
GEOSPATIAL_FORMATS = [".shp", ".geojson", ".json"]
NONGEOSPATIAL_FORMATS = [".csv", ".orc"]
WKT_TYPES = [
    "POLYGON",
    "MULTIPOLYGON",
    "LINESTRING",
    "POINT",
    "GEOMETRYCOLLECTION",
]
GEOMETRY_COLUMNS = ["geometry", "geom", "wkt", "the_geom"]


def read_wkt(wkt_str: str, crs: int = 4326) -> gpd.GeoDataFrame:
    """Convert WKT string to GeoDataFrame.

    Args:
        wkt_str: WKT geometry string
        crs: Coordinate reference system (default: 4326)

    Returns:
        GeoDataFrame containing the geometry

    Raises:
        FileHandlerError: If WKT parsing fails
    """
    try:
        geometry = wkt.loads(wkt_str)
        gdf = gpd.GeoDataFrame(geometry=[geometry], crs=crs)
        return gdf
    except Exception as e:
        raise FileHandlerError(f"Failed to parse WKT: {str(e)}") from e


def read_orc_with_geometry(
    file_path: Path, crs: Optional[int] = None, geometry_column: Optional[str] = None
) -> gpd.GeoDataFrame:
    """Read ORC file containing geometry information.

    Args:
        file_path: Path to ORC file
        crs: Optional coordinate reference system
        geometry_column: Optional name of column containing WKT geometry strings

    Returns:
        GeoDataFrame from ORC

    Raises:
        FileHandlerError: If geometry column not found or parsing fails
    """
    try:
        # Read ORC file into pandas DataFrame
        table = orc.read_table(str(file_path))
        df = table.to_pandas()

        # Use specified geometry column or try to find one
        if geometry_column:
            if geometry_column not in df.columns:
                raise FileHandlerError(f"Specified geometry column '{geometry_column}' not found in ORC")
            geom_col = geometry_column
        else:
            # Find geometry column
            try:
                geom_col = next(
                    col for col in df.columns if any(col.lower() == g for g in GEOMETRY_COLUMNS)
                )
            except StopIteration:
                geom_col = None
            if geom_col is None:
                raise FileHandlerError("No geometry column found in ORC")

        # Convert WKT strings to geometries
        df["geometry"] = df[geom_col].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, geometry="geometry")

        if crs is not None:
            gdf.set_crs(crs, inplace=True)

        return gdf
    except Exception as e:
        if isinstance(e, FileHandlerError):
            raise
        raise FileHandlerError(f"Failed to read ORC: {str(e)}") from e


def read_csv_with_geometry(
    file_path: Path, crs: Optional[int] = None, geometry_column: Optional[str] = None
) -> gpd.GeoDataFrame:
    """Read CSV file containing geometry information.

    Args:
        file_path: Path to CSV file
        crs: Optional coordinate reference system

    Returns:
        GeoDataFrame from CSV

    Raises:
        FileHandlerError: If geometry column not found or parsing fails
    """
    try:
        df = pd.read_csv(file_path)

        # Use specified geometry column or try to find one
        if geometry_column:
            if geometry_column not in df.columns:
                raise FileHandlerError(f"Specified geometry column '{geometry_column}' not found in CSV")
            geom_col = geometry_column
        else:
            # Find geometry column
            try:
                geom_col = next(
                    col for col in df.columns if any(col.lower() == g for g in GEOMETRY_COLUMNS)
                )
            except StopIteration:
                geom_col = None
            if geom_col is None:
                raise FileHandlerError("No geometry column found in CSV")

        # Convert WKT strings to geometries
        df["geometry"] = df[geom_col].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, geometry="geometry")

        if crs is not None:
            gdf.set_crs(crs, inplace=True)

        return gdf
    except Exception as e:
        if isinstance(e, FileHandlerError):
            raise
        raise FileHandlerError(f"Failed to read CSV: {str(e)}") from e


def read_geometry_file(
    file_path: Union[str, Path], crs: Optional[int] = None,
    geometry_column: Optional[str] = None
) -> gpd.GeoDataFrame:
    """Read geometry from various file formats.

    Supported formats:
    - GeoJSON (.geojson, .json)
    - Shapefile (.shp)
    - CSV (.csv) with WKT geometry column
    - WKT string (directly)

    Args:
        file_path: Path to the geometry file or WKT string
        crs: Optional CRS to use (if not specified in file)

    Returns:
        GeoDataFrame containing the geometries

    Raises:
        FileHandlerError: If file reading fails
    """
    try:
        # Handle WKT string input
        if any(wkt_type in str(file_path) for wkt_type in WKT_TYPES):
            logger.info("Detected WKT string input")
            return read_wkt(str(file_path), crs or 4326)

        # Handle file paths
        path = Path(file_path)
        if not path.exists():
            raise FileHandlerError(f"File not found: {file_path}")

        suffix = path.suffix.lower()
        logger.info(f"Reading file with format: {suffix}")

        if suffix in [".geojson", ".json"]:
            gdf = gpd.read_file(path)
        elif suffix == ".shp":
            gdf = gpd.read_file(path)
        elif suffix == ".csv":
            gdf = read_csv_with_geometry(path, crs, geometry_column)
        elif suffix == ".orc":
            gdf = read_orc_with_geometry(path, crs, geometry_column)
        else:
            raise FileHandlerError(f"Unsupported file format: {suffix}")

        # Set CRS if provided and not already set
        if crs is not None:
            if gdf.crs is None:
                gdf.set_crs(crs, inplace=True)
            else:
                gdf = gdf.to_crs(crs)

        return gdf

    except Exception as e:
        if isinstance(e, FileHandlerError):
            raise
        raise FileHandlerError(f"Failed to read geometry: {str(e)}") from e


def export_data(gdf: gpd.GeoDataFrame, output_file: Union[str, Path]) -> None:
    """Export GeoDataFrame to various formats.

    Supported formats:
    - GeoJSON (.geojson, .json)
    - Shapefile (.shp)
    - CSV (.csv) with WKT geometry
    - ORC (.orc)

    Args:
        gdf: GeoDataFrame to export
        output_file: Path to output file

    Raises:
        FileHandlerError: If export fails
    """
    try:
        path = Path(output_file)
        suffix = path.suffix.lower()
        logger.info(f"Exporting to format: {suffix}")

        if suffix in [".geojson", ".json"]:
            gdf.to_file(path, driver="GeoJSON")
        elif suffix == ".csv":
            # Convert geometry to WKT for CSV export
            df = pd.DataFrame(gdf)
            df["geometry"] = df["geometry"].apply(
                lambda x: x.wkt if x else None
            )
            df.to_csv(path, index=False)
        elif suffix in [".shp", ".zip"]:
            gdf.to_file(path, driver="ESRI Shapefile")
        elif suffix == ".orc":
            df = pd.DataFrame(gdf)
            df["geometry"] = df["geometry"].apply(
                lambda x: x.wkt if x else None
            )
            table = pa.Table.from_pandas(df)
            with pa.output_stream(path) as orc_writer:
                pa.orc.write_table(table, orc_writer)
        else:
            raise FileHandlerError(f"Unsupported output format: {suffix}")

        logger.info(f"Successfully exported to {output_file}")

    except Exception as e:
        raise FileHandlerError(f"Failed to export data: {str(e)}") from e


# For backward compatibility
def load_data(
    input_file: Union[str, Path], input_crs: int = 4326
) -> gpd.GeoDataFrame:
    """Legacy function for backward compatibility."""
    return read_geometry_file(input_file, input_crs)
