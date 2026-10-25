# Current changes

This replaces superseded window-size and artwork experiments. See
[CHECKLIST.md](CHECKLIST.md) for the complete implemented/tested inventory and
remaining external steps.

## Window, maze and limits

```python
CANVAS_SIZE = (2100, 1800)
width: int = Field(default=39, ge=15, le=61)
height: int = Field(default=29, ge=11, le=43)
```

The window stays fixed and windowed on the detected 3840×2160 monitor. The default
maze uses 47-pixel tiles. Maximum dimensions preserve at least 32-pixel tiles in
the 1980×1380 play area. Invalid fields use their defaults without discarding
valid sibling values. All ten example levels use the default dimensions.

## Artwork and UI

- Pac-Man and ghosts remastered from 30×30 to 314×314 transparent PNGs, preserving
  their classic shapes, colors and expressions. Other player directions are
  rotations of the same design. [Artwork prompts](project-management/ARTWORK.md).
- Sprites use smooth scaling. No low-resolution background or wall PNGs remain.
- Background uses a native-resolution gradient and restrained arcade corners.
- Walls use rounded geometry, rendered at double size and downsampled once into
  the cached maze. Game collision/path geometry is unchanged.
- Charcoal panels, off-white text, warm yellow focus and soft blue walls replace
  inconsistent saturated colors.
- Menu, pause, win/loss and level completion share panel helpers.
- Scores have aligned ranks, names and right-aligned values; long values fit their
  column. Name entry shows a focused field, limit counter and save feedback.
- Instructions stays a static page. Enter/Escape returns to the menu.

UI files have separate jobs: `menu.py` handles input/saving, `menu_view.py` draws
pages, `panels.py` shares simple components, `background.py` renders the backdrop,
and `game_ui.py` draws the cached maze and live HUD. There is no extra framework.
See [UI snippets](project-management/UI.md).

## Ghost movement

```python
BASE_SPEED = 2.5  # Tiles per second.
```

Normal speed is 2.5 tiles/second; frightened speed is 60% of that. Movement uses
elapsed frame time, carries fractional distance, stops at tile centers and caps
large movement steps at 50ms. Paused frames do not become a large resume jump.

Chase searches actual open passages. Invalid ambush targets fall back to the
player; nearby ghosts chase directly. Frightened ghosts choose increasing
maze-path distance, including a valid reverse, and can wait at a dead end instead
of looping around walls. Freeze stops both targeting and pixel movement.

## Scoring, pause and errors

- Existing name rules retained: 1–10 ASCII letters/digits/spaces, not all spaces.
- Empty names and save failures show feedback and permit retry.
- Actual final score saved using the configured filename; success returns to menu.
- Top ten scores are sorted descending; malformed/missing files handled.
- Score writes use a temporary file and atomic replacement, preserving old data
  when writing/replacement fails.
- Pause menu selection agrees with Enter; P/Escape resumes directly.
- Level/power/eaten-ghost timers exclude manual pause time.
- Same-frame power-pellet collection frightens ghosts before contact checks.
- External generator errors return to menu; the assigned wheel is unchanged and
  `perfect=False` is explicit. Later unspecified seeds are fresh random values.
- Movement bounds prevent leaving the generator's open entry/exit.
- Configuration validates fields independently, supports full-line comments,
  ignores unknown keys and reports invalid level objects. Optional absent seeds
  are valid and do not generate warning noise.
- CLI and packaging failures report clear messages/nonzero status. Startup
  always releases Pygame resources.

## Types, docstrings and tools

Every application function has explicit parameter and return annotations.
Google-style docstrings describe purpose, `Args`, `Returns` and relevant raised
errors. flake8 and the subject's full mypy flags pass.

Ruff is configured only in Neovim, using a shared editor-owned `ruff.toml` for the
LSP and Conform: 79 columns and Flake8-style E/F/W checks. The game has no Ruff
configuration/dependency/Makefile step. A separate Google-docstring audit was run
with the installed editor tool.

## Cleanup and packaging

Removed duplicate asset trees, unused ZIPs/preview, the unused vendor package,
duplicate generator wheel, unused menu handler and unused formatter dependency.
The root assigned wheel remains. Original removed assets have a recovery backup
at `/tmp/pac-man-unused-assets-20261025.tar.gz` for this working session; Git also
retains tracked originals in history.

`pac-man.py`, the module entry point and installed console script launch the same
app. Makefile includes install/run/debug/clean/lint/package. `pac-man.spec` and
`package.py` reproduce the Linux executable and ZIP. Temporary caches/build
outputs stay out of Git; clean preserves the environment and release files.

## Verification

Validated UI navigation, score persistence/retry, all result screens, maze limits,
reachability, ghost travel at 30/60/120 FPS, legal turns, freeze, chase/flee routes,
lag caps, file/config/generator/asset/display failures, docstrings and type hints.
See [acceptance notes](project-management/ACCEPTANCE.md) for exact scope.
Real desktop playthrough, evaluator graphics-library approval and public gaming
platform publication remain external acceptance steps.
