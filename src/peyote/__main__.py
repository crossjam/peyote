"""peyote CLI implementation.

Create visually attractive computational artifacts
"""

import sys

import typer
from loguru import logger

from .self_subcommand import cli as self_cli
from .settings import Settings

cli = typer.Typer()

cli.add_typer(
    self_cli,
    name="self",
    help="Manage the peyote command.",
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
