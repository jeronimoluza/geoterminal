import geoterminal
import fire


import pysnooper


class TerminalTool:
    def __init__(self):
        # Initialize any resources or configurations here
        pass
    
    def hello(self, name="World"):
        """Print a greeting message."""
        print(f"Hello, {name}!")
    
    def csv_to_geojson(self, path, outfile, **kwargs):
        """Converts a CSV into a JSON"""
        data = geoterminal.geom.loading.from_csv(path, **kwargs)
        geoterminal.geom.loading.to_geojson(data, outfile)

    # Define more methods for your tool as needed
    def test_loading(self):
        data = geoterminal.geom.loading.from_csv('metadata_variation.csv', to_pandas = True)
        d1 = data.dtypes
        data = geoterminal.geom.loading.from_csv('metadata_variation.csv', geometry = 'region_shapefile_wkt')
        d2 = data.dtypes
        assert d1.ne(d2).any()

def main():
    terminal_tool = TerminalTool()
    fire.Fire(terminal_tool)

if __name__ == "__main__":
    main()

