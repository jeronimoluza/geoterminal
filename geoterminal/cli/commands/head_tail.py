"""Head and tail commands implementation."""
import argparse
import logging
from typing import Any

from geoterminal.file_io.file_io import read_geometry_file

logger = logging.getLogger(__name__)


def handle_head_command(args: argparse.Namespace) -> None:
    """Handle the head command execution.

    Args:
        args: Parsed command line arguments
    """
    gdf = read_geometry_file(args.input, args.input_crs)
    result = gdf.head(args.rows)
    print(f"First {args.rows} rows of {args.input}:")
    print(result.to_string())


def handle_tail_command(args: argparse.Namespace) -> None:
    """Handle the tail command execution.

    Args:
        args: Parsed command line arguments
    """
    gdf = read_geometry_file(args.input, args.input_crs)
    result = gdf.tail(args.rows)
    print(f"Last {args.rows} rows of {args.input}:")
    print(result.to_string())
