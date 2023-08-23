import pysnooper
import geopandas as gpd
import pandas as pd
from geoterminal import utils

def load_geometries(data):
    index_geometry = data.geometry.to_dict()
    index_geometry_loaded = {k:utils.load_wkt(v) for k,v in index_geometry}
    data.geometry = index_geometry_loaded
    return gpd.GeoDataFrame(data)

def to_geojson(data, path):
    data.to_file(path, driver = 'GeoJSON')
