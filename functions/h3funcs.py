import warnings

warnings.filterwarnings("ignore")
import h3
from typing import Optional, Union
from shapely import Polygon, MultiPolygon, wkt
from geopandas import GeoDataFrame
import geopandas as gpd


def polyfill(
    unary: Optional[Union[str, Polygon, MultiPolygon, GeoDataFrame]],
    resolution: int,
    geom=False,
):
    if type(unary) == str:
        unary = wkt.loads(unary)
    elif type(unary) == GeoDataFrame:
        unary = unary.union_all()

    def polyfill_polygon(unary, resolution):
        coords = [(lat, lon) for lon, lat in unary.exterior.coords]
        return h3.polygon_to_cells(h3.Polygon(coords), resolution)

    # unary = gdf.union_all()
    if type(unary) == Polygon:
        data = gpd.GeoDataFrame(
            list(polyfill_polygon(unary, resolution)), columns=["hex"]
        )

    if type(unary) == MultiPolygon:
        multi = gpd.GeoDataFrame({"geometry": [unary]})
        finalset = []
        for g in multi.explode(index_parts=True).geometry.values:
            hexes = polyfill_polygon(g, resolution)
            finalset.extend(hexes)
        data = gpd.GeoDataFrame(list(set(finalset)), columns=["hex"])

    if geom:
        geometry = data.hex.apply(get_geometry)
        data = gpd.GeoDataFrame(data, geometry=geometry)
        data["geometry"] = data.geometry.buffer(0)
    return data


def get_geometry(hex_id):
    pairs = h3.cell_to_boundary(hex_id, geo_json=True)
    return Polygon(pairs)
