# CLI Usage

Generative Computational Hallucinatory Art provides a command-line interface built with Typer.

## Basic Syntax

```bash
peyote [OPTIONS] [COMMAND] [ARGS]...
```

## Global Options

The following options are available for all commands:

- `--help`: Show help message and exit
- `--version`: Show version and exit

## Commands

### Help

Get help for the CLI or any specific command:

```bash
peyote --help
peyote [command] --help
```

### Version

Display the version:

```bash
peyote --version
```

## Self-Subcommands

Generative Computational Hallucinatory Art uses a self-subcommand pattern, where the main command can also act as a subcommand. This provides a clean and intuitive interface.

## Logging

The CLI uses structured logging with Loguru. You can control the log level using:

```bash
peyote --log-level DEBUG [command]
```

## Log Files

By default, logs are also written to `peyote.log` in the current directory.
## Examples

For specific usage examples, see the [Examples](examples.md) page.

## Error Handling

The CLI provides clear error messages and appropriate exit codes:

- `0`: Success
- `1`: General error
- `2`: Command line usage error

## Shell Completion

Generative Computational Hallucinatory Art supports shell completion for bash, zsh, and fish. To enable it:

### Bash

```bash
eval "$(_PEYOTE_COMPLETE=bash_source peyote)"
```

### Zsh

```bash
eval "$(_PEYOTE_COMPLETE=zsh_source peyote)"
```

### Fish

```bash
eval "$(_PEYOTE_COMPLETE=fish_source peyote)"
```