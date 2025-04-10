"""Head and tail commands implementation."""

import argparse
import logging
from shapely import wkt

from geoterminal.io.file import read_geometry_file

logger = logging.getLogger(__name__)


def simplify_geom_repr(geom_wkt: str) -> str:
    if geom_wkt is None:
        return "None"
    return f"{wkt.loads(geom_wkt).geom_type.upper()}(...)"

def handle_head_command(args: argparse.Namespace) -> None:
    """Handle the head command execution.

    Args:
        args: Parsed command line arguments
    """
    gdf = read_geometry_file(args.input, args.input_crs)
    result = gdf.head(args.head).to_wkt()
    result["geometry"] = result["geometry"].apply(simplify_geom_repr)
    print(f"First {args.head} rows of {args.input}:")
    print(result.to_string())


def handle_tail_command(args: argparse.Namespace) -> None:
    """Handle the tail command execution.

    Args:
        args: Parsed command line arguments
    """
    gdf = read_geometry_file(args.input, args.input_crs)
    result = gdf.tail(args.tail).to_wkt()
    result["geometry"] = result["geometry"].apply(simplify_geom_repr)
    print(f"Last {args.tail} rows of {args.input}:")
    print(result.to_string())
