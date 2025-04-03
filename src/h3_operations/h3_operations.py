from shapely import Polygon
import geopandas as gpd
import pandas as pd
import h3


def get_hex_geometry(hex_id):
    """Gets the geometry of a given hex identifier

    Args:
        hex_id (str): Hexagon identifier

    Returns:
        str: WKT of the hexagon geometry
    """
    pairs = h3.cell_to_boundary(hex_id)
    pairs_reversed = [(lng, lat) for lat, lng in pairs]
    return Polygon(pairs_reversed)


def polyfill(gdf, resolution, include_geometry=False):
    """
    Apply H3 polyfill operation to the GeoDataFrame.

    Parameters:
        gdf (GeoDataFrame): The GeoDataFrame containing geometry data.
        resolution (int): The H3 resolution to use for polyfilling.
        include_geometry (bool): Whether to include the original geometry in the output.

    Returns:
        GeoDataFrame: A GeoDataFrame with H3 hexagons.
    """
    hexes = []
    gdf = gdf.explode(index_parts=True).reset_index(drop=True)
    for geom in gdf.geometry:
        if geom.is_valid:
            hex_set = h3.geo_to_cells(geom, res=resolution)
            hexes.extend(list(hex_set))

    hex_gdf = pd.DataFrame({"hex": hexes})

    if include_geometry:
        hex_gdf["geometry"] = hex_gdf["hex"].apply(lambda h: get_hex_geometry(h))
        hex_gdf = gpd.GeoDataFrame(hex_gdf, crs=4326)

    return hex_gdf
