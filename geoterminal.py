import click

import commands


@click.group()
def cli() -> None:
    click.echo("Geoterminal is alive!")


cli.add_command(commands.convert)
