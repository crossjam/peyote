# HexTrail Screensaver - Code Summary and Python Port Plan

## Original Code Summary

**HexTrail** is an XScreenSaver module written in C with OpenGL that creates a mesmerizing animated pattern of colored lines growing across a hexagonal grid.

### Core Concept

The screensaver creates a honeycomb grid of hexagonal cells. Animated "arms" (lines) grow from the centers of hexagons toward their edges, then continue into neighboring hexagons, creating a branching network of colorful trails across the hexagonal substrate.

### Key Data Structures

1. **arm** (hextrail.c:39-43)
   - State: EMPTY, IN, WAIT, OUT, or DONE
   - `ratio`: Growth progress (0.0 to 1.0)
   - `speed`: Animation speed

2. **hexagon** (hextrail.c:45-53)
   - Position (XYZ coordinates)
   - 6 neighbors (pointers to adjacent hexagons)
   - 6 arms (one for each edge)
   - Color index
   - Border state and animation ratio

3. **hextrail_configuration** (hextrail.c:55-70)
   - Grid dimensions and hexagon array
   - Color palette (8 colors)
   - OpenGL context and rotation state
   - Animation state (FIRST, DRAW, FADE)

### Algorithm Flow

#### Grid Initialization (make_plane, hextrail.c:100-171)
1. Creates a 2D array of hexagons (count*2 × count*2)
2. Positions hexagons in honeycomb pattern (offset every other row)
3. Links each hexagon to its 6 neighbors using clever index arithmetic
4. Generates smooth colormap with 8 colors

#### Animation Loop (tick_hexagons, hextrail.c:245-377)

**Arm Growth:**
- **OUT state**: Arm grows from center to edge
  - When ratio reaches 1.0, transitions neighbor's opposite arm to IN state
- **IN state**: Arm grows from edge to center
  - When ratio reaches 1.0, spawns 1-4 new OUT arms to random empty neighbors
  - This creates the branching behavior

**Arm Spawning** (add_arms, hextrail.c:185-241):
- Randomly selects 1-4 available neighbor directions
- Creates paired arms: OUT from current hex, WAIT in neighbor
- Mostly keeps same color, occasionally shifts to next color in palette
- Increments live_count for active animations

**Border Animation:**
- Borders fade IN when hexagon becomes active
- Borders fade OUT after random delay when arms complete
- Creates pulsing effect around active hexagons

**Scene Reset:**
- When live_count reaches 0, triggers FADE state
- All borders fade out
- Scene resets and starts fresh from center

#### Rendering (draw_hexagons, hextrail.c:381-583)

**Hexagon Borders:**
- Drawn as 6 quads forming a ring
- Thickness controlled by margin calculations
- Opacity controlled by border_ratio

**Arms:**
- Each arm rendered as 2 triangles forming a quad
- Gradient coloring: blends between current hex color and neighbor color
- Width controlled by thickness parameter
- Length controlled by arm ratio

**Center Caps:**
- Small hexagon in center to hide line joins
- Scales based on number of active arms

### OpenGL Rendering Details

- Uses perspective projection with gluPerspective
- Camera positioned at (0, 0, 30) looking at origin
- Scene scaled by factor of 18
- Smooth shading with GL_SMOOTH
- Depth testing disabled (2D rendering)
- Front face winding: GL_CCW

### Configuration Parameters

- **count** (default: 20): Grid size multiplier
- **speed** (default: 1.0): Animation speed (0.1-20)
- **thickness** (default: 0.15): Line width (0.05-0.5)
- **spin**: Enable rotation animation
- **wander**: Enable translation animation
- **wireframe**: Render in wireframe mode

### Interactive Features

- Mouse trackball for rotation
- Keyboard controls to adjust grid size (+/- keys, arrows)
- Space/Enter to reset animation

---

## Python/Pygame-CE Port Implementation Plan

### Phase 1: Core Data Structures

**Files to create:**
- `hextrail_pygame.py` - Main entry point
- `hexagon.py` - Hexagon and Arm classes
- `grid.py` - Grid management
- `config.py` - Configuration constants

**Tasks:**
1. Define `Arm` class with state enum and properties
2. Define `Hexagon` class with position, neighbors, arms, color
3. Create `HexGrid` class to manage hexagon array and neighbor linking
4. Implement neighbor calculation logic (handle even/odd row offsets)

### Phase 2: Grid Initialization

**Tasks:**
1. Generate hexagonal grid positions
   - Use formula: `x = col * width`, `y = row * height`
   - Offset x by `width/2` for odd rows
   - Center grid around (screen_width/2, screen_height/2)
2. Calculate hexagon size based on count parameter
3. Link neighbors using same 6-direction logic as C code
4. Generate color palette using colorsys module (HSV interpolation)

### Phase 3: Animation Logic

**Tasks:**
1. Implement `tick_hexagons()` method:
   - Update all arm ratios based on speed
   - Handle state transitions (OUT→DONE→IN→DONE)
   - Spawn new arms when IN arms complete
2. Implement `add_arms()` method:
   - Random neighbor selection
   - Pair arm creation (OUT + WAIT)
   - Color propagation logic
3. Implement border animation with fade in/out
4. Add live_count tracking
5. Implement scene reset on completion

### Phase 4: Rendering with Pygame

