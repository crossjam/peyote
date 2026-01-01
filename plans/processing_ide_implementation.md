# Processing-like IDE Implementation Plan

**Created:** 2025-12-30  
**Last Updated:** 2026-01-01 (Added platformdirs for OS-specific app directories)  
**Status:** Draft for Review

---

## Problem Description

### Issue Reference
This plan addresses the requirements specified in `./plans/processing_ide_plan.md` to create a Processing-like integrated development environment (IDE) for Python-based generative art using PySide6.

### Background
[Processing](https://processing.org) is a popular creative coding environment that enables artists and designers to create generative art through a simple, accessible IDE. The Processing IDE provides:
- An integrated text editor for code
- A visual display window for rendered output
- Play/Stop controls for running sketches
- A console for messages and errors
- Tabbed interface for managing multiple sketches

### Objective
Create a PySide6-based GUI application that provides a Processing-like development environment for Python generative art, specifically designed to:
1. Edit Python code (not Java-like Processing code)
2. Launch and execute Python sketch modules
3. Integrate with the existing `FramebufferWidget` architecture (from `src/peyote/smoke_subcommand.py`) for display
4. Support both real-time display and offline rendering (GIF/PNG export)
5. Provide an intuitive, artist-friendly interface

**Note:** This plan focuses on the IDE UI components and sketch execution mechanism. The drawing API that sketches will use is out of scope for this plan and will be addressed separately.

### Requirements Summary
From the high-level spec:
- **GUI Framework:** PySide6 (Qt for Python)
- **Code Editor:** Python syntax highlighting, line numbers
- **Display Window:** Real-time rendering using existing FramebufferWidget or similar
- **Execution Model:** Load and run user Python modules (sketches)
- **Rendering Modes:** 
  - Interactive mode: real-time display window
  - Offline mode: render to GIF/PNG files
- **Architecture:** Keep class hierarchy flat; avoid over-engineering
- **Integration:** New command group/subcommand in peyote CLI
- **Testing:** Offscreen widget tests with image validation

**Out of Scope:** Implementation of the drawing API itself (functions like `ellipse()`, `rect()`, etc.). The IDE will load and execute sketch modules, but the specific drawing primitives available to sketches will be defined separately.

### Reference Image Analysis
The provided Processing IDE screenshot shows:
- **Title Bar:** Application name and sketch name
- **Toolbar:** Play/Stop buttons, settings icon, Java/mode selector
- **Tabs:** Multiple sketch files can be opened
- **Text Editor:** Syntax-highlighted code with line numbers (left margin)
- **Display Window:** Separate window showing live rendered output
- **Message Area:** Thin strip for status messages
- **Console:** Dark terminal-style output area
- **Footer:** Console/Errors toggle buttons

---

## Implementation Approaches

### Approach 1: Integrated Single-Window IDE (Recommended)

**Overview:** Create a single main window with docked panels for code editor, display, console, and controls.

**Architecture:**
```
MainWindow (QMainWindow)
├── Toolbar (QToolBar)
│   ├── Play Button (QPushButton)
│   ├── Stop Button (QPushButton)
│   └── Settings Button (QPushButton)
├── Central Widget (QSplitter - horizontal)
│   ├── Left Pane (QSplitter - vertical)
│   │   ├── Tab Widget (QTabWidget)
│   │   │   └── Code Editor Tabs (CodeEditorWidget)
│   │   └── Bottom Panel (QSplitter - horizontal)
│   │       ├── Messages Area (QTextEdit)
│   │       └── Console Area (QTextEdit)
│   └── Right Pane
│       └── Display Widget (FramebufferWidget or OffscreenWidget)
```

**Advantages:**
- Single window management (simpler state handling)
- Resizable panes via QSplitter
- Native Qt docking behavior
- Consistent with modern IDE patterns (VS Code, PyCharm)
- Easy to save/restore layout

**Disadvantages:**
- Deviates from Processing's separate display window
- Less screen real estate for display at small window sizes

---

### Approach 2: Multi-Window IDE

**Overview:** Main window for code/controls, separate floating window for display (closer to Processing).

**Status:** Not chosen for initial implementation. Single-window approach (Approach 1) selected instead.

**Advantages:**
- Matches Processing's UX more closely
- Display can be full-screened independently
- Better for dual-monitor setups

**Disadvantages:**
- Two windows to manage (position, focus, close behavior)
- More complex state synchronization
- Display window lifecycle tied to sketch execution

---

### Approach 3: Hybrid with Detachable Display

**Overview:** Start with Approach 1, but allow display pane to be "popped out" into separate window.

**Status:** Future enhancement. Can be added after single-window IDE is stable.

**Advantages:**
- Best of both worlds
- Flexibility for different workflows

**Disadvantages:**
- Most complex implementation
- Docking/undocking state management

---

## Recommended Approach

**Approach 1 (Integrated Single-Window IDE)** is the chosen approach for implementation:
1. Simpler to implement and maintain
2. Aligns with modern IDE conventions
3. Qt's QSplitter provides excellent resizing UX
4. Better for small screens and laptops
5. **Decision confirmed:** Single-window IDE with integrated display pane

**Multi-Tab Architecture:**
- Each tab represents its own Python module within a unified package
- All tabs are treated as a single Python package, allowing cross-tab imports
- Enables easy factoring of helper functions, classes, and utility code across tabs
- Supports modular sketch development with shared code

---

## Alternative Approaches

### Multi-Tab Package Architecture

**Overview:** The IDE treats all open tabs as a unified Python package, enabling modular sketch development.

**Structure:**
```
project_name/
├── __init__.py          # Makes it a Python package
├── main.py              # Tab 1: Main sketch with setup() and draw()
├── helpers.py           # Tab 2: Helper functions
├── classes.py           # Tab 3: Custom classes
└── constants.py         # Tab 4: Shared constants
```

**Benefits:**
- **Code Organization:** Separate concerns across multiple modules
- **Reusability:** Define functions/classes once, use across tabs
- **Cross-Module Imports:** `from helpers import calculate_position`
- **Clean Architecture:** Factor complex sketches into manageable pieces
- **Collaboration:** Team members can work on different modules

**Execution Model:**
- Main module (typically first tab) contains `setup()` and `draw()`
- Other modules provide supporting code
- All modules share the same namespace within the package
- Runtime imports work naturally between modules

---

### Code Execution Strategies

#### Option A: Module Loading via importlib (Recommended)
Load user code as Python modules using `importlib`, then introspect for Processing-like functions (`setup()`, `draw()`, etc.). Code entered in the IDE will be written to package files and loaded using this mechanism.

**Implementation:**
- Save each tab's content to a `.py` file in a project directory
- Use `platformdirs` for managing auto-saved sketch locations
- Create `__init__.py` to establish package structure
- Use `importlib.util.spec_from_file_location()` and `importlib.util.module_from_spec()` to load modules
- Add project directory to `sys.path` for import resolution
- Introspect main module for `setup` and `draw` functions using `hasattr()` or `getattr()`
- Execute functions in controlled manner
- Support module reloading for iterative development

**Note:** The specific functions/API available within sketches (drawing primitives, etc.) is out of scope for this IDE plan.

**Pros:**
- Proper Python module semantics (imports work naturally)
- Better isolation than `exec()`
- Cleaner introspection and error handling
- Supports relative imports and package structure
- Can use standard Python debugging tools
- Module reloading allows iterative development without restart
- OS-appropriate directory management via platformdirs

**Cons:**
- Slightly more complex than `exec()`
- Need to manage project files and directories
- Module caching considerations (must use `importlib.reload()`)

#### Option B: Subprocess Execution
Run user code in a separate Python subprocess.

**Pros:**
- Better isolation
- Can kill runaway processes
- Safer error handling

**Cons:**
- IPC overhead for framebuffer sharing
- More complex architecture
- Slower startup

#### Option C: Direct exec() in Isolated Namespace
Execute user code using Python's `exec()` with a custom namespace containing drawing functions.

**Pros:**
- Simple and direct
- No temporary files needed

**Cons:**
- Security concerns (but acceptable for local dev tool)
- Imports don't work naturally
- Less clean error handling

**Decision:** Use **Option A** (importlib module loading) for initial implementation, with proper module lifecycle management and hot-reloading support.

---

### Editor Widget Options

#### Option A: QPlainTextEdit with Custom Syntax Highlighter
Built-in Qt widget with custom QSyntaxHighlighter subclass.

**Pros:**
- Native Qt integration
- Lightweight
- Full control

**Cons:**
- Basic features only (no autocompletion, goto definition)
- Need to implement line numbers manually

#### Option B: QScintilla (Python-QScintilla)
Advanced code editor component with built-in syntax highlighting.

**Pros:**
- Professional features (folding, markers, autocompletion)
- Battle-tested
- Python syntax support built-in

**Cons:**
- Additional dependency
- More complex API
- Heavier weight

#### Option C: Embedded Monaco Editor (via QWebEngineView)
VS Code's editor in a web view.

**Pros:**
- Best-in-class editor features
- Modern UX

**Cons:**
- Requires QtWebEngine (large dependency)
- Bridge complexity (JS ↔ Python)
- Overkill for use case

**Decision:** Start with **Option A** (QPlainTextEdit) for simplicity. Can upgrade to QScintilla in future if needed.

---

## Implementation Plan

### Phase 1: Core IDE Window Structure and Application Setup
**Goal:** Create the main window shell with all UI components laid out (non-functional) and initialize application directories.

**Tasks:**
- [ ] Set up application directories with platformdirs:
  - [ ] Initialize user data directory for auto-saved sketches
  - [ ] Initialize user config directory for logging configuration
  - [ ] Create directory structure on first run
  - [ ] Set up logging configuration in config directory
- [ ] Create new module: `src/peyote/ide/`
- [ ] Create `ide_window.py` with `ProcessingIDEWindow(QMainWindow)` class
- [ ] Implement toolbar with Play/Stop buttons (QPushButton)
- [ ] Create QSplitter layout:
  - [ ] Left pane with QTabWidget for editors
  - [ ] Right pane for display widget (placeholder QWidget initially)
  - [ ] Bottom panel with Messages/Console (QTextEdit widgets)
- [ ] Add status bar for brief messages
- [ ] Create basic menu bar (File, Edit, Sketch, Help)
- [ ] Apply basic styling (consider dark theme similar to Processing)

**Files to create:**
- `src/peyote/ide/__init__.py`
- `src/peyote/ide/ide_window.py`
- `src/peyote/ide/styles.py` (optional: Qt stylesheet)
- `src/peyote/ide/app_dirs.py` (platformdirs wrapper for app directories)

**Acceptance:**
- Window opens and displays all UI components
- Splitters are draggable and resize correctly
- Window is resizable
- Application directories are created on first run
- Logging configuration directory is initialized

---

### Phase 2: Code Editor Widget
**Goal:** Implement a functional Python code editor with syntax highlighting, line numbers, and multi-tab support.

**Tasks:**
- [ ] Create `code_editor.py` with `CodeEditorWidget(QPlainTextEdit)` class
- [ ] Implement `PythonSyntaxHighlighter(QSyntaxHighlighter)`:
  - [ ] Highlight keywords (def, class, if, for, etc.)
  - [ ] Highlight strings (single/double/triple quotes)
  - [ ] Highlight comments (#)
  - [ ] Highlight numbers
  - [ ] Highlight built-in functions
- [ ] Implement line number area (custom widget in left margin)
- [ ] Add basic text editor features:
  - [ ] Tab key inserts 4 spaces (or configurable)
  - [ ] Auto-indent on new line
  - [ ] Ctrl+/ for comment toggle
- [ ] Integrate into QTabWidget in main window
- [ ] Implement tab management:
  - [ ] New tab (Ctrl+N)
  - [ ] Close tab (Ctrl+W)
  - [ ] Switch tabs (Ctrl+Tab)
  - [ ] Module naming: "module_1", "module_2", etc. (or user-defined)
  - [ ] Modified indicator (asterisk in tab title)
- [ ] **Implement package structure for tabs:**
  - [ ] Create a unique package directory for the current sketch project
  - [ ] Each tab corresponds to a Python module file in that package
  - [ ] Generate `__init__.py` to make it a proper Python package
  - [ ] Track mapping between tabs and module files
  - [ ] Support cross-module imports (e.g., `from module_2 import helper_function`)

**Files to create:**
- `src/peyote/ide/code_editor.py`
- `src/peyote/ide/syntax_highlighter.py`
- `src/peyote/ide/line_numbers.py`
- `src/peyote/ide/tab_manager.py` (manages tab-to-module mapping)

**Acceptance:**
- Can type Python code with syntax highlighting
- Line numbers display correctly
- Multiple tabs can be created and managed
- Tab switching works
- Each tab has a unique module name
- Tabs are saved as separate module files in a package directory

---

### Phase 3: Display Widget Integration
**Goal:** Integrate FramebufferWidget for real-time display and create an offscreen rendering variant.

**Tasks:**
- [ ] Refactor existing `FramebufferWidget` from `smoke_subcommand.py`:
  - [ ] Extract to `src/peyote/ide/display_widget.py`
  - [ ] Make frame update method more generic (accept callable)
  - [ ] Remove hardcoded animation, make it driven by external code
- [ ] Create `OffscreenWidget` class:
  - [ ] No QWidget inheritance (pure rendering)
  - [ ] Same NumPy buffer + QImage pattern
  - [ ] Render to QImage without display
  - [ ] Implement `save_png(path)` method
  - [ ] Implement `save_gif(path, frames)` method (using PIL/Pillow)
- [ ] Integrate `FramebufferWidget` into IDE right pane
- [ ] Add display size controls in toolbar (e.g., 640x360, 800x600, 1920x1080)

**Files to create:**
- `src/peyote/ide/display_widget.py` (move and refactor FramebufferWidget)
- `src/peyote/ide/offscreen_widget.py`

**Acceptance:**
- Display widget shows in right pane
- Can be resized with splitter
- Offscreen widget can render and save PNG

---

### Phase 4: Code Execution Engine
**Goal:** Load and execute user Python sketch modules as a unified package using importlib.

**Tasks:**
- [ ] Create `execution_engine.py` with `SketchExecutor` class
- [ ] Implement package-based file management with platformdirs:
  - [ ] Use `platformdirs.user_data_dir("dev.pirateninja.peyote", "pirateninja")` for auto-saved sketches
  - [ ] Create sketches directory: `{data_dir}/sketches/project_name/`
  - [ ] Write each tab's content to a separate `.py` file (e.g., `module_1.py`, `module_2.py`)
  - [ ] Generate `__init__.py` to make it a proper Python package
  - [ ] Support user-defined module names (editable tab names)
  - [ ] Track whether project is user-saved or auto-saved to app directory
- [ ] Implement package loading with importlib:
  - [ ] Add project directory to `sys.path` for import resolution
  - [ ] Load main module using `importlib.util.spec_from_file_location()`
  - [ ] Use `importlib.util.module_from_spec()` to create module
  - [ ] Execute module with `spec.loader.exec_module()`
  - [ ] Introspect for `setup` and `draw` functions using `hasattr()`
  - [ ] Support module reloading with `importlib.reload()` for iterative development
  - [ ] Support cross-module imports (modules can import from sibling modules in package)
- [ ] Implement `SketchExecutor.load_and_run()`:
  - [ ] Save all tab contents to their respective module files
  - [ ] Identify the "main" module (first tab or designated main)
  - [ ] Load main module using importlib
  - [ ] Validate that main module has required functions
  - [ ] Call user's `setup()` once (if present)
  - [ ] Start timer to call user's `draw()` at ~60fps (if present)
  - [ ] Handle exceptions gracefully with full traceback
  - [ ] Route print statements to console widget (capture stdout)
- [ ] Implement module lifecycle management:
  - [ ] Stop previous sketch before loading new one
  - [ ] Reload all modified modules when Play is pressed
  - [ ] Cleanup old modules from sys.modules
  - [ ] Handle reload on code changes (hot-reload)
- [ ] Integrate with Display Widget:
  - [ ] Connect executor to FramebufferWidget
  - [ ] Allow sketch module to access the display widget for rendering
  - [ ] Update display after each draw() call
- [ ] Implement Play/Stop button functionality:
  - [ ] Play: save all tabs to package, load main module, start execution
  - [ ] Stop: halt execution, unload modules, clear display

**Files to create:**
- `src/peyote/ide/execution_engine.py`
- `src/peyote/ide/module_loader.py` (helper for importlib operations)
- `src/peyote/ide/package_manager.py` (manages package structure and files)

**Acceptance:**
- Can write sketch across multiple tabs
- Modules can import from each other (e.g., `from module_2 import MyClass`)
- Play button runs the main module (first tab or designated)
- Stop button halts execution and unloads all modules
- Sketch code can access display widget for rendering
- Errors show in console with proper tracebacks indicating which module failed
- Can reload sketch after code changes in any tab (hot-reload)
- Imports work naturally in sketch code (e.g., `import math`)
- Helper functions/classes defined in one tab can be used in another

**Note:** The specific API that sketches use for drawing is out of scope. This phase focuses on the package-based module loading and execution infrastructure.

---

### Phase 5: Console and Error Handling
**Goal:** Provide useful feedback via console and message areas.

**Tasks:**
- [ ] Implement console output capture:
  - [ ] Redirect stdout/stderr during execution
  - [ ] Append to Console QTextEdit
  - [ ] Auto-scroll to bottom
  - [ ] Colorize errors (red text)
- [ ] Implement error handling:
  - [ ] Catch exceptions in setup()/draw()
  - [ ] Display traceback in console
  - [ ] Show brief error in message area
  - [ ] Highlight error line in editor (optional: red background)
- [ ] Add console controls:
  - [ ] Clear console button
  - [ ] Copy output button
  - [ ] Console/Errors toggle (filter view)
- [ ] Add message area for status:
  - [ ] "Sketch started"
  - [ ] "Sketch stopped"
  - [ ] "Rendering to file..."
  - [ ] "Saved to output.png"

**Files modified:**
- `src/peyote/ide/ide_window.py`
- `src/peyote/ide/execution_engine.py`

**Acceptance:**
- print() statements appear in console
- Exceptions show full traceback
- Console can be cleared
- Status messages appear in message area

---

### Phase 6: File Operations
**Goal:** Load and save Python sketch packages (multi-file projects).

**Tasks:**
- [ ] Implement File menu actions:
  - [ ] New Project (Ctrl+N) - create new multi-tab project
  - [ ] Open Project (Ctrl+O) - load existing project directory
  - [ ] Save Project (Ctrl+S) - save all tabs to project directory
  - [ ] Save Project As (Ctrl+Shift+S) - save with new project name
  - [ ] Open File in Tab - add single .py file as new tab
  - [ ] Save Tab As - save individual tab to separate file
  - [ ] Recent projects list
  - [ ] Exit (Ctrl+Q)
- [ ] Implement project file management:
  - [ ] Project directory structure: `project_name/` with module files and `__init__.py`
  - [ ] Track project path and individual module file paths
  - [ ] Update window title with project name
  - [ ] Prompt to save on close if any tab is modified
  - [ ] **User-saved projects:** Default to `~/peyote-projects/` or user-chosen location
  - [ ] **Auto-saved projects:** Use platformdirs data directory for unsaved sketches
  - [ ] Auto-save project structure on tab changes to app directory
  - [ ] Allow promoting auto-saved project to user-saved location (Save As)
- [ ] Implement tab/module file synchronization:
  - [ ] Map each tab to its module file
  - [ ] Save tab content to corresponding module file
  - [ ] Load module files into tabs when opening project
  - [ ] Track which tabs have unsaved changes
- [ ] Create example projects:
  - [ ] `examples/basic_project/` - single module with setup() and draw()
  - [ ] `examples/multi_module/` - multiple tabs with shared utilities
  - [ ] `examples/animation/` - animation example using helper modules
- [ ] Add "Examples" menu to load bundled example projects

**Files to create:**
- `examples/basic_project/__init__.py`
- `examples/basic_project/main.py`
- `examples/multi_module/__init__.py`
- `examples/multi_module/main.py`
- `examples/multi_module/helpers.py`
- `examples/animation/__init__.py`
- `examples/animation/main.py`
- `src/peyote/ide/project_manager.py` (handles project loading/saving)

**Files modified:**
- `src/peyote/ide/ide_window.py`

**Acceptance:**
- Can create new projects with multiple tabs
- Can open and save project directories
- Each tab corresponds to a module file in the project
- Unsaved changes are detected per tab
- Example projects load correctly with all modules in separate tabs
- Tabs maintain their names and content when project is reopened
- Can add new tabs (new modules) to existing project
- Example sketches load correctly

---

### Phase 7: Export Functionality (Offline Rendering)
**Goal:** Render sketches to PNG and GIF files without display window.

**Tasks:**
- [ ] Add Export menu with actions:
  - [ ] Export Frame (PNG)
  - [ ] Export Animation (GIF)
- [ ] Implement PNG export:
  - [ ] Run setup() + single draw() call on OffscreenWidget
  - [ ] Save QImage to PNG file
  - [ ] Show file save dialog
- [ ] Implement GIF export:
  - [ ] Prompt for frame count (e.g., 60, 120, 300)
  - [ ] Run setup() + multiple draw() calls
  - [ ] Capture each frame to PIL Image
  - [ ] Save as animated GIF
  - [ ] Show progress dialog
- [ ] Add Pillow dependency for GIF encoding:
  - [ ] Update `pyproject.toml`
  - [ ] Use `PIL.Image.save(images, save_all=True, append_images=...)`

**Files to create:**
- `src/peyote/ide/export.py`

**Files modified:**
- `src/peyote/ide/ide_window.py`
- `pyproject.toml` (add Pillow dependency)

**Acceptance:**
- Can export single frame as PNG
- Can export animation as GIF
- Files open correctly in image viewers

---

### Phase 8: CLI Integration
**Goal:** Launch the IDE via peyote CLI.

**Tasks:**
- [ ] Create new subcommand: `src/peyote/ide_subcommand.py`
- [ ] Implement CLI with typer:
  - [ ] `peyote ide` - launch IDE
  - [ ] `peyote ide --file sketch.py` - open specific file
  - [ ] `peyote ide --example basic` - open example
- [ ] Integrate into `__main__.py`:
  - [ ] Add `ide_cli` to main CLI typer
- [ ] Handle QApplication lifecycle correctly:
  - [ ] Ensure only one QApplication instance
  - [ ] Exit cleanly with sys.exit(app.exec())

**Files to create:**
- `src/peyote/ide_subcommand.py`

**Files modified:**
- `src/peyote/__main__.py`

**Acceptance:**
- `peyote ide` launches the IDE
- `peyote ide --file example.py` opens file
- Exits cleanly on window close

---

### Phase 9: Settings and Preferences
**Goal:** Persist user preferences and add settings dialog.

**Tasks:**
- [ ] Implement settings system using QSettings:
  - [ ] Window size and position
  - [ ] Splitter positions
  - [ ] Last opened files
  - [ ] Editor preferences (tab size, theme)
  - [ ] Default display size
- [ ] Create settings dialog:
  - [ ] Editor tab (font, size, tab width, theme)
  - [ ] Display tab (default size, FPS)
  - [ ] Export tab (default format, quality)
- [ ] Add Preferences menu item (Ctrl+,)
- [ ] Load settings on startup, save on exit

**Files to create:**
- `src/peyote/ide/settings_dialog.py`
- `src/peyote/ide/preferences.py`

**Files modified:**
- `src/peyote/ide/ide_window.py`

**Acceptance:**
- Window position/size restored on restart
- Settings dialog allows customization
- Preferences persist between sessions

---

### Phase 10: Polish and UX Improvements
**Goal:** Improve visual design and user experience.

**Tasks:**
- [ ] Apply consistent styling:
  - [ ] Dark theme similar to Processing (optional)
  - [ ] Custom icons for Play/Stop buttons
  - [ ] Consistent colors across widgets
- [ ] Add keyboard shortcuts:
  - [ ] Ctrl+R: Run (same as Play)
  - [ ] Ctrl+.: Stop
  - [ ] Ctrl+E: Export
  - [ ] F11: Fullscreen display
- [ ] Improve editor UX:
  - [ ] Current line highlighting
  - [ ] Matching bracket highlighting
  - [ ] Find/Replace (Ctrl+F, Ctrl+H)
- [ ] Add tooltips to toolbar buttons
- [ ] Add About dialog with version info
- [ ] Add Help menu with documentation links

**Files modified:**
- `src/peyote/ide/ide_window.py`
- `src/peyote/ide/code_editor.py`
- `src/peyote/ide/styles.py`

**Acceptance:**
- IDE looks polished and professional
- All shortcuts work
- UX feels smooth and responsive

---

---

## Testing Strategy

### Unit Tests

**Editor Tests** (`tests/test_code_editor.py`):
- [ ] Syntax highlighting correctly highlights Python keywords
- [ ] Line numbers update on text change
- [ ] Tab insertion works
- [ ] Comment toggle works

**Execution Engine Tests** (`tests/test_execution_engine.py`):
- [ ] User code loads as Python module
- [ ] setup() called once, draw() called repeatedly (if present in sketch)
- [ ] Exceptions are caught and reported
- [ ] stdout/stderr captured correctly
- [ ] Module reloading works correctly

### Integration Tests

**Offscreen Rendering Tests** (`tests/test_offscreen_rendering.py`):
- [ ] Create OffscreenWidget
- [ ] Run simple sketch that renders something
- [ ] Save PNG
- [ ] Verify PNG exists and has correct dimensions
- [ ] Load PNG with PIL and verify it was modified from blank
- [ ] Test GIF export with multiple frames
- [ ] Verify GIF animation

**Sketch Execution Tests** (`tests/test_sketch_execution.py`):
- [ ] Execute example sketches without errors
- [ ] Verify module loading and unloading
- [ ] Test error handling (syntax errors, runtime errors)
- [ ] Test hot-reload functionality

### Manual Testing

**IDE Testing Checklist:**
- [ ] Launch IDE and verify window layout
- [ ] Create new sketch, type code, run it
- [ ] Stop sketch mid-execution
- [ ] Open and save files
- [ ] Create multiple tabs
- [ ] Export PNG and GIF
- [ ] Adjust settings and verify persistence
- [ ] Test all keyboard shortcuts
- [ ] Test example sketches
- [ ] Test error handling (introduce intentional errors)
- [ ] Test on different OS (macOS, Linux, Windows if possible)

### Performance Testing
- [ ] Measure frame rate with simple sketch (~60 FPS target)
- [ ] Test with complex sketch (many shapes per frame)
- [ ] Test with large canvas (1920x1080)
- [ ] Verify no memory leaks (run for extended period)

### Reference Image Tests (Automated)
Create a suite of canonical sketches and reference images to test the execution infrastructure:
1. **test_module_loading.py**: Simple sketch that renders something
   - Verify module loads and executes without error
   - Compare output PNG to verify rendering occurred
2. **test_animation.py**: Animated sketch (10 frames)
   - Verify frame_count increments
   - Verify display updates each frame

**Test Framework:**
- Use pytest
- Use PIL for image comparison
- Use `pytest-qt` for Qt widget testing
- Store reference images in `tests/reference_images/`
- Generate test images in `tests/output_images/`
- Basic validation that rendering occurred (image changed from blank)

---

## Dependencies

### Required
- **PySide6**: Qt bindings for Python (already in dependencies)
- **numpy**: Array manipulation (already in dependencies)
- **Pillow**: GIF export and image comparison in tests
- **platformdirs**: OS-specific user application directories
- **loguru**: Logging (already in dependencies)
- **typer**: CLI framework (already in dependencies)

### Development
- **pytest**: Testing framework (already in dev dependencies)
- **pytest-qt**: Qt testing utilities
- **pytest-cov**: Coverage reporting (already in dev dependencies)

### Add to pyproject.toml
```toml
[project]
dependencies = [
    # ... existing ...
    "pillow",       # Add this
    "platformdirs", # Add this
]

[dependency-groups]
dev = [
    # ... existing ...
    "pytest-qt",  # Add this
]
```

### Application Directories

The IDE uses `platformdirs` to manage OS-specific user application directories with the app name `dev.pirateninja.peyote`:

**User Data Directory** (for sketch packages):
- **Linux:** `~/.local/share/dev.pirateninja.peyote/`
- **macOS:** `~/Library/Application Support/dev.pirateninja.peyote/`
- **Windows:** `%LOCALAPPDATA%\dev.pirateninja.peyote\`

**User Config Directory** (for logging configuration):
- **Linux:** `~/.config/dev.pirateninja.peyote/`
- **macOS:** `~/Library/Application Support/dev.pirateninja.peyote/`
- **Windows:** `%LOCALAPPDATA%\dev.pirateninja.peyote\`

**Usage:**
```python
from platformdirs import user_data_dir, user_config_dir

# Sketch packages not explicitly saved by user
data_dir = user_data_dir("dev.pirateninja.peyote", "pirateninja")
sketches_dir = Path(data_dir) / "sketches"

# Logging configuration files
config_dir = user_config_dir("dev.pirateninja.peyote", "pirateninja")
log_config = Path(config_dir) / "logging.conf"
```

---

## Security and Safety Considerations

### Code Execution Security
**Risk:** User code loaded as Python modules has full access to Python runtime and can import any module.

**Mitigations:**
1. **Documentation:** Clearly document that the IDE is a local development tool, not for running untrusted code.
2. **Module Isolation:** Each sketch runs as a separate module in a controlled namespace.
3. **Application Directory Management:** Sketch files stored in OS-appropriate application directories managed by `platformdirs`.
4. **No Automatic Execution:** Sketches only run when user explicitly clicks Play button.
5. **Future Enhancement:** Consider restricted execution environment (e.g., RestrictedPython) if needed.

**Advantages of importlib approach:**
- More predictable behavior than `exec()`
- Standard Python module semantics for error handling
- Better stack traces and debugging
- Imports work naturally (user code can `import math`, etc.)

**Decision:** For v1, this is acceptable as a local dev tool. Users are running their own code with full Python capabilities, which is appropriate for a creative coding IDE.

### File System Access
User sketches can open files, write files, etc.

**Mitigations:**
1. Default save location is user's home directory or designated sketches folder.
2. No automatic execution of files on open.
3. Auto-saved sketches stored in OS-appropriate application data directory via `platformdirs`.
4. User-saved projects stored in user-chosen locations.

### Memory Safety
NumPy buffer shared between Python and Qt must not cause segfaults.

**Mitigations:**
1. Keep reference to NumPy array (`_buf` attribute) to prevent GC.
2. Ensure buffer is not resized while QImage references it.
3. Follow pattern from existing `FramebufferWidget`.

---

## Satisfaction Criteria

The implementation will be considered complete and successful when:

### Functional Requirements
- ✅ IDE launches via `peyote ide` command
- ✅ User can write Python code with syntax highlighting
- ✅ User can run code with Play button
- ✅ Visual output displays in real-time in display pane
- ✅ Console shows print output and errors
- ✅ User can save and load .py sketch files
- ✅ User can export single frame as PNG
- ✅ User can export animation as GIF
- ✅ Example sketches are included and functional

### Non-Functional Requirements
- ✅ Frame rate is ~60 FPS for simple sketches
- ✅ UI is responsive (no freezing during execution)
- ✅ Window layout is resizable and intuitive
- ✅ Settings persist between sessions
- ✅ Code is well-documented and maintainable
- ✅ Test coverage >80% for core modules

### User Experience
- ✅ A beginner can open the IDE, load an example, and run it within 1 minute
- ✅ A user can create a simple animation (bouncing ball) within 5 minutes
- ✅ Error messages are clear and actionable
- ✅ Keyboard shortcuts follow common IDE conventions

### Testing
- ✅ All automated tests pass
- ✅ Offscreen rendering test successfully generates and validates PNG
- ✅ Example sketches run without errors
- ✅ Manual testing checklist completed

---

## Estimated Effort

### Development Time (for experienced Python/Qt developer)
- **Phase 1-2 (UI Shell + Editor):** 2-3 days
- **Phase 3-4 (Display + Execution):** 3-4 days
- **Phase 5-6 (Console + Files):** 2-3 days
- **Phase 7-8 (Export + CLI):** 2-3 days
- **Phase 9-10 (Settings + Polish):** 2-3 days
- **Testing:** 2-3 days (parallel with development)

**Total:** 13-19 days (2.5-4 weeks)

### Lines of Code Estimate
- **IDE Window:** ~300 lines
- **Code Editor:** ~400 lines
- **Display Widgets:** ~300 lines
- **Execution Engine:** ~400 lines
- **File Operations:** ~200 lines
- **Export:** ~200 lines
- **CLI Integration:** ~100 lines
- **Settings:** ~200 lines
- **Tests:** ~600 lines

**Total:** ~2,700 lines

**Note:** Drawing API implementation (out of scope) would add an estimated ~500 lines.

---

## Future Enhancements (Out of Scope for v1)

1. **Drawing API Implementation:** Design and implement the Processing-like drawing primitives that sketches will use (ellipse, rect, line, etc.)
2. **Debugger Integration:** Breakpoints, step through, variable inspection
3. **Variable Inspector Panel:** Live view of sketch variables
4. **Performance Profiler:** Identify slow draw() calls
5. **Snippet Library:** Pre-built code templates
6. **Community Sharing:** Upload/download sketches from web
7. **3D Rendering:** OpenGL-based 3D drawing capabilities
8. **Video Export:** MP4/MOV export with audio
9. **Multi-file Projects:** Import local modules in sketches
10. **Git Integration:** Version control for sketches
11. **Live Coding Mode:** Code changes reflected immediately without restart

---

## Open Questions for Clarification

1. **Display Widget Architecture:** ✓ **Decided**
   - Single-window IDE with integrated display pane (not detachable in v1)
   - Can be added as future enhancement if needed

2. **Frame Rate Control:**
   - Should frame rate be fixed at 60 FPS or configurable?
   - **Recommendation:** Start with fixed 60 FPS, make configurable later if needed.

3. **Error Recovery:**
   - When draw() throws exception, should we halt execution or keep running and show error?
   - **Recommendation:** Halt execution, show error, allow user to fix and restart.

4. **Main Module Designation:**
   - Should the first tab always be the main module, or can users designate which tab is main?
   - **Recommendation:** Start with first tab as main, add designation UI later if needed.

5. **Sketch Module Interface:**
   - How should sketches access the display widget for rendering?
   - Should there be a standard module/API they import, or is it passed as a parameter?
   - **Recommendation:** To be determined based on drawing API design (out of scope for this plan).

---

## References

- **PySide6 Documentation:** https://doc.qt.io/qtforpython-6/
- **Processing IDE Overview:** https://processing.org/environment
- **Processing Reference:** https://processing.org/reference
- **Qt Examples:** https://doc.qt.io/qtforpython-6/examples/index.html
- **QSyntaxHighlighter:** https://doc.qt.io/qtforpython-6/PySide6/QtGui/QSyntaxHighlighter.html
- **Pillow GIF Export:** https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif

---

## Version History

- **v1.0 (2025-12-30):** Initial draft for review
- **v1.1 (2025-12-30):** Updated code execution strategy from `exec()` to importlib-based module loading for better isolation, natural import support, and cleaner error handling
- **v1.2 (2025-12-30):** Removed Drawing API implementation from scope; focused plan on IDE UI components and sketch module loading/execution infrastructure. Drawing API design deferred to separate effort.
- **v1.3 (2025-12-31):** Confirmed single-window IDE approach. Enhanced multi-tab architecture: all tabs treated as unified Python package enabling cross-module imports, shared utilities, and modular sketch development. Updated Phases 2, 4, and 6 to reflect package-based project structure.
- **v1.4 (2026-01-01):** Added `platformdirs` dependency for OS-specific application directory management. App name: `dev.pirateninja.peyote`. Auto-saved sketches stored in user data directory, logging configuration in user config directory. Updated Phases 1, 4, 6 and Dependencies section.
