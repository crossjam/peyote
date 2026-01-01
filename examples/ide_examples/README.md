# Peyote IDE Example Sketches

This directory contains example sketches for the Peyote IDE.

## Basic Sketch

The `basic_sketch` example demonstrates the fundamental structure of a Peyote sketch:

- `setup()` function: Called once when the sketch starts
- `draw()` function: Called repeatedly for animation (approximately 60 times per second)

## Running Examples

To open an example in the IDE:

```bash
peyote ide start --example basic_sketch
```

Or simply launch the IDE and use File > Open Project to navigate to an example directory.

## Creating Your Own Sketches

A minimal sketch needs at least a `setup()` or `draw()` function:

```python
def setup():
    """Called once when sketch starts."""
    print("Hello from setup!")

def draw():
    """Called repeatedly for animation."""
    # Your drawing code here
    pass
```

## Multi-Module Projects

You can organize complex sketches across multiple files:

```
my_sketch/
├── __init__.py
├── main.py       # Contains setup() and draw()
├── helpers.py    # Helper functions
└── classes.py    # Custom classes
```

Modules can import from each other:

```python
# In main.py
from helpers import calculate_position

def draw():
    x, y = calculate_position()
    # Use x, y for drawing
```
