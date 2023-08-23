import pysnooper
import geopandas as gpd
import pandas as pd
from geoterminal import utils

import warnings
warnings.filterwarnings('ignore')

def from_csv(path, to_pandas = False, **kwargs):
    data = pd.read_csv(path)
    if not to_pandas:
        data = load_geometries(data, kwargs)
    return data

def load_geometries(data, geometry):
    geom_col = geometry['geometry']
    index_geometry = data[geom_col].to_numpy()
    index_geometry_loaded = [utils.load_wkt(v) for v in index_geometry]
    data[geom_col] = index_geometry_loaded
    return gpd.GeoDataFrame(data.rename(columns = {geom_col: 'geometry'}))

def to_geojson(data, path):
    data.to_file(path, driver = 'GeoJSON')