**Rendering strategy** (since pygame-ce doesn't have OpenGL integration by default):

**Option A: Pure pygame rendering**
- Use `pygame.draw.polygon()` for hexagons
- Use `pygame.draw.line()` with width for arms
- Use alpha surfaces for transparency effects
- Calculate vertices manually from hexagon center positions

**Option B: PyOpenGL integration**
- Use `pygame.display.set_mode()` with `OPENGL` flag
- Port OpenGL rendering code more directly
- Maintain vertex calculations from original

**Recommended: Option A** for simplicity and pygame-ce compatibility

**Rendering tasks:**
1. Create method to calculate 6 hexagon corner vertices
2. Implement `draw_hexagon_border()`:
   - Draw 6 trapezoidal segments for border ring
   - Apply alpha based on border_ratio
3. Implement `draw_arm()`:
   - Calculate line start/end based on ratio
   - Draw with gradient color (interpolate between hex colors)
   - Use `pygame.draw.polygon()` for width
4. Implement `draw_center_cap()`:
   - Draw small filled hexagon in center
5. Add fade-to-black effect during FADE state

### Phase 5: Configuration and Controls

**Tasks:**
1. Create config system with command-line arguments:
   - `--count`, `--speed`, `--thickness`
   - `--no-spin`, `--no-wander`
   - `--fullscreen`, `--width`, `--height`
2. Implement keyboard controls:
   - Arrow keys / +/- to adjust count
   - Space to reset
   - ESC to quit
3. Implement mouse camera rotation (optional, simpler than trackball)
4. Add FPS display option

### Phase 6: Effects and Polish

**Tasks:**
1. Implement rotation/wander animation:
   - Rotate entire scene around center
   - Translate scene position over time
   - Use simple sin/cos for smooth motion
2. Add smooth color interpolation along arms
3. Optimize rendering:
   - Only draw visible hexagons
   - Batch similar drawing operations
   - Use dirty rect optimization if needed
4. Add anti-aliasing with `pygame.gfxdraw` if available

### Phase 7: Testing and Refinement

**Tasks:**
1. Test with various grid sizes (count: 2-80)
2. Test speed range (0.1-20)
3. Test thickness range (0.05-0.5)
4. Verify arm growth and branching behavior matches original
5. Verify color propagation and border animations
6. Profile performance and optimize bottlenecks
7. Test on different screen resolutions

---

## Technical Considerations for Python Port

### Mathematics

**Hexagon geometry:**
- Corner angles: 0°, 60°, 120°, 180°, 240°, 300°
- Height to width ratio: `sqrt(3) / 2 ≈ 0.866`
- Neighbor offsets depend on row parity (even vs odd)

**Color blending:**
- Use linear interpolation: `color1 * (1 - t) + color2 * t`
- Apply fade_ratio to all RGB components

### Performance Optimization

1. **Pre-calculate hexagon vertices** - Store corner positions, don't recalculate each frame
2. **Cull invisible hexagons** - Only draw hexagons with active arms or visible borders
3. **Use pygame.Surface caching** - Cache rendered hexagons if static
4. **Limit active arms** - Port the live_count system to prevent too many simultaneous animations

### Python-Specific Implementation Notes

**Replace C patterns:**
- `malloc/free` → Python list/dict management (automatic)
- `abort()` → `raise AssertionError()` or `assert`
- `random()` → `random.randint()`, `random.random()`
- `frand()` → `random.uniform(0, n)`
- `BELLRAND(n)` → `(random.uniform(0,n) + random.uniform(0,n) + random.uniform(0,n)) / 3`

**Enums:**
```python
from enum import Enum, auto

class ArmState(Enum):
    EMPTY = auto()
    IN = auto()
    WAIT = auto()
    OUT = auto()
    DONE = auto()

class SceneState(Enum):
    FIRST = auto()
    DRAW = auto()
    FADE = auto()
```

**Color palette:**
```python
import colorsys

def make_colormap(num_colors):
    colors = []
    for i in range(num_colors):
        hue = i / num_colors
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        colors.append((int(r*255), int(g*255), int(b*255)))
    return colors
```

---

## Estimated Complexity

- **Lines of code**: ~800-1000 lines (vs 782 in original)
- **Development time**: 2-3 days for experienced Python/pygame developer
- **Main challenges**:
  1. Hexagonal grid neighbor calculation
  2. Smooth gradient rendering without OpenGL
  3. Performance with large grids (40×40 = 1600 hexagons)

---

## File Structure

```
hextrail-pygame/
├── hextrail_pygame.py      # Main entry point, game loop
├── hexagon.py              # Hexagon and Arm classes
├── grid.py                 # HexGrid management
├── renderer.py             # Drawing functions
├── config.py               # Configuration and constants
├── utils.py                # Helper functions (BELLRAND, color interpolation)
└── README.md               # Usage instructions
```

---

## Dependencies

```
pygame-ce >= 2.0.0
Python >= 3.8
```

Optional:
```
numpy  # For faster vector math (if performance needed)
```

---

## Next Steps

1. Set up project structure
2. Implement Phase 1 (data structures)
3. Implement Phase 2 (grid initialization) and verify neighbor links
4. Implement Phase 3 (animation logic) with debug visualization
5. Implement Phase 4 (rendering) incrementally
6. Polish and optimize

The port should maintain the same visual aesthetic and behavior while being more accessible to Python developers and easier to modify/extend.
