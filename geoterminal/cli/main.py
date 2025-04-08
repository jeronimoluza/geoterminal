"""Main CLI entry point for the geoterminal package."""

import logging

from geoterminal.cli.commands.clip import handle_clip_command
from geoterminal.cli.commands.head_tail import (
    handle_head_command,
    handle_tail_command,
)
from geoterminal.cli.parser import setup_parser
from geoterminal.cli.processor import process_geometries
from geoterminal.file_io.file_io import (
    FileHandlerError,
    export_data,
    read_geometry_file,
)
from geoterminal.geometry_operations.geometry_operations import (
    GeometryOperationError,
    GeometryProcessor,
)
from geoterminal.h3_operations.h3_operations import H3OperationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Execute the main CLI functionality.

    Parse command line arguments and process the geospatial data accordingly.
    """
    parser = setup_parser()
    args = parser.parse_args()

    try:
        # Handle special commands if specified
        if args.head:
            handle_head_command(args)
            return
        elif args.tail:
            handle_tail_command(args)
            return

        # If only input is provided, show help
        if not args.output:
            parser.print_help()
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
