"""Command-line argument parser for the geoterminal package."""

import argparse

from geoterminal._version import __version__


def setup_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="GeoTerminal is a command-line tool designed to \
    simplify common GIS tasks that you may encounter in your daily work."
    )

    # Add version argument
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # Add log level argument
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level (default: INFO)",
    )

    # Add main arguments for default behavior (file conversion)
    parser.add_argument(
        "input", help="Input geometry (file path or WKT string)"
    )
    parser.add_argument(
        "output",
        nargs="?",
        help="Output file path (format determined by extension)",
    )
    parser.add_argument(
        "--mask", help="Mask geometry (file path or WKT string)"
    )
    parser.add_argument(
        "--mask-crs",
        type=int,
        default=4326,
        help="CRS for mask geometry (default: 4326)",
    )
    parser.add_argument(
        "--buffer-size", type=float, help="Buffer size to apply"
    )
    parser.add_argument(
        "--h3-res", type=int, help="H3 resolution for polyfilling"
    )
    parser.add_argument(
        "--h3-geom",
        default=True,
        action="store_true",
        help="Include H3 geometries",
    )
    parser.add_argument(
        "--input-crs", type=int, default=4326, help="Input CRS (default: 4326)"
    )
    parser.add_argument("--output-crs", type=int, help="Output CRS")
    parser.add_argument(
        "--geometry-column",
        help="Column name to use as geometry for CSV/ORC files \
        (must contain WKT strings)",
    )
    # Inspect mode arguments
    parser.add_argument(
        "--head",
        type=int,
        nargs="?",
        const=5,
        default=None,
        metavar="N",
        help="Show first N rows of the geometry file (default: 5)",
    )
    parser.add_argument(
        "--tail",
        type=int,
        nargs="?",
        const=5,
        default=None,
        metavar="N",
        help="Show last N rows of the geometry file (default: 5)",
    )
    parser.add_argument(
        "--crs",
        action="store_true",
        help="Show coordinate reference system information",
    )
    parser.add_argument(
        "--shape",
        action="store_true",
        help="Show the dimensions (rows, columns) of the GeoDataFrame",
    )
    parser.add_argument(
        "--dtypes",
        action="store_true",
        help="Show the data types of all columns in the GeoDataFrame",
    )

    # Geometric operations
    parser.add_argument(
        "--unary-union",
        action="store_true",
        help="Compute the unary union of all input geometries",
    )
    parser.add_argument(
        "--envelope",
        action="store_true",
        help="Compute the bounding box envelope of all input geometries",
    )
    parser.add_argument(
        "--convex-hull",
        action="store_true",
        help="Compute the convex hull of all input geometries",
    )
    parser.add_argument(
        "--centroid",
        action="store_true",
        help="Compute the centroid of all input geometries",
    )

    # Data operations
    parser.add_argument(
        "--query",
        type=str,
        help="Filter data using a pandas query string \
        (e.g., 'column > value')",
    )

    return parser
