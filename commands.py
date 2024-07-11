import click

from functions.conversion import ConversionFunction


@click.command()
@click.argument("input_file")
@click.argument("output_file")
@click.option("--h3_res", type=int, help="H3 hexagon resolution to convert to")
@click.option("--h3_geom", type=bool, help="Wether to include the H3 geometry or not")
@click.option("--input_crs", type=int, help="Input file projection")
@click.option("--output_crs", type=int, help="Output file projection")
@click.option("--buffer_size", type=float, help="Buffer distance to apply")
def convert(
    input_file: str,
    output_file: str,
    h3_res: int = None,
    h3_geom: bool = False,
    input_crs: int = None,
    output_crs: int = None,
    buffer_size: float = None,
) -> None:
    function = ConversionFunction(
        input_file, output_file, h3_res, h3_geom, buffer_size, input_crs, output_crs
    )
    click.echo(f"Converting to {output_file}")
    data = function.load_data()
    data = function.transform_data(data)
    function.export_data(data)
    click.echo(f"Conversion completed successfully.")
