# Peyote IDE

A Processing-like integrated development environment for creating generative art with Python.

## Features

- **Code Editor**: Python syntax highlighting, line numbers, auto-indent
- **Multi-Tab Support**: Organize your sketch across multiple modules
- **Real-Time Display**: See your artwork as it renders at 60 FPS
- **Interactive Console**: View print output and error messages
- **Play/Stop Controls**: Start and stop your sketch with a click
- **Package-Based Architecture**: Modules can import from each other

## Quick Start

Launch the IDE:

```bash
peyote ide start
```

Or open a specific file:

```bash
peyote ide start --file my_sketch.py
```

## Writing Sketches

A basic sketch has two functions:

```python
def setup():
    """Called once when the sketch starts."""
    print("Initializing...")

def draw():
    """Called repeatedly at ~60 FPS for animation."""
    # Your drawing code here
    pass
```

## Architecture

The IDE treats all open tabs as a unified Python package, allowing you to:

- Split complex sketches across multiple files
- Define helper functions and classes in separate modules
- Import code between modules naturally

### Example Multi-Module Sketch

**Tab 1: main.py**
```python
from helpers import calculate_position

def setup():
    print("Starting animation")

def draw():
    x, y = calculate_position()
    # Use coordinates for drawing
```

**Tab 2: helpers.py**
```python
import math

def calculate_position():
    return 100, 200
```

## Components

- `ide_window.py`: Main IDE window with UI layout
- `code_editor.py`: Code editor with syntax highlighting and line numbers
- `syntax_highlighter.py`: Python syntax highlighting
- `display_widget.py`: Real-time and offscreen rendering widgets
- `execution_engine.py`: Executes user sketches with setup()/draw() pattern
- `module_loader.py`: Loads sketch modules using importlib
- `package_manager.py`: Manages package structure for sketches
- `tab_manager.py`: Handles editor tab creation/deletion
- `app_dirs.py`: OS-specific application directory management
- `logging_setup.py`: Logging configuration
- `styles.py`: Dark theme stylesheet

## Technical Details

### Execution Model

1. All tabs are saved as Python modules in a package directory
2. Modules are loaded using `importlib` for proper Python semantics
3. The first tab is designated as the main module
4. `setup()` is called once, `draw()` is called repeatedly
5. stdout/stderr are captured and displayed in the console

### Display System

- **FramebufferWidget**: Real-time display using NumPy-backed QImage
- **OffscreenWidget**: Headless rendering for exporting PNG/GIF
- 60 FPS refresh rate for smooth animation

### Package Structure

Auto-saved sketches are stored in:
- **Linux**: `~/.local/share/dev.pirateninja.peyote/sketches/`
- **macOS**: `~/Library/Application Support/dev.pirateninja.peyote/sketches/`
- **Windows**: `%LOCALAPPDATA%\dev.pirateninja.peyote\sketches\`

## Future Enhancements

- File save/load (beyond auto-save)
- Export to PNG/GIF
- Settings dialog
- Example sketches
- Drawing API (currently sketches must provide their own rendering)
