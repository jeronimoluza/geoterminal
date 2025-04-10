"""Head and tail commands implementation."""

import argparse
import logging
from shapely.geometry import base

from geoterminal.io.file import read_geometry_file

logger = logging.getLogger(__name__)


def simplify_geom_repr(geom: base.BaseGeometry) -> str:
    if geom is None:
        return "None"
    return f"{geom.geom_type.upper()}(...)"

def handle_head_command(args: argparse.Namespace) -> None:
    """Handle the head command execution.

    Args:
        args: Parsed command line arguments
    """
    gdf = read_geometry_file(args.input, args.input_crs)
    result = gdf.head(args.head)
    result["geometry"] = result["geometry"].apply(simplify_geom_repr)

    print(f"First {args.head} rows of {args.input}:")
    print(result.to_string())


def handle_tail_command(args: argparse.Namespace) -> None:
    """Handle the tail command execution.

    Args:
        args: Parsed command line arguments
    """
    gdf = read_geometry_file(args.input, args.input_crs)
    result = gdf.tail(args.head)
    result["geometry"] = result["geometry"].apply(simplify_geom_repr)
    print(f"Last {args.head} rows of {args.input}:")
    print(result.to_string())
