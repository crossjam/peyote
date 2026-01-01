"""IDE subcommand for launching the Peyote IDE."""

import sys

import typer
from loguru import logger

cli = typer.Typer()


@cli.command()
def start(
    file: str = typer.Option(
        None,
        "--file",
        "-f",
        help="Open a specific Python file",
    ),
    example: str = typer.Option(
        None,
        "--example",
        "-e",
        help="Open a specific example sketch",
    ),
) -> None:
    """Launch the Peyote IDE for creating generative art sketches.

    The IDE provides a Processing-like environment for writing and running
    Python sketches with real-time visual feedback.
    """
    logger.info(f"Launching IDE with {file=}, {example=}")

    # Import here to avoid loading Qt unless needed
    from .ide import launch_ide

    # TODO: Handle file and example options
    if file:
        logger.info(f"Would open file: {file}")
    if example:
        logger.info(f"Would open example: {example}")

    # Launch the IDE
    sys.exit(launch_ide())
