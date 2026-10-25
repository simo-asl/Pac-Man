*This project has been created as part of the 42 curriculum by tlaghzal, mel-asla.*

# Pac-Man

## Description

A desktop Pac-Man game in Python and Pygame, using the assigned MazeGenerator
package without modifying it. Eat pellets, avoid ghosts, and complete ten levels.
The interface uses charcoal panels, soft blue walls and warm yellow highlights.
Pac-Man and ghosts retain their classic appearance with remastered 314×314
source images. Scores, lives, levels and timers come from the active game.

## Instructions

Use Python 3.12 (selected by `.python-version`) and [uv](https://docs.astral.sh/uv/).

```sh
make install
make run
# Equivalent subject entry point:
uv run python3 pac-man.py config.json
```

The installed `uv run pac-man config.json` command and
`uv run python -m src config.json` launch the same application.
Exactly one JSON configuration path is required. Usage, file, and syntax errors
print a message and return a nonzero exit status without a traceback.

The game opens in a fixed **2100×1800 window**. It stays windowed and cannot be
resized by dragging. This size was chosen for the detected 3840×2160 monitor.
Artwork is drawn directly at the game canvas size, keeping
sprites, maze tiles, and text aligned without stretching the finished frame.

### Controls

| Key | Action |
| --- | --- |
| Arrow keys | Move; Up/Down selects menu items |
| Enter | Confirm the selected option |
| P or Escape during gameplay | Pause |
| Up/Down, then Enter while paused | Resume or return to the main menu |
| P or Escape while paused | Resume immediately |
| Enter or Escape in High Scores / Instructions | Return to the main menu |
| Enter after winning or losing | Open name entry |
| Backspace during name entry | Delete the last character |
| Enter during name entry | Save and return to the menu |
| I / F / L / S | Toggle invincibility / freeze ghosts / extra life / skip level |

Starting a new game resets the score and lives. Scores and remaining lives carry
across levels. Running out of time ends the game. Losing a life pauses briefly,
then respawns all actors; losing every life ends the game. The level timer and
player power duration stop while manually paused. Eaten ghosts return to their
corner after five active seconds. Power pellets last ten seconds.

### Code documentation

Functions have explicit parameter and return annotations. Google-style
docstrings describe purpose, `Args`, `Returns`, and raised errors where relevant.
`make lint` runs the subject's flake8 and mypy checks. Ruff configuration belongs
to the editor; it is not a project dependency or lint step.

### Development and packaging

```sh
make lint       # flake8 and the subject's mypy flags
make debug      # Python pdb
make clean      # project caches, preserving the virtual environment
make package    # current-platform PyInstaller executable and Linux ZIP
```

`make package` builds `dist/pac-man` and `dist/pac-man-linux.zip`, containing the
executable, editable config, README, checklist, change notes, project-management
documents and artwork provenance. On Linux, extract the
ZIP, run `chmod +x pac-man` if needed, then `./pac-man config.json`. A desktop SDL
runtime is required; the build is not a Windows/macOS executable. Build on each
target operating system for its native executable. Generated files are ignored
by Git; `pac-man.spec` and `package.py` are the reproducible packaging sources.

A public gaming-platform listing has **not** been published. Upload the release
ZIP to a free restricted/unlisted Itch.io project to complete the subject's
hosting requirement. See the [readiness checklist](project-management/READINESS.md).

## Configuration

The configuration is a JSON object. Full lines starting with `#` or `//` are
ignored; inline and block comments are not supported. Unknown keys are ignored.
Missing and invalid settings print a message and use their defaults.
The optional seed can be omitted without a warning. Valid sibling
settings are retained. Numeric fields require integers, not strings or booleans.
An unreadable file, malformed JSON, a non-object root, or a filename without
`.json` stops startup cleanly because these do not provide usable configuration.

| Key | Default | Meaning / accepted range |
| --- | --- | --- |
| `highscore_filename` | `highscores.json` | Nonempty score-file path |
| `lives` | 3 | Starting lives, at least 1 |
| `pacgum` | 42 | Requested pellet count, at least 0 |
| `points_per_pacgum` | 10 | Points per pellet, at least 0 |
| `points_per_super_pacgum` | 50 | Points per power pellet, at least 0 |
| `points_per_ghost` | 200 | Points per edible ghost, at least 0 |
| `level_max_time` | 90 | Seconds per level, at least 1 |
| `levels` | Ten 39×29 levels | At least ten level objects |
| `levels[].width` | 39 | Maze columns, 15–61 |
| `levels[].height` | 29 | Maze rows, 11–43 |
| `levels[].seed` | `null` | Optional integer seed |

The default maze uses 47-pixel tiles. At the largest accepted dimensions, tiles
remain at least 32 pixels wide. The lower bounds leave room for the generator's
central pattern and useful corridors; the upper bounds prevent unreadable grids.
Out-of-range dimensions use the defaults, preserving valid sibling settings. The
first level uses seed 42 unless explicitly configured; other levels get fresh
random seeds unless specified. A missing `levels` list uses ten defaults with
seed 42 for the first level. A list shorter than ten is replaced by the default
list to satisfy the required minimum level count. Invalid level fields fall back
individually to their defaults.

Pellets cover at least 70% of available corridors to satisfy “most corridors” in
the subject. `pacgum` can increase that count up to the available positions; setting
it to zero does not remove that coverage minimum. Four power pellets occupy the
corners. Player spawn and power-pellet cells are excluded from normal pellets.

Relative configuration and high-score paths are resolved from the working
directory. Bundled artwork is resolved from the application location.

## Highscore

Scores are stored as JSON with a `scores` array of `{ "name": ..., "score": ... }`
objects. JSON keeps the format small and readable without another dependency.
Names contain 1–10 ASCII letters, digits, or spaces and must contain a non-space
character. Enter trims surrounding spaces. Scores are non-negative integers.

The top ten are sorted highest first. Missing, empty, invalid, and unreadable
files are handled as an empty list with a warning where appropriate. The menu
loads the score file when displaying High Scores, and the HUD loads the saved
best when a level starts. Game Over and Level Complete show centered score cards with a single Enter
action. Victory has a large final score. Name entry uses a bordered input field
and visible validation feedback. Instructions is a static page; Enter or Escape
returns to the menu without selecting an option. Both win and loss lead to name
entry. Empty names show
an error. Saving writes a temporary file in the same directory, then replaces
the destination, protecting the previous file from incomplete writes. Save
failures keep name entry open for retry. Successful saves return to the menu.
The HUD's Best value is the larger of the saved best and current score.

## Maze Generation

The supplied `mazegenerator-2.1.0-py3-none-any.whl` remains in the project root
and is a local dependency in `pyproject.toml`. Keep it there for installation.
`Maze` calls `MazeGenerator((width, height), perfect=False, seed=seed)` and reads
the returned wall-bit grid. Wall bits 1/2/4/8 represent north/east/south/west.
The package is unmodified. Generation errors are shown in the main menu.

Tiles fit between the HUD and footer, and the maze is centered in that region.
A shared grid-to-pixel conversion aligns actors and pellets with the walls.
Movement checks both wall bits and destination bounds, including the generator's
open outer entry/exit. The player's spawn is the nearest usable cell to the center.

## Implementation

The frame loop handles events, updates active gameplay and draws directly into
the fixed window, capped at 60 FPS. Static walls and the background are cached;
actors, pellets, scores and time are drawn each frame. Fonts are cached by size.
Remastered sprites use smooth scaling to the tile size.

Ghosts follow open shortest paths toward chase or ambush targets. Invalid ambush
targets fall back to the player. Within four cells they chase directly. Their
normal speed is 2.5 tiles/second and frightened speed is 1.5 tiles/second,
independent of frame rate. They turn only at tile centers and cannot overshoot a
target. A 50ms movement-step cap prevents large jumps after a stall. Frightened
ghosts use actual maze-path distance to flee, waiting when trapped at a dead end.
Evaluation cheats remain available for testing transitions and collisions.

The UI uses one gold selection highlight, aligned score columns and consistent
result panels. Instructions is a static page. Name entry shows a placeholder,
a character count and save feedback. Its code is split between input
(`menu.py`), page drawing (`menu_view.py`) and shared panels (`panels.py`). See
[UI changes and code snippets](project-management/UI.md).

## General Software Architecture

| Module | Responsibility |
| --- | --- |
| `pac-man.py`, `src/__main__.py` | CLI, desktop window, event loop, fixed window |
| `src/parsing/` | Configuration models and recovery from invalid settings |
| `src/maze.py` | Assigned-generator adapter, wall grid and coordinate conversion |
| `src/game_controller.py` | Level setup, state transitions and gameplay orchestration |
| `src/game/` | Player, ghosts, pellets, collisions, scores, timers and cheats |
| `src/ui/` | Screens, state dispatch, drawing, HUD and pause overlays |
| `src/resources.py` | Source/bundled asset paths |
| `pac-man.spec`, `package.py` | Executable and release archive |

`StateMachine` dispatches events and rendering to `Menu` or `GameController`.
The controller owns the current `Game`, `Maze`, `Player`, and `GhostsManager`.
`GameUi` renders their values through `Draw`. `High` validates and persists scores.

## Project Management

The [project-management directory](project-management/) contains the current
subject checklist and acceptance results. It records completed work and remaining
submission steps without inventing a historical timeline or team assignments.
[CHANGES.md](CHANGES.md) contains current code snippets and explanations.

The background is drawn at the full window resolution with a quiet gradient and
subtle arcade corners. Walls are rounded geometry, antialiased once at double
resolution and cached. No enlarged background PNGs or bitmap wall tiles remain.
See the full [checklist](CHECKLIST.md) and [artwork notes](project-management/ARTWORK.md).

## Resources

- [Pygame documentation](https://www.pygame.org/docs/)
- [Python documentation](https://docs.python.org/3/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- Local assignment: `en.subject.pdf`, version 1.5.
- [Artwork provenance](src/assets/arcade/LICENSE.md) and
  [remaster prompts](project-management/ARTWORK.md).
- AI assistance: subject review, UI and window implementation, parser/error
  handling, gameplay bug fixes, lint/type fixes, sprite remastering and native background rendering,
  packaging, headless verification, and documentation. Authors must review and
  understand this work and perform peer review before submission.
