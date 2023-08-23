from shapely import wkt

def load_wkt(wkt_string: str):
    return wkt.loads(wkt_string)
