import geopandas as gpd


def apply_buffer(gdf, buffer_size):
    """
    Apply a buffer operation to the geometry in the GeoDataFrame.

    Parameters:
        gdf (GeoDataFrame): The GeoDataFrame containing geometry data.
        buffer_size (float): The buffer size to apply.

    Returns:
        GeoDataFrame: GeoDataFrame with buffered geometries.
    """
    gdf.geometry = gdf.geometry.buffer(buffer_size)
    return gdf


def reproject_gdf(gdf, output_crs):
    """
    Reproject the GeoDataFrame to a new CRS.

    Parameters:
        gdf (GeoDataFrame): The GeoDataFrame to reproject.
        output_crs (int or str): The target coordinate reference system.

    Returns:
        GeoDataFrame: GeoDataFrame reprojected to the target CRS.
    """
    return gdf.to_crs(crs=output_crs)
