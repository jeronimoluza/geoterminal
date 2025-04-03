import argparse
import logging
from pathlib import Path
from typing import Optional, Union

from geoterminal.file_io.file_io import read_geometry_file, export_data, FileHandlerError
from geoterminal.geometry_operations.geometry_operations import GeometryProcessor, GeometryOperationError
from geoterminal.h3_operations.h3_operations import H3Processor, H3OperationError, polyfill

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_geometries(processor: GeometryProcessor, args: argparse.Namespace) -> None:
    """Process geometries based on command line arguments.

    Args:
        processor: GeometryProcessor instance
        args: Parsed command line arguments
    """
    try:
        # Apply buffer operation if specified
        if args.buffer_size:
            processor.apply_buffer(args.buffer_size)

        # Apply H3 polyfill if specified
        if args.h3_res:
            processor.gdf = polyfill(processor.gdf, args.h3_res, include_geometry=args.h3_geom)

        # Reproject if specified
        if args.output_crs:
            processor.reproject(args.output_crs)

    except GeometryOperationError as e:
        logger.error(f"Geometry operation failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during processing: {str(e)}")
        raise

def setup_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(description="GIS Toolkit CLI")
    
    # Add main arguments (previously process command arguments)
    parser.add_argument("input", help="Input geometry (file path or WKT string)")
    parser.add_argument("output", help="Output file path (format determined by extension)")
    parser.add_argument("--buffer-size", type=float, help="Buffer size to apply")
    parser.add_argument("--h3-res", type=int, help="H3 resolution for polyfilling")
    parser.add_argument("--h3-geom", action="store_true", help="Include H3 geometries")
    parser.add_argument("--input-crs", type=int, default=4326, help="Input CRS (default: 4326)")
    parser.add_argument("--output-crs", type=int, help="Output CRS")
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Additional commands')

    # Clip command
    clip_parser = subparsers.add_parser('clip', help='Clip geometries with mask')
    clip_parser.add_argument(
        'input',
        help='Input geometry (file path or WKT string). Supported formats: GeoJSON, Shapefile, CSV with WKT, or inline WKT'
    )
    clip_parser.add_argument(
        'mask',
        help='Mask geometry (file path or WKT string). Supported formats: GeoJSON, Shapefile, CSV with WKT, or inline WKT'
    )
    clip_parser.add_argument(
        'output',
        help='Output file path. Format determined by extension (.geojson, .shp, .csv)'
    )
    clip_parser.add_argument(
        '--input-crs',
        type=int,
        default=4326,
        help='CRS for input geometry (default: 4326)'
    )
    clip_parser.add_argument(
        '--mask-crs',
        type=int,
        default=4326,
        help='CRS for mask geometry (default: 4326)'
    )

    return parser

def main() -> None:
    """Main entry point for the CLI."""
    parser = setup_parser()
    args = parser.parse_args()

    try:
        # Default behavior (previously process command)
        if not args.command:
            # Load and process data
            gdf = read_geometry_file(args.input, args.input_crs)
            
            processor = GeometryProcessor(gdf)
            process_geometries(processor, args)
            
            # Export results
            export_data(processor.gdf, args.output)
            logger.info(f"Successfully processed and saved to {args.output}")

        elif args.command == 'clip':
            try:
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

            except FileHandlerError as e:
                logger.error(f"File handling error: {str(e)}")
                raise SystemExit(1)

    except (GeometryOperationError, H3OperationError) as e:
        logger.error(f"Operation failed: {str(e)}")
        raise SystemExit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
