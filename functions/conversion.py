import geopandas as gpd
import pandas as pd
import pyarrow as pa
from shapely import wkt

GEOSPATIAL_FORMATS = ["shp", "geojson"]
NONGEOSPATIAL_FORMATS = ["csv", "orc"]


class ConversionFunction:
    def __init__(
        self, input_file, output_file, buffer_size=None, input_crs=None, output_crs=None
    ):
        self.input_file = input_file
        self.output_file = output_file
        self.buffer_size = buffer_size
        self.input_crs = input_crs
        self.output_crs = output_crs

    @staticmethod
    def detect_file_format(file_path):
        """
        Detect the file format based on the file extension.
        """
        extension = file_path.split(".")[-1].lower()
        return extension

    def load_data(self):
        """
        Load data into a GeoDataFrame or DataFrame based on the file format.
        """
        if self.detect_file_format(self.input_file) in GEOSPATIAL_FORMATS:
            return gpd.read_file(self.input_file)
        elif self.detect_file_format(self.input_file) in NONGEOSPATIAL_FORMATS:
            df = pd.read_csv(self.input_file)
            if "geometry" in df.columns:
                df["geometry"] = df.geometry.apply(wkt.loads)
                if self.input_crs:
                    return gpd.GeoDataFrame(df, crs=self.input_crs)
                else:
                    return gpd.GeoDataFrame(df, crs=4326)

        else:
            raise ValueError("Unsupported file format")

    def transform_data(self, gdf):
        """
        Apply transformations to the GeoDataFrame.
        """
        if self.output_crs:
            gdf = gdf.to_crs(crs=self.output_crs)
        if self.buffer_size:
            gdf.geometry = gdf.buffer(self.buffer_size)
        return gdf

    def export_data(self, gdf):
        """
        Export GeoDataFrame to a specified file.
        """
        output_format = self.detect_file_format(self.output_file)
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
