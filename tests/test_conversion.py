import pytest
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point
from shapely import wkt
import pyarrow as pa
from functions import utils, h3funcs
from functions.conversion import (
    ConversionFunction,
)


@pytest.fixture
def sample_polygon_wkt():
    return "POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))"


@pytest.fixture
def sample_point_wkt():
    return "POINT (0.5 0.5)"


@pytest.fixture
def sample_geodataframe():
    return gpd.GeoDataFrame(
        [{"geometry": Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])}], crs=4326
    )


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
            "id": [1, 2],
            "geometry": ["POINT (0.5 0.5)", "POINT (1.5 1.5)"],
        }
    )


def test_load_data_geospatial_format(mocker, sample_geodataframe):
    mocker.patch("functions.utils.detect_file_format", return_value="geojson")
    mocker.patch("geopandas.read_file", return_value=sample_geodataframe)

    conversion = ConversionFunction("input.geojson", "output.csv")
    result = conversion.load_data()

    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1


def test_load_data_wkt_string(sample_polygon_wkt):
    conversion = ConversionFunction(sample_polygon_wkt, "output.geojson")
    result = conversion.load_data()

    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1
    assert result.geometry.iloc[0] == wkt.loads(sample_polygon_wkt)


def test_load_data_nongeospatial_format(mocker, sample_dataframe):
    mocker.patch("functions.utils.detect_file_format", return_value="csv")
    mocker.patch("pandas.read_csv", return_value=sample_dataframe)

    conversion = ConversionFunction("input.csv", "output.geojson")
    result = conversion.load_data()

    assert isinstance(result, gpd.GeoDataFrame)
    assert "geometry" in result.columns
    assert len(result) == 2


def test_transform_data_with_buffer(sample_geodataframe):
    conversion = ConversionFunction("input.geojson", "output.geojson", buffer_size=1)
    transformed_gdf = conversion.transform_data(sample_geodataframe)
    print(transformed_gdf.geometry.iloc[0])
    print(sample_geodataframe.buffer(1).iloc[0])

    assert transformed_gdf.geometry.iloc[0].equals(
        sample_geodataframe.buffer(1).iloc[0]
    )


def test_transform_data_with_h3(mocker, sample_geodataframe):
    mocker.patch("functions.h3funcs.polyfill", return_value=sample_geodataframe)

    conversion = ConversionFunction(
        "input.geojson", "output.geojson", h3_res=9, h3_geom=True
    )
    transformed_gdf = conversion.transform_data(sample_geodataframe)

    h3funcs.polyfill.assert_called_once_with(sample_geodataframe, 9, True)
    assert isinstance(transformed_gdf, gpd.GeoDataFrame)


def test_transform_data_with_crs_conversion(sample_geodataframe):
    conversion = ConversionFunction("input.geojson", "output.geojson", output_crs=3857)
    transformed_gdf = conversion.transform_data(sample_geodataframe)

    assert transformed_gdf.crs.to_epsg() == 3857


def test_export_data_geojson(mocker, sample_geodataframe):
    mocker.patch("functions.utils.detect_file_format", return_value="geojson")
    mocker.patch("geopandas.GeoDataFrame.to_file")

    conversion = ConversionFunction("input.geojson", "output.geojson")
    conversion.export_data(sample_geodataframe)

    gpd.GeoDataFrame.to_file.assert_called_once_with("output.geojson", driver="GeoJSON")


def test_export_data_csv(mocker, sample_geodataframe):
    mocker.patch("functions.utils.detect_file_format", return_value="csv")
    mocker.patch("pandas.DataFrame.to_csv")

    conversion = ConversionFunction("input.geojson", "output.csv")
    conversion.export_data(sample_geodataframe)

    pd.DataFrame.to_csv.assert_called_once_with("output.csv", index=False)


def test_export_data_shapefile(mocker, sample_geodataframe):
    mocker.patch("functions.utils.detect_file_format", return_value="shp")
    mocker.patch("geopandas.GeoDataFrame.to_file")

    conversion = ConversionFunction("input.geojson", "output.shp")
    conversion.export_data(sample_geodataframe)

    gpd.GeoDataFrame.to_file.assert_called_once_with(
        "output.shp", driver="ESRI Shapefile"
    )


def test_export_data_orc(mocker, sample_geodataframe):
    mocker.patch("functions.utils.detect_file_format", return_value="orc")
    mocker.patch("pyarrow.orc.write_table")
    mocker.patch("pyarrow.Table.from_pandas", return_value="mock_table")
    mocker.patch("pyarrow.output_stream")

    conversion = ConversionFunction("input.geojson", "output.orc")
    conversion.export_data(sample_geodataframe)

    pa.Table.from_pandas.assert_called_once()
    pa.orc.write_table.assert_called_once()
