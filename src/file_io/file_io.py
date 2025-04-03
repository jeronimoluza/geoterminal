import geopandas as gpd
import pandas as pd
from shapely import wkt
import pyarrow as pa
from src.utils.helpers import detect_file_format

GEOSPATIAL_FORMATS = ["shp", "geojson"]
NONGEOSPATIAL_FORMATS = ["csv", "orc"]
WKTS = ["POLYGON", "MULTIPOLYGON", "LINESTRING", "POINT", "GEOMETRYCOLLECTION"]


def load_data(input_file, input_crs=4326):
    """
    Load data into a GeoDataFrame or DataFrame based on the file format.
    """
    file_format = detect_file_format(input_file)
    if file_format in GEOSPATIAL_FORMATS:
        return gpd.read_file(input_file)
    elif any(input_file.startswith(wkt_type) for wkt_type in WKTS):
        return gpd.GeoDataFrame(
            [wkt.loads(input_file)], columns=["geometry"], crs=input_crs
        )
    elif file_format in NONGEOSPATIAL_FORMATS:
        df = pd.read_csv(input_file)
        if "geometry" in df.columns:
            df["geometry"] = df.geometry.apply(wkt.loads)
            return gpd.GeoDataFrame(df, crs=input_crs)
    else:
        raise ValueError("Unsupported file format")


def export_data(gdf, output_file):
    """
    Export GeoDataFrame to a specified file.
    """
    output_format = detect_file_format(output_file)
    if output_format == "geojson":
        gdf.to_file(output_file, driver="GeoJSON")
    elif output_format == "csv":
        gdf.to_csv(output_file, index=False)
    elif output_format in ["shp", "zip"]:
        gdf.to_file(output_file, driver="ESRI Shapefile")
    elif output_format == "orc":
        df = pd.DataFrame(gdf)
        table = pa.Table.from_pandas(df)
        with pa.output_stream(output_file) as orc_writer:
            pa.orc.write_table(table, orc_writer)
    else:
        raise ValueError("Unsupported output format")
