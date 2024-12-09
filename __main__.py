import click
from commands.edit import Edit
from commands.rename import Rename


@click.group()
def cli():
    """Photo Date command line tools."""
    pass


cli.add_command(Edit)
cli.add_command(Rename)


if __name__ == "__main__":
    cli()
