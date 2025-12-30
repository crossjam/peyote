# Examples

This page provides practical examples of using Generative Computational Hallucinatory Art.

## Basic Usage

### Getting Help

```bash
# Show main help
peyote --help

# Show help for a specific command
peyote [command] --help
```

### Check Version

```bash
peyote --version
```

## Advanced Usage

### Using with Different Log Levels

```bash
# Run with debug logging
peyote --log-level DEBUG [command]

# Run with minimal logging
peyote --log-level ERROR [command]
```

### Using with Configuration

```bash
# Set configuration via environment variables
export PEYOTE_SETTING_NAME=value
peyote [command]

# Or create a .env file
echo "PEYOTE_SETTING_NAME=value" > .env
peyote [command]
```
## Common Workflows

### Example Workflow 1

```bash
# Step 1: Initialize
peyote init

# Step 2: Process
peyote process --input file.txt

# Step 3: Output
peyote output --format json
```

### Example Workflow 2

```bash
# One-liner example
peyote process --input file.txt --output result.txt --verbose
```

## Error Handling Examples

### Common Errors

```bash
# File not found
peyote process --input nonexistent.txt
# Error: Input file 'nonexistent.txt' not found

# Invalid option
peyote --invalid-option
# Error: No such option: --invalid-option
```

### Debugging

```bash
# Run with debug logging to troubleshoot
peyote --log-level DEBUG process --input file.txt
```

## Integration Examples

### Use in Scripts

```bash
#!/bin/bash
set -e

# Check if peyote is installed
if ! command -v peyote &> /dev/null; then
    echo "peyote is not installed"
    exit 1
fi

# Run the command
peyote process --input "$1" --output "$2"
echo "Processing complete"
```

### Use with Make

```makefile
.PHONY: process
process:
	peyote process --input input.txt --output output.txt

.PHONY: clean
clean:
	rm -f output.txt peyote.log
```

## Performance Tips

- Use appropriate log levels in production
- Process files in batches when possible
- Use configuration files for repeated settings

## Next Steps

- Learn more about the [API Reference](../reference/)
- Check out the [Contributing Guide](../contributing.md)
- Visit the [GitHub repository](https://github.com/crossjam/peyote)