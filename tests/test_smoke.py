"""Test peyote smoke subcommand."""

import importlib

from typer.testing import CliRunner

main_module_name = "peyote.__main__"
main_module = importlib.import_module(main_module_name)
runner = CliRunner()


def test_smoke_help() -> None:
    """Test the smoke subcommand help flag."""
    result = runner.invoke(main_module.cli, ["smoke", "--help"])
    assert result.exit_code == 0
    assert "smoke" in result.output.lower()
    assert "pyside6" in result.output.lower() or "smoke test" in result.output.lower()
    assert "width" in result.output.lower()
    assert "height" in result.output.lower()


def test_smoke_subcommand_available() -> None:
    """Test that smoke subcommand is registered."""
    result = runner.invoke(main_module.cli, ["--help"])
    assert result.exit_code == 0
    assert "smoke" in result.output.lower()
