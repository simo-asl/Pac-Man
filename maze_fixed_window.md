# Fitting the Maze into a Fixed Window in Pygame

## 1. The Problem in the Current Codebase

In the current implementation:
1. **Window Size Tied to Maze Dimensions**: In [`src/maze.py`](src/maze.py#L33-L36):
   ```python
   self.CELL_SIZE = 40
   self.WI = self.columns * self.CELL_SIZE
   self.HE = self.rows * self.CELL_SIZE
   self.screen = pygame.display.set_mode((self.WI, self.HE))
   ```
2. **Extreme Maze Sizes in `config.json`**:
   - Level 0: `10 x 10` $\rightarrow 400 \times 400$ px (tiny window).
   - Level 1: `990 x 40` $\rightarrow 39,600 \times 1,600$ px (crashes or overflows off the screen).
3. **Inconsistent Windows**:
   - [`src/ui/menu.py`](src/ui/menu.py#L65-L67) tries to use a fixed window (`1200 x 1000`).
   - If `Maze` re-creates `pygame.display.set_mode()`, the window flashes and resizes between the menu and each level.
4. **No Space for HUD**:
   - The 42 subject requires an in-game HUD showing score, remaining lives, level, and timer. A fixed window needs a reserved HUD area (e.g., top 60px).

---

## 2. The Two Primary Approaches

| Approach | Best Used When | How It Works |
| :--- | :--- | :--- |
| **Approach A: Dynamic Cell Scaling (Auto-Fit & Center)** | Maze is small/medium (e.g. 10x10 to 40x40) | Dynamically computes `CELL_SIZE` so the entire maze fits inside the fixed window. |
| **Approach B: Camera / Scrolling Viewport** | Maze is huge (e.g. 990x40) | Keeps a playable `CELL_SIZE` (e.g. 32px or 40px) and scrolls a camera centered on the player. |
| **Recommended: Hybrid Engine** | Any maze dimension | Automatically fits the maze if cells $\ge$ 20px; switches to Camera scrolling if cells would become too small. |

---

## 3. Approach A: Dynamic Cell Scaling (Auto-Fit)

If you want the entire maze visible on screen without scrolling, compute `CELL_SIZE` dynamically according to the fixed window dimensions.

### Math & Formulas

```
Fixed Window:       WINDOW_WIDTH x WINDOW_HEIGHT (e.g., 1000 x 800)
Reserved HUD Bar:   HUD_HEIGHT (e.g., 60 px at the top)
Playable Area:      MAZE_AREA_WIDTH  = WINDOW_WIDTH - 2 * PADDING
                    MAZE_AREA_HEIGHT = WINDOW_HEIGHT - HUD_HEIGHT - 2 * PADDING

Dynamic Cell Size:  CELL_SIZE = min(MAZE_AREA_WIDTH // columns, MAZE_AREA_HEIGHT // rows)

Centered Offsets:   OFFSET_X = (WINDOW_WIDTH - columns * CELL_SIZE) // 2
                    OFFSET_Y = HUD_HEIGHT + (MAZE_AREA_HEIGHT - rows * CELL_SIZE) // 2
```

### Implementing in `Maze`:

```python
class Maze:
    def __init__(self, config: GameConfig, level: int, screen: pygame.Surface):
        self.screen = screen
        self.columns = config.levels[level].width
        self.rows = config.levels[level].height
        self.level = level

        # 1. Fixed dimensions from the active screen
        win_w, win_h = self.screen.get_size()
        hud_height = 60
        padding = 20

        avail_w = win_w - (padding * 2)
        avail_h = win_h - hud_height - (padding * 2)

        # 2. Dynamic CELL_SIZE (ensure at least 1 pixel)
        self.CELL_SIZE = max(1, min(avail_w // self.columns, avail_h // self.rows))

        # 3. Centering offsets
        self.offset_x = (win_w - (self.columns * self.CELL_SIZE)) // 2
        self.offset_y = hud_height + (avail_h - (self.rows * self.CELL_SIZE)) // 2

    def grid_to_pixel(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        pixel_x = self.offset_x + grid_x * self.CELL_SIZE + self.CELL_SIZE // 2
        pixel_y = self.offset_y + grid_y * self.CELL_SIZE + self.CELL_SIZE // 2
        return (pixel_x, pixel_y)

    def pixel_to_grid(self, pixel_x: int, pixel_y: int) -> tuple[int, int]:
        grid_x = (pixel_x - self.offset_x) // self.CELL_SIZE
        grid_y = (pixel_y - self.offset_y) // self.CELL_SIZE
        return (grid_x, grid_y)
```

> [!WARNING]
> If a level is **990 columns wide** in an 800px window, `800 // 990 = 0` pixels! Dynamic scaling only works well up to ~40–50 cells. For 990x40, you **must** use a Camera.

---

## 4. Approach B: Camera & Viewport Scrolling (Recommended for 990x40)

With a camera, `CELL_SIZE` stays at a crisp, playable size (e.g., 32 or 40 px). The window stays fixed, and the viewport follows Pac-Man.

### 1. The Camera Class

Create `src/game/camera.py`:

```python
import pygame

class Camera:
    def __init__(self, view_width: int, view_height: int, hud_height: int = 60):
        self.view_width = view_width
        self.view_height = view_height - hud_height
        self.hud_height = hud_height
        self.x = 0
        self.y = 0

    def update(self, target_x: int, target_y: int, world_width: int, world_height: int):
        # Center the camera on the target (Pac-Man)
        self.x = target_x - self.view_width // 2
        self.y = target_y - self.view_height // 2

        # Clamp camera to maze boundaries so we don't show empty void
        max_x = max(0, world_width - self.view_width)
        max_y = max(0, world_height - self.view_height)
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def apply_point(self, world_x: int, world_y: int) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates."""
        return (world_x - self.x, world_y - self.y + self.hud_height)

    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """Convert a world Rect to screen Rect."""
        return rect.move(-self.x, -self.y + self.hud_height)
```

### 2. Viewport Frustum Culling (Performance Optimization)

A 990x40 maze has **39,600 cells**. Drawing every cell with Python loops drops FPS from 60 to 1 FPS!
With a camera, only draw the cells visible inside the viewport:

```python
def draw_visible_maze(self, camera: Camera):
    # Only iterate over the visible slice of columns and rows
    start_col = max(0, camera.x // self.CELL_SIZE)
    end_col = min(self.columns, (camera.x + camera.view_width) // self.CELL_SIZE + 2)

    start_row = max(0, camera.y // self.CELL_SIZE)
    end_row = min(self.rows, (camera.y + camera.view_height) // self.CELL_SIZE + 2)

    for y in range(start_row, end_row):
        for x in range(start_col, end_col):
            cell = self.maze[y][x]
            screen_x, screen_y = camera.apply_point(x * self.CELL_SIZE, y * self.CELL_SIZE)
            self.draw.draw_maze_cell(screen_x, screen_y, cell, color38, 2)
```

---

## 5. Approach C: Offscreen Surface Scaling (Virtual Canvas)

Another clean technique is to render the maze onto a fixed virtual surface and scale it down to the window.

```python
# In your main game initialization:
VIRTUAL_WIDTH = 1200
VIRTUAL_HEIGHT = 800
virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

# In the game loop:
virtual_surface.fill((0, 0, 0))
# 1. Render all game elements onto virtual_surface at virtual coordinates
maze.draw(virtual_surface)
player.draw(virtual_surface)
ghosts.draw(virtual_surface)

# 2. Scale virtual surface to the actual fixed display window
screen.blit(
    pygame.transform.smoothscale(virtual_surface, screen.get_size()),
    (0, 0)
)
pygame.display.flip()
```

---

## 6. How to Refactor Your Current Code Step-by-Step

### Step 1: Centralize Window Creation in `__main__.py`
Never create `pygame.display.set_mode()` inside `Maze.__init__`. Create it once in `__main__.py` (or a main `App` class) and pass `screen` down:

```python
# src/__main__.py
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Pass screen to Maze
maze = Maze(parser.parser(), level=0, screen=screen)
```

### Step 2: Update `Maze.__init__` in `src/maze.py`
Remove `pygame.display.set_mode()` from `Maze`:

```python
# src/maze.py
class Maze:
    def __init__(self, config: GameConfig, level: int, screen: pygame.Surface):
        self.screen = screen
        self.columns = config.levels[level].width
        self.rows = config.levels[level].height
        self.level = level

        win_w, win_h = self.screen.get_size()
        hud_h = 60

        # Check if the maze fits comfortably
        max_cell_w = win_w // self.columns
        max_cell_h = (win_h - hud_h) // self.rows
        ideal_cell = min(max_cell_w, max_cell_h)

        if ideal_cell >= 20:
            # Mode A: Auto-fit whole maze on screen
            self.mode = "fit"
            self.CELL_SIZE = ideal_cell
            self.offset_x = (win_w - self.columns * self.CELL_SIZE) // 2
            self.offset_y = hud_h + ((win_h - hud_h) - self.rows * self.CELL_SIZE) // 2
            self.camera = None
        else:
            # Mode B: Large maze -> Use Camera scrolling
            self.mode = "camera"
            self.CELL_SIZE = 32  # Comfortable tile size
            self.offset_x = 0
            self.offset_y = 0
            self.camera = Camera(win_w, win_h, hud_height=hud_h)
```

### Step 3: Fast Line Drawing in `src/ui/draw.py`
Notice that [`src/ui/draw.py`](src/ui/draw.py#L12-L25) currently uses `set_at()` pixel-by-pixel:
```python
# Slow: Calling set_at in nested loops
for offset in range(thickness):
    for x in range(start_x, end_x):
        self.screen.set_at((x, y + offset), color)
```
For fixed windows and smooth scrolling, replace this with Pygame's native line drawing:
```python
# Fast (100x faster, hardware-accelerated):
def draw_horizontal_line(self, start_x: int, y: int, end_x: int, color, thickness: int = 1) -> None:
    pygame.draw.line(self.screen, color, (start_x, y), (end_x, y), thickness)

def draw_vertical_line(self, x: int, start_y: int, end_y: int, color, thickness: int = 1) -> None:
    pygame.draw.line(self.screen, color, (x, start_y), (x, end_y), thickness)
```

### Step 4: Render World Coordinates to Screen Coordinates
When drawing entities (Pac-Man, ghosts, dots), apply the camera or offset:

```python
# In entity draw method:
def draw(self, screen: pygame.Surface, camera: Camera | None = None, offset=(0, 0)):
    if camera:
        draw_x, draw_y = camera.apply_point(self.x, self.y)
    else:
        draw_x = self.x + offset[0]
        draw_y = self.y + offset[1]

    # Only draw if within screen bounds
    if 0 <= draw_x <= screen.get_width() and 0 <= draw_y <= screen.get_height():
        rect = self.image.get_rect(center=(draw_x, draw_y))
        screen.blit(self.image, rect)
```

---

## 7. Recommended HUD Layout for 42 Subject

Keep the top 60px of the fixed window reserved for the HUD:

```
+-----------------------------------------------------------+  y = 0
| SCORE: 1250      LIVES: ♥ ♥ ♥      LEVEL: 1      TIME: 84s|  HUD Area (60px)
+-----------------------------------------------------------+  y = 60
|                                                           |
|                     MAZE PLAY AREA                        |  Fixed Window
|                 (Centered or Viewport)                    |  (e.g., 1024x768)
|                                                           |
+-----------------------------------------------------------+  y = 768
```

```python
def draw_hud(screen: pygame.Surface, score: int, lives: int, level: int, time_left: int):
    # Top banner background
    pygame.draw.rect(screen, (20, 20, 20), (0, 0, screen.get_width(), 60))
    pygame.draw.line(screen, (255, 255, 255), (0, 60), (screen.get_width(), 60), 2)

    font = pygame.font.Font(None, 32)
    hud_text = f"SCORE: {score}   LIVES: {lives}   LEVEL: {level}   TIME: {time_left}s"
    surface = font.render(hud_text, True, (255, 220, 50))
    screen.blit(surface, (20, 15))
```

---

## 8. Summary Comparison

| Strategy | Pros | Cons | Recommendation |
| :--- | :--- | :--- | :--- |
| **Dynamic Resizing (Auto-Fit)** | Simple math; entire maze is visible at once. | Unplayable for very wide/tall mazes (990x40). | Use for mazes $\le 40 \times 40$. |
| **Camera Viewport** | Works with any maze size (even $10,000 \times 10,000$); crisp sprites. | Player cannot see the whole maze at once; requires culling. | **Must-have** for the 990x40 level. |
| **Hybrid (Auto-Fit + Camera)** | Adapts dynamically to any configuration in `config.json`. | Requires a small condition to choose between the two. | **Best choice for the project.** |
