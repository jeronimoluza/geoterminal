"""Command-line argument parser for the geoterminal package."""

import argparse


def setup_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="GeoTerminal is a command-line tool designed to \
    simplify common GIS tasks that you may encounter in your daily work."
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
        metavar="N",
        help="Show first N rows of the geometry file in WKT format",
    )
    parser.add_argument(
        "--tail",
        type=int,
        metavar="N",
        help="Show last N rows of the geometry file in WKT format",
    )
    parser.add_argument(
        "--crs",
        action="store_true",
        help="Show coordinate reference system information",
    )

    # # Add subcommands
    # subparsers = parser.add_subparsers(
    #     dest="command", help="Additional commands"
    # )

    # Set up head and tail commands
    # setup_head_command(subparsers)
    # setup_tail_command(subparsers)

    # # Set up clip command
    # setup_clip_command(subparsers)

    return parser
