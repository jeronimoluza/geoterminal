import geopandas as gpd
import pandas as pd
import pyarrow as pa
from shapely import wkt
from functions import utils, h3funcs

GEOSPATIAL_FORMATS = ["shp", "geojson"]
NONGEOSPATIAL_FORMATS = ["csv", "orc"]
WKTS = ["POLYGON", "MULTIPOLYGON", "LINESTRING", "POINT", "GEOMETRYCOLLECTION"]


class ConversionFunction:
    def __init__(
        self,
        input_file,
        output_file,
        h3_res=None,
        h3_geom=False,
        buffer_size=None,
        input_crs=None,
        output_crs=None,
    ):
        self.input_file = input_file
        self.output_file = output_file
        self.h3_res = h3_res
        self.h3_geom = h3_geom
        self.buffer_size = buffer_size
        if input_crs:
            self.input_crs = input_crs
        else:
            self.input_crs = 4326
        self.output_crs = output_crs

    def load_data(self):
        """
        Load data into a GeoDataFrame or DataFrame based on the file format.
        """
        if utils.detect_file_format(self.input_file) in GEOSPATIAL_FORMATS:
            return gpd.read_file(self.input_file)
        elif len([f for f in WKTS if str(self.input_file).startswith(f)]):
            return gpd.GeoDataFrame(
                [wkt.loads(self.input_file)], columns=["geometry"], crs=self.input_crs
            )
        elif utils.detect_file_format(self.input_file) in NONGEOSPATIAL_FORMATS:
            df = pd.read_csv(self.input_file)
            if "geometry" in df.columns:
                df["geometry"] = df.geometry.apply(wkt.loads)
                return gpd.GeoDataFrame(df, crs=self.input_crs)

        else:
            raise ValueError("Unsupported file format")

    def transform_data(self, gdf):
        """
        Apply transformations to the GeoDataFrame.
        """
        if self.buffer_size:
            gdf.geometry = gdf.geometry.buffer(self.buffer_size)
        if self.h3_res:
            gdf = h3funcs.polyfill(gdf, self.h3_res, self.h3_geom)
        if self.output_crs:
            gdf = gdf.to_crs(crs=self.output_crs)
        return gdf

    def export_data(self, gdf):
        """
        Export GeoDataFrame to a specified file.
        """
        output_format = utils.detect_file_format(self.output_file)
        if output_format == "geojson":
            gdf.to_file(self.output_file, driver="GeoJSON")
        elif output_format == "csv":
            gdf.to_csv(self.output_file, index=False)
        elif output_format in ["shp", "zip"]:
            gdf.to_file(self.output_file, driver="ESRI Shapefile")
        elif output_format == "orc":
            df = pd.DataFrame(gdf)
            table = pa.Table.from_pandas(df)
            with pa.output_stream(self.output_file) as orc_writer:
                pa.orc.write_table(table, orc_writer)
        else:
            raise ValueError("Unsupported output format")
