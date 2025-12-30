# Processing-like IDE Implementation Plan

**Created:** 2025-12-30  
**Last Updated:** 2025-12-30 (Revised code execution strategy to use importlib)  
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
2. Execute user code against a framebuffer for real-time visualization
3. Integrate with the existing `FramebufferWidget` architecture (from `src/peyote/smoke_subcommand.py`)
4. Support both real-time display and offline rendering (GIF/PNG export)
5. Provide an intuitive, artist-friendly interface

### Requirements Summary
From the high-level spec:
- **GUI Framework:** PySide6 (Qt for Python)
- **Code Editor:** Python syntax highlighting, line numbers
- **Display Window:** Real-time rendering using existing FramebufferWidget or similar
- **Execution Model:** Run user Python code with access to drawing primitives
- **Rendering Modes:** 
  - Interactive mode: real-time display window
  - Offline mode: render to GIF/PNG files
- **Architecture:** Keep class hierarchy flat; avoid over-engineering
- **Integration:** New command group/subcommand in peyote CLI
- **Testing:** Offscreen widget tests with image validation

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

**Architecture:**
```
MainWindow (QMainWindow)
├── Toolbar (QToolBar)
├── Tab Widget (QTabWidget) - Code Editors
└── Bottom Panel (QSplitter)
    ├── Messages Area (QTextEdit)
    └── Console Area (QTextEdit)

DisplayWindow (QWidget)
└── FramebufferWidget
```

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

**Advantages:**
- Best of both worlds
- Flexibility for different workflows

**Disadvantages:**
- Most complex implementation
- Docking/undocking state management

---

## Recommended Approach

**Approach 1 (Integrated Single-Window IDE)** is recommended for the initial implementation because:
1. Simpler to implement and maintain
2. Aligns with modern IDE conventions
3. Qt's QSplitter provides excellent resizing UX
4. Can evolve to Approach 3 in future if needed
5. Better for small screens and laptops

---

## Alternative Approaches

### Code Execution Strategies

#### Option A: Module Loading via importlib (Recommended)
Load user code as Python modules using `importlib`, then introspect for Processing-like functions (`setup()`, `draw()`, etc.). Code entered in the IDE will be written to temporary files and loaded using this mechanism.

**Implementation:**
- Save editor content to temporary `.py` file in a temp directory
- Use `importlib.util.spec_from_file_location()` and `importlib.util.module_from_spec()` to load module
- Introspect module for `setup` and `draw` functions using `hasattr()` or `getattr()`
- Execute functions in controlled manner
- Support module reloading for iterative development

**Pros:**
- Proper Python module semantics (imports work naturally)
- Better isolation than `exec()`
- Cleaner introspection and error handling
- Supports relative imports and package structure
- Can use standard Python debugging tools
- Module reloading allows iterative development without restart

**Cons:**
- Slightly more complex than `exec()`
- Need to manage temporary files
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

### Phase 1: Core IDE Window Structure
**Goal:** Create the main window shell with all UI components laid out (non-functional).

**Tasks:**
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

**Acceptance:**
- Window opens and displays all UI components
- Splitters are draggable and resize correctly
- Window is resizable

---

### Phase 2: Code Editor Widget
**Goal:** Implement a functional Python code editor with syntax highlighting and line numbers.

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
  - [ ] "Untitled-1", "Untitled-2" naming
  - [ ] Modified indicator (asterisk in tab title)

**Files to create:**
- `src/peyote/ide/code_editor.py`
- `src/peyote/ide/syntax_highlighter.py`
- `src/peyote/ide/line_numbers.py`

**Acceptance:**
- Can type Python code with syntax highlighting
- Line numbers display correctly
- Multiple tabs can be created and managed
- Tab switching works

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
**Goal:** Execute user Python code and provide drawing API using module loading.

**Tasks:**
- [ ] Create `execution_engine.py` with `SketchExecutor` class
- [ ] Implement temporary file management:
  - [ ] Create temp directory for sketch modules (e.g., `~/.peyote/sketches/`)
  - [ ] Write editor content to `.py` file in temp directory
  - [ ] Generate unique module names to avoid conflicts
- [ ] Implement module loading with importlib:
  - [ ] Use `importlib.util.spec_from_file_location()` to create module spec
  - [ ] Use `importlib.util.module_from_spec()` to load module
  - [ ] Execute module with `spec.loader.exec_module()`
  - [ ] Introspect module for `setup` and `draw` functions using `hasattr()`
  - [ ] Support module reloading with `importlib.reload()` for iterative development
