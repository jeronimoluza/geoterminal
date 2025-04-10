"""Main CLI entry point for the geoterminal package."""

from loguru import logger

from geoterminal.cli.commands.head_tail import (
    handle_head_command,
    handle_tail_command,
)
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
from geoterminal.operators.h3_operations import H3OperationError


def main() -> None:
    """Execute the main CLI functionality.

    Parse command line arguments and process the geospatial data accordingly.
    """
    parser = setup_parser()
    args = parser.parse_args()

    # Set up logging with provided log level
    setup_logging(args.log_level)

    try:
        # Handle special commands if specified
        if args.head:
            handle_head_command(args)
            return
        elif args.tail:
            handle_tail_command(args)
            return

        # If only input is provided, enter inspect mode
        if not args.output:
            if args.head:
                handle_head_command(args)
            elif args.tail:
                handle_tail_command(args)
            elif args.crs:
                # Show CRS information
                gdf = read_geometry_file(
                    args.input, args.input_crs, args.geometry_column
                )
                logger.info(f"CRS: {gdf.crs}")
            else:
                # Show inspect mode help
                logger.info("\nInspect Mode Options:")
                logger.info("  --head N     Show first N rows in WKT format")
                logger.info("  --tail N     Show last N rows in WKT format")
                logger.info(
                    "  --crs        Show coordinate reference system info"
                )
            return

        # Default behavior: file conversion with optional operations
        gdf = read_geometry_file(
            args.input, args.input_crs, args.geometry_column
        )

        processor = GeometryProcessor(gdf)
        process_geometries(processor, args)

        # Export results
        export_data(processor.gdf, args.output)
        logger.info(f"Successfully processed and saved to {args.output}")

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
