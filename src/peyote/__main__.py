"""peyote CLI implementation.

Create visually attractive computational artifacts
"""

import sys

import typer
from loguru import logger

from .ide_subcommand import cli as ide_cli
from .self_subcommand import cli as self_cli
from .settings import Settings
from .smoke_subcommand import cli as smoke_cli

cli = typer.Typer()

cli.add_typer(
    ide_cli,
    name="ide",
    help="Launch the Peyote IDE for creating generative art sketches.",
)

cli.add_typer(
    self_cli,
    name="self",
    help="Manage the peyote command.",
)

cli.add_typer(
    smoke_cli,
    name="smoke",
    help="Run smoke test of Pyside6 integration.",
)


@cli.callback(invoke_without_command=True, no_args_is_help=True)
def global_callback(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False,
        "--debug",
        "-D",
        help="Enable debugging output.",
    ),
) -> None:
    """Create visually attractive computational artifacts"""
    ctx.obj = Settings()
    debug = debug or ctx.obj.debug
    (logger.enable if debug else logger.disable)("peyote")
    logger.add("peyote.log")
    logger.info(f"{debug=}")


if __name__ == "__main__":
    sys.exit(cli())