- [ ] Design user-facing drawing API (Processing-like functions):
  - [ ] `setup()` - called once at start
  - [ ] `draw()` - called every frame
  - [ ] `size(width, height)` - set canvas size
  - [ ] `background(r, g, b)` - clear with color
  - [ ] `fill(r, g, b)` - set fill color
  - [ ] `stroke(r, g, b)` - set stroke color
  - [ ] `no_stroke()` - disable stroke
  - [ ] `no_fill()` - disable fill
  - [ ] `ellipse(x, y, w, h)` - draw ellipse
  - [ ] `rect(x, y, w, h)` - draw rectangle
  - [ ] `line(x1, y1, x2, y2)` - draw line
  - [ ] `point(x, y)` - draw point
  - [ ] `text(string, x, y)` - draw text
  - [ ] Mouse/keyboard state variables: `mouse_x`, `mouse_y`, `mouse_pressed`
  - [ ] Frame state: `frame_count`
- [ ] Implement drawing API module injection:
  - [ ] Make drawing API available as importable module (e.g., `from peyote.sketch import *`)
  - [ ] Or inject into module's namespace before execution
- [ ] Implement `SketchExecutor.load_and_run(code_string)`:
  - [ ] Save code to temporary file
  - [ ] Load module using importlib
  - [ ] Validate that module has required functions
  - [ ] Call user's `setup()` once (if present)
  - [ ] Start timer to call user's `draw()` at ~60fps (if present)
  - [ ] Handle exceptions gracefully with full traceback
  - [ ] Route print statements to console widget (capture stdout)
- [ ] Implement module lifecycle management:
  - [ ] Stop previous sketch before loading new one
  - [ ] Cleanup old modules and temp files
  - [ ] Handle reload on code changes (hot-reload)
- [ ] Integrate with Display Widget:
  - [ ] Connect executor to FramebufferWidget
  - [ ] Pass QPainter to drawing functions
  - [ ] Update display after each draw() call
- [ ] Implement Play/Stop button functionality:
  - [ ] Play: save code, load module, start execution
  - [ ] Stop: halt execution, unload module, clear display

**Files to create:**
- `src/peyote/ide/execution_engine.py`
- `src/peyote/ide/drawing_api.py` (or `src/peyote/sketch/__init__.py`)
- `src/peyote/ide/module_loader.py` (helper for importlib operations)

**Acceptance:**
- Can write simple sketch with setup() and draw()
- Play button runs the sketch by loading it as a module
- Stop button halts execution and unloads module
- Drawing functions render to display
- Errors show in console with proper tracebacks
- Can reload sketch after code changes (hot-reload)
- Imports work naturally in sketch code (e.g., `import math`)

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
**Goal:** Load and save Python sketch files.

**Tasks:**
- [ ] Implement File menu actions:
  - [ ] New (Ctrl+N) - clear editor
  - [ ] Open (Ctrl+O) - file dialog, load .py file
  - [ ] Save (Ctrl+S) - save current tab
  - [ ] Save As (Ctrl+Shift+S) - save with new name
  - [ ] Recent files list
  - [ ] Exit (Ctrl+Q)
- [ ] Implement sketch file management:
  - [ ] Track file path per tab
  - [ ] Update window title with current file name
  - [ ] Prompt to save on close if modified
  - [ ] Default save location (~/peyote-sketches or similar)
- [ ] Create example sketches:
  - [ ] `examples/basic_shapes.py`
  - [ ] `examples/animation.py`
  - [ ] `examples/mouse_interaction.py`
- [ ] Add "Examples" menu to load bundled sketches

**Files to create:**
- `examples/basic_shapes.py`
- `examples/animation.py`
- `examples/mouse_interaction.py`

**Files modified:**
- `src/peyote/ide/ide_window.py`

**Acceptance:**
- Can open and save .py files
- Unsaved changes are detected
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

### Phase 11: Advanced Drawing API (Optional Future Work)
**Goal:** Expand drawing capabilities beyond basic shapes.

**Tasks (Future):**
- [ ] Add transformation functions:
  - [ ] `translate(x, y)`
  - [ ] `rotate(angle)`
  - [ ] `scale(sx, sy)`
  - [ ] `push()` / `pop()` for transform stack
- [ ] Add advanced shapes:
  - [ ] `bezier(x1, y1, cx1, cy1, cx2, cy2, x2, y2)`
  - [ ] `polygon(points)`
  - [ ] `arc(x, y, w, h, start, stop)`
- [ ] Add image loading:
  - [ ] `load_image(path)`
  - [ ] `image(img, x, y, w, h)`
- [ ] Add noise/random utilities:
  - [ ] `random(min, max)`
  - [ ] `noise(x, y)` (Perlin noise)
- [ ] Add color utilities:
  - [ ] `color(r, g, b, a)`
  - [ ] `lerp_color(c1, c2, amt)`
  - [ ] `hsv_to_rgb(h, s, v)`
- [ ] Add NumPy buffer access:
  - [ ] `pixels` array for direct manipulation
  - [ ] `load_pixels()` / `update_pixels()`

**Files to expand:**
- `src/peyote/ide/drawing_api.py`

---

## Testing Strategy

### Unit Tests

