# Configuration

Generative Computational Hallucinatory Art uses Pydantic Settings for configuration management, which allows you to configure the application using environment variables, configuration files, or both.

## Environment Variables

You can configure peyote using environment variables:

```bash
export PEYOTE_SETTING_NAME=value
peyote [command]
```

## Configuration File

You can also use a configuration file. Create a `.env` file in your project directory:

```bash
# .env
PEYOTE_SETTING_NAME=value
```

## Available Settings

The following settings are available:

### Logging Settings

- `PEYOTE_LOG_LEVEL`: Set the logging level (default: INFO)
- `PEYOTE_LOG_FILE`: Path to log file (default: peyote.log)
### Application Settings

Add your application-specific settings here.

## Priority Order

Settings are loaded in the following priority order (highest to lowest):

1. Environment variables
2. Configuration file (`.env`)
3. Default values

## Example

```bash
# Set log level to DEBUG
export PEYOTE_LOG_LEVEL=DEBUG

# Run the CLI
peyote [command]
```

