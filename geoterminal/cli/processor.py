"""Geometry processing functionality for the CLI."""

import argparse
import logging

from geoterminal.geometry_operations.geometry_operations import (
    GeometryProcessor,
)
from geoterminal.h3_operations.h3_operations import polyfill

from geoterminal.file_io.file_io import read_geometry_file

logger = logging.getLogger(__name__)


def process_geometries(
    processor: GeometryProcessor, args: argparse.Namespace
) -> None:
    """Process geometries based on command line arguments.

    Args:
        processor: GeometryProcessor instance
        args: Parsed command line arguments
    """
    try:
        # Apply clip operation if specified
        if args.mask:
            mask_gdf = read_geometry_file(args.mask, args.mask_crs)
            processor.clip(mask_gdf)

        # Apply buffer operation if specified
        if args.buffer_size:
            processor.apply_buffer(args.buffer_size)

        # Apply H3 polyfill if specified
        if args.h3_res:
            processor.gdf = polyfill(
                processor.gdf, args.h3_res, include_geometry=args.h3_geom
            )

        # Reproject if specified
        if args.output_crs:
            processor.reproject(args.output_crs)

    except Exception as e:
        logger.error(f"Unexpected error during processing: {str(e)}")
        raise
