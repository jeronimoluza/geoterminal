"""Command-line argument parser for the geoterminal package."""

import argparse

from geoterminal.cli.commands.clip import setup_clip_command
from geoterminal.cli.commands.head_tail import (
    setup_head_command,
    setup_tail_command,
)


def setup_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(description="GIS Toolkit CLI")

    # Add main arguments for default behavior
    parser.add_argument(
        "input", help="Input geometry (file path or WKT string)"
    )
    parser.add_argument(
        "output", help="Output file path (format determined by extension)"
    )
    parser.add_argument(
        "--buffer-size", type=float, help="Buffer size to apply"
    )
    parser.add_argument(
        "--h3-res", type=int, help="H3 resolution for polyfilling"
    )
    parser.add_argument(
        "--h3-geom", action="store_true", help="Include H3 geometries"
    )
    parser.add_argument(
        "--input-crs", type=int, default=4326, help="Input CRS (default: 4326)"
    )
    parser.add_argument("--output-crs", type=int, help="Output CRS")
    parser.add_argument(
        "--geometry-column", 
        help="Column name to use as geometry for CSV/ORC files (must contain WKT strings)"
    )

    # Add subcommands
    subparsers = parser.add_subparsers(
        dest="command", help="Additional commands"
    )

    # Set up head and tail commands
    setup_head_command(subparsers)
    setup_tail_command(subparsers)

    # Set up clip command
    setup_clip_command(subparsers)

    return parser