**Editor Tests** (`tests/test_code_editor.py`):
- [ ] Syntax highlighting correctly highlights Python keywords
- [ ] Line numbers update on text change
- [ ] Tab insertion works
- [ ] Comment toggle works

**Execution Engine Tests** (`tests/test_execution_engine.py`):
- [ ] User code executes in isolated namespace
- [ ] setup() called once, draw() called repeatedly
- [ ] Exceptions are caught and reported
- [ ] stdout/stderr captured correctly

**Drawing API Tests** (`tests/test_drawing_api.py`):
- [ ] Each drawing function renders correctly
- [ ] Coordinate system is correct
- [ ] Colors are applied correctly

### Integration Tests

**Offscreen Rendering Tests** (`tests/test_offscreen_rendering.py`):
- [ ] Create OffscreenWidget
- [ ] Run simple sketch (draw red circle)
- [ ] Save PNG
- [ ] Verify PNG exists and has correct dimensions
- [ ] Load PNG with PIL and check pixel colors match expected
- [ ] Test GIF export with multiple frames
- [ ] Verify GIF animation

**Sketch Execution Tests** (`tests/test_sketch_execution.py`):
- [ ] Execute example sketches without errors
- [ ] Verify output is rendered (compare against reference images)
- [ ] Test error handling (syntax errors, runtime errors)

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
Create a suite of canonical sketches and reference images:
1. **test_basic_shapes.py**: Draw circle, rectangle, line
   - Compare output PNG against reference PNG
   - Allow small tolerance for anti-aliasing differences
2. **test_colors.py**: Draw colored shapes
   - Verify RGB values in specific pixel locations
3. **test_animation.py**: Animated sketch (10 frames)
   - Verify frame_count increments
   - Verify shapes move correctly

**Test Framework:**
- Use pytest
- Use PIL for image comparison
- Use `pytest-qt` for Qt widget testing
- Store reference images in `tests/reference_images/`
- Generate test images in `tests/output_images/`
- Use MSE (Mean Squared Error) or SSIM for image comparison

---

## Dependencies

### Required
- **PySide6**: Qt bindings for Python (already in dependencies)
- **numpy**: Array manipulation (already in dependencies)
- **Pillow**: GIF export and image comparison in tests
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
    "pillow",  # Add this
]

[dependency-groups]
dev = [
    # ... existing ...
    "pytest-qt",  # Add this
]
```

---

## Security and Safety Considerations

### Code Execution Security
**Risk:** User code loaded as Python modules has full access to Python runtime and can import any module.

**Mitigations:**
1. **Documentation:** Clearly document that the IDE is a local development tool, not for running untrusted code.
2. **Module Isolation:** Each sketch runs as a separate module in a controlled namespace.
3. **Temporary File Management:** Sketch files stored in dedicated temp directory with proper cleanup.
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
3. Temp directory for sketch modules isolated from user files.

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
- **Drawing API:** ~500 lines
- **File Operations:** ~200 lines
- **Export:** ~200 lines
- **CLI Integration:** ~100 lines
- **Settings:** ~200 lines
- **Tests:** ~800 lines

**Total:** ~3,400 lines

---

## Future Enhancements (Out of Scope for v1)

1. **Debugger Integration:** Breakpoints, step through, variable inspection
2. **Variable Inspector Panel:** Live view of sketch variables
3. **Performance Profiler:** Identify slow draw() calls
4. **Snippet Library:** Pre-built code templates
5. **Community Sharing:** Upload/download sketches from web
6. **3D Rendering:** OpenGL-based 3D drawing API
7. **Video Export:** MP4/MOV export with audio
8. **Multi-file Projects:** Import local modules in sketches
9. **Git Integration:** Version control for sketches
10. **Live Coding Mode:** Code changes reflected immediately without restart

---

## Open Questions for Clarification

1. **Display Widget Architecture:**
   - Should display pane be detachable (like Processing)? Or always integrated?
   - **Recommendation:** Start integrated, add detach feature later if needed.

2. **Drawing API Compatibility:**
   - Should we match Processing's API exactly (e.g., `rect(x, y, w, h)`) or use more Pythonic names?
   - **Recommendation:** Match Processing for familiarity, but use Python naming conventions (e.g., `background()` not `background()`).

3. **Frame Rate Control:**
   - Should users be able to set FPS (e.g., `frame_rate(30)`)? Or fixed at 60?
   - **Recommendation:** Start with fixed 60 FPS, add `frame_rate()` in Phase 11.

4. **NumPy API Exposure:**
   - Should users have direct access to the framebuffer NumPy array for pixel manipulation?
   - **Recommendation:** Yes, as `pixels` global in Phase 11. This enables advanced techniques.

5. **Error Recovery:**
   - When draw() throws exception, should we halt execution or keep running and show error?
   - **Recommendation:** Halt execution, show error, allow user to fix and restart.

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
