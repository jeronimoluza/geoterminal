"""Head and tail commands implementation."""
import argparse
import logging
from typing import Any

from geoterminal.file_io.file_io import read_geometry_file

logger = logging.getLogger(__name__)


def setup_head_command(subparsers: Any) -> None:
    """Set up the head command parser.

    Args:
        subparsers: Subparser group to add this command to
    """
    head_parser = subparsers.add_parser(
        "head", help="Show first n rows of the geometry file"
    )
    head_parser.add_argument("input", help="Input geometry file path")
    head_parser.add_argument(
        "-n",
        "--rows",
        type=int,
        default=5,
        help="Number of rows to show (default: 5)",
    )
    head_parser.add_argument(
        "--input-crs", type=int, default=4326, help="Input CRS (default: 4326)"
    )


def setup_tail_command(subparsers: Any) -> None:
    """Set up the tail command parser.

    Args:
        subparsers: Subparser group to add this command to
    """
    tail_parser = subparsers.add_parser(
        "tail", help="Show last n rows of the geometry file"
    )
    tail_parser.add_argument("input", help="Input geometry file path")
    tail_parser.add_argument(
        "-n",
        "--rows",
        type=int,
        default=5,
        help="Number of rows to show (default: 5)",
    )
    tail_parser.add_argument(
        "--input-crs", type=int, default=4326, help="Input CRS (default: 4326)"
    )


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
