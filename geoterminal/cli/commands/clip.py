"""Clip command implementation."""
import argparse
import logging
from typing import Any

from geoterminal.file_io.file_io import export_data, read_geometry_file
from geoterminal.geometry_operations.geometry_operations import GeometryProcessor

logger = logging.getLogger(__name__)

def setup_clip_command(subparsers: Any) -> None:
    """Set up the clip command parser.
    
    Args:
        subparsers: Subparser group to add this command to
    """
    clip_parser = subparsers.add_parser(
        "clip", help="Clip geometries with mask"
    )
    clip_parser.add_argument(
        "input",
        help=(
            "Input geometry (file path or WKT string). Supported formats: "
            "GeoJSON, Shapefile, CSV with WKT, or inline WKT"
        ),
    )
    clip_parser.add_argument(
        "mask",
        help=(
            "Mask geometry (file path or WKT string). Supported formats: "
            "GeoJSON, Shapefile, CSV with WKT, or inline WKT"
        ),
    )
    clip_parser.add_argument(
        "output",
        help=(
            "Output file path. Format determined by extension "
            "(.geojson, .shp, .csv)"
        ),
    )
    clip_parser.add_argument(
        "--input-crs",
        type=int,
        default=4326,
        help="CRS for input geometry (default: 4326)",
    )
    clip_parser.add_argument(
        "--mask-crs",
        type=int,
        default=4326,
        help="CRS for mask geometry (default: 4326)",
    )

def handle_clip_command(args: argparse.Namespace) -> None:
    """Handle the clip command execution.
    
    Args:
        args: Parsed command line arguments
    """
    # Load input geometry
    logger.info(f"Reading input geometry from {args.input}")
    input_gdf = read_geometry_file(args.input, args.input_crs)

    # Load mask geometry
    logger.info(f"Reading mask geometry from {args.mask}")
    mask_gdf = read_geometry_file(args.mask, args.mask_crs)

    # Process clip operation
    processor = GeometryProcessor(input_gdf)
    processor.clip(mask_gdf)

    # Export results
    export_data(processor.gdf, args.output)
    logger.info(f"Successfully clipped and saved to {args.output}")
