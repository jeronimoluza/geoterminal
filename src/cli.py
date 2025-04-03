import argparse
from src.file_io import load_data, export_data
from src.geometry_operations import apply_buffer, reproject_gdf
from src.h3_operations import polyfill


def main():
    parser = argparse.ArgumentParser(description="GIS Toolkit CLI")

    parser.add_argument("--input-file", required=True, help="Path to the input file")
    parser.add_argument("--output-file", required=True, help="Path to the output file")
    parser.add_argument(
        "--buffer-size", type=float, help="Buffer size to apply to geometries"
    )
    parser.add_argument(
        "--h3-res", type=int, help="H3 resolution for polyfilling geometries"
    )
    parser.add_argument(
        "--h3-geom",
        action="store_true",
        help="Include H3 hexagon geometries in the output",
    )
    parser.add_argument(
        "--input-crs", type=int, help="Input coordinate reference system (CRS)"
    )
    parser.add_argument(
        "--output-crs", type=int, help="Output coordinate reference system (CRS)"
    )

    args = parser.parse_args()

    # Load the data
    gdf = load_data(
        input_file=args.input_file,
        input_crs=args.input_crs if args.input_crs else 4326,
    )

    # Apply buffer operation if specified
    if args.buffer_size:
        gdf = apply_buffer(gdf, args.buffer_size)

    # Apply H3 polyfill if specified
    if args.h3_res:
        gdf = polyfill(gdf, args.h3_res, include_geometry=args.h3_geom)

    # Reproject the GeoDataFrame if specified
    if args.output_crs:
        gdf = reproject_gdf(gdf, args.output_crs)

    # Export the data
    export_data(gdf, args.output_file)


if __name__ == "__main__":
    main()
