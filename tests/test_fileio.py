import os
import tempfile
from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import Point, Polygon

from geoterminal.file_io.file_io import (
    FileHandlerError,
    read_geometry_file,
    read_wkt,
    export_data,
)

# Test fixtures
@pytest.fixture
def sample_wkt():
    return "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"

@pytest.fixture
def sample_gdf():
    polygon = Polygon([(30, 10), (40, 40), (20, 40), (10, 20), (30, 10)])
    return gpd.GeoDataFrame(geometry=[polygon], crs=4326)

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

# Test WKT reading
def test_read_wkt(sample_wkt):
    gdf = read_wkt(sample_wkt)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert gdf.crs.to_epsg() == 4326
    assert len(gdf) == 1
    assert isinstance(gdf.geometry.iloc[0], Polygon)

def test_read_wkt_invalid():
    with pytest.raises(FileHandlerError):
        read_wkt("INVALID WKT")

# Test file reading
def test_read_geometry_file_wkt(sample_wkt):
    gdf = read_geometry_file(sample_wkt)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert gdf.crs.to_epsg() == 4326

def test_read_geometry_file_geojson(temp_dir, sample_gdf):
    file_path = temp_dir / "test.geojson"
    sample_gdf.to_file(file_path, driver="GeoJSON")
    
    gdf = read_geometry_file(file_path)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == len(sample_gdf)

def test_read_geometry_file_csv(temp_dir, sample_gdf):
    file_path = temp_dir / "test.csv"
    # Convert geometry to WKT for CSV export
    df = sample_gdf.copy()
    df['geometry'] = df['geometry'].apply(lambda x: x.wkt)
    df.to_csv(file_path, index=False)
    
    gdf = read_geometry_file(file_path)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == len(sample_gdf)

def test_read_geometry_file_invalid():
    with pytest.raises(FileHandlerError):
        read_geometry_file("nonexistent.file")

# Test file exporting
def test_export_geojson(temp_dir, sample_gdf):
    file_path = temp_dir / "output.geojson"
    export_data(sample_gdf, file_path)
    assert file_path.exists()
    
    # Verify exported file can be read back
    gdf = gpd.read_file(file_path)
    assert len(gdf) == len(sample_gdf)

def test_export_csv(temp_dir, sample_gdf):
    file_path = temp_dir / "output.csv"
    export_data(sample_gdf, file_path)
    assert file_path.exists()
    
    # Verify exported file contains WKT geometry
    gdf = read_geometry_file(file_path)
    assert len(gdf) == len(sample_gdf)

def test_export_invalid_format(temp_dir, sample_gdf):
    with pytest.raises(FileHandlerError):
        export_data(sample_gdf, temp_dir / "output.invalid")
