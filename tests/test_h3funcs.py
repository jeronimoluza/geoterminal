import geopandas as gpd
import h3
import pytest
from geopandas import GeoDataFrame
from shapely.geometry import MultiPolygon, Polygon

from functions.h3funcs import get_geometry, polyfill


def test_polyfill_with_polygon():
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    resolution = 5
    result = polyfill(polygon, resolution)
    assert isinstance(result, GeoDataFrame)
    assert "hex" in result.columns
    assert len(result) > 0


def test_polyfill_with_multipolygon():
    polygon1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    polygon2 = Polygon([(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)])
    multipolygon = MultiPolygon([polygon1, polygon2])
    resolution = 5
    result = polyfill(multipolygon, resolution)
    assert isinstance(result, GeoDataFrame)
    assert "hex" in result.columns
    assert len(result) > 0


def test_polyfill_with_wkt_string():
    wkt_string = "POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))"
    resolution = 5
    result = polyfill(wkt_string, resolution)
    assert isinstance(result, GeoDataFrame)
    assert "hex" in result.columns
    assert len(result) > 0


def test_polyfill_with_geodataframe():
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    gdf = gpd.GeoDataFrame([polygon], columns=["geometry"])
    resolution = 5
    result = polyfill(gdf, resolution)
    assert isinstance(result, GeoDataFrame)
    assert "hex" in result.columns
    assert len(result) > 0


def test_polyfill_with_geom():
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    resolution = 5
    result = polyfill(polygon, resolution, geom=True)
    assert isinstance(result, GeoDataFrame)
    assert "hex" in result.columns
    assert "geometry" in result.columns
    assert len(result) > 0


def test_get_geometry():
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    resolution = 5
    hex_id = polyfill(polygon, resolution).hex.values[0]
    geom = get_geometry(hex_id)
    assert isinstance(geom, Polygon)
    assert len(geom.exterior.coords) > 0
