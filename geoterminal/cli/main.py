"""Command-line interface for the geoterminal package."""

import sys

from loguru import logger

from geoterminal.cli.parser import setup_parser
from geoterminal.cli.processor import process_geometries
from geoterminal.io.file import (
    FileHandlerError,
    export_data,
    read_geometry_file,
)
from geoterminal.log import setup_logging
from geoterminal.operators.geometry_operations import (
    GeometryOperationError,
    GeometryProcessor,
)
from geoterminal.operators.inspect_operations import InspectProcessor


def main() -> None:
    """Execute the main CLI functionality."""
    try:
        # Parse arguments
        parser = setup_parser()
        args = parser.parse_args()

        # Configure logging
        setup_logging(args.log_level)

        # Read input file
        gdf = read_geometry_file(
            args.input, args.input_crs, args.geometry_column
        )

        # If only input is provided, enter inspect mode
        if not args.output:
            # Initialize inspect processor
            inspect_processor = InspectProcessor(gdf)

            # Handle inspection operations
            if args.head is not None:
                result = inspect_processor.head(args.head if args.head else 5)
                print(result)
            elif args.tail is not None:
                result = inspect_processor.tail(args.tail if args.tail else 5)
                print(result)
            elif args.crs:
                crs = inspect_processor.get_crs()
                print(f"CRS: {crs}")
            elif args.shape:
                shape = inspect_processor.get_shape()
                print(f"Shape: {shape[0]} rows × {shape[1]} columns")
            elif args.dtypes:
                dtypes = inspect_processor.get_dtypes()
                print("Column data types:")
                for col, dtype in dtypes.items():
                    print(f"  {col}: {dtype}")
            else:
                # Show inspect mode help
                logger.info("\nInspect Mode Options:")
                logger.info("  --head N     Show first N rows")
                logger.info("  --tail N     Show last N rows")
                logger.info(
                    "  --crs        Show coordinate reference system info"
                )
                logger.info("  --shape      Show dimensions (rows × columns)")
                logger.info("  --dtypes     Show column data types")
            return

        # Default behavior: file conversion with optional operations
        processor = GeometryProcessor(gdf)
        process_geometries(processor, args)

        # Export results
        export_data(processor.gdf, args.output)
        logger.info(f"Successfully processed and saved to {args.output}")

    except FileHandlerError as e:
        logger.error(f"File handling error: {str(e)}")
        sys.exit(1)
    except GeometryOperationError as e:
        logger.error(f"Geometry operation error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
