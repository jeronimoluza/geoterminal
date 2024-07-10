import click

from functions.conversion import ConversionFunction


@click.command()
@click.argument("input_file")
@click.argument("output_file")
@click.option("--input_crs", type=int, help="Input file projection")
@click.option("--output_crs", type=int, help="Output file projection")
@click.option("--buffer_size", type=float, help="Buffer distance to apply")
def convert(
    input_file: str,
    output_file: str,
    input_crs: int = None,
    output_crs: int = None,
    buffer_size: float = None,
) -> None:
    try:
        function = ConversionFunction(
            input_file, output_file, buffer_size, input_crs, output_crs
        )
        click.echo(f"Converting to {output_file}")
        data = function.load_data()
        data = function.transform_data(data)
        function.export_data(data)
        click.echo(f"Conversion completed successfully.")
    except Exception as e:
        click.echo(f"An error occurred: {e}")
        raise SystemExit(1)
