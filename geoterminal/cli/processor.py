"""Geometry processing functionality for the CLI."""

import argparse
import logging

from geoterminal.file_io.file_io import read_geometry_file
from geoterminal.geometry_operations.geometry_operations import (
    GeometryProcessor,
)
from geoterminal.h3_operations.h3_operations import polyfill

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
        # Get the order of operations from the command line arguments
        operations = []
        for arg in vars(args):
            value = getattr(args, arg)
            if value is not None:
                if arg == 'mask' and value:
                    operations.append(('mask', value))
                elif arg == 'buffer_size' and value:
                    operations.append(('buffer', value))
                elif arg == 'h3_res' and value:
                    operations.append(('h3', value))
                elif arg == 'output_crs' and value:
                    operations.append(('reproject', value))
        
        # Apply operations in the order they appear in command line
        for op_type, value in operations:
            if op_type == 'mask':
                mask_gdf = read_geometry_file(value, args.mask_crs)
                processor.clip(mask_gdf)
            elif op_type == 'buffer':
                processor.apply_buffer(value)
            elif op_type == 'h3':
                processor.gdf = polyfill(
                    processor.gdf, value, include_geometry=args.h3_geom
                )
            elif op_type == 'reproject':
                processor.reproject(value)

    except Exception as e:
        logger.error(f"Unexpected error during processing: {str(e)}")
        raise
