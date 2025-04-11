"""Geometry processing functionality for the CLI."""

import argparse
import sys

from loguru import logger

from geoterminal.io.file import read_geometry_file
from geoterminal.operators.geometry_operations import GeometryProcessor
from geoterminal.operators.h3_operations import polyfill

# Map command line flags to operation types
OP_FLAGS = {
    "--mask": "mask",
    "--buffer-size": "buffer",
    "--h3-res": "h3",
    "--output-crs": "reproject",
    "--unary-union": "unary_union",
    "--envelope": "envelope",
    "--convex-hull": "convex_hull",
}


def process_geometries(
    processor: GeometryProcessor, args: argparse.Namespace
) -> None:
    """Process geometries based on command line arguments.

    Args:
        processor: GeometryProcessor instance
        args: Parsed command line arguments
    """
    try:
        # Get operations in order they appear in command line
        operations = []
        args_list = sys.argv[1:]
        i = 0
        while i < len(args_list):
            arg = args_list[i]
            if arg in OP_FLAGS:
                op_type = OP_FLAGS[arg]
                value = None

                if op_type == "mask":
                    value = args.mask
                elif op_type == "buffer":
                    value = args.buffer_size
                elif op_type == "h3":
                    value = args.h3_res
                elif op_type == "reproject":
                    value = args.output_crs
                elif op_type in ["unary_union", "envelope", "convex_hull"]:
                    value = True

                if value is not None:
                    operations.append((op_type, value))
            i += 1

        # Apply operations in the order they appear in command line
        for op_type, value in operations:
            if op_type == "mask":
                mask_gdf = read_geometry_file(value, args.mask_crs)
                processor.clip(mask_gdf)
            elif op_type == "buffer":
                processor.apply_buffer(value)
            elif op_type == "h3":
                processor.gdf = polyfill(
                    processor.gdf, value, include_geometry=args.h3_geom
                )
            elif op_type == "reproject":
                processor.reproject(value)
            elif op_type == "unary_union":
                processor.unary_union()
            elif op_type == "envelope":
                processor.envelope()
            elif op_type == "convex_hull":
                processor.convex_hull()

    except Exception as e:
        logger.error(f"Unexpected error during processing: {str(e)}")
        raise
