# Asset and dead-code cleanup

The cleanup keeps runtime resources under one directory and preserves the
assigned MazeGenerator wheel. It is not a new artwork generation pass.

## Retained asset inventory

| Directory | Contents | Count |
| --- | --- | --- |
| `src/assets/backgrounds/` | Main menu, highscores, instructions, victory and name entry | 5 PNGs |
| `src/assets/ghosts/` | Four directions for each ghost, four eyes sprites, frightened sprite | 21 PNGs |
| `src/assets/player/` | Four open-mouth player directions used by the current code | 4 PNGs |
| `src/assets/walls/` | Images for wall masks 0–15 | 16 PNGs |
| `src/assets/fonts/` | Tamzen Bold BDF and its license | 2 files |

Total: 48 runtime/font-license files. Asset paths are resolved by
`src/resources.py`, so they do not depend on the current working directory.
The root `mazegenerator-2.1.0-py3-none-any.whl` stays because `pyproject.toml`
references it directly.

## Removed material

- The duplicate `src/game/assets/` tree after copying only the files used by code.
- Unused copies of sprites, backgrounds, pellet/life icons and HUD panels.
- Half/closed-mouth animation frames and flashing frightened sprites that the
  current renderer never selects.
- Unused preview pictures and asset ZIP archives.
- The duplicate generator wheel under `vendor/`; the referenced root wheel stays.
- The unused `src/pac_man` legacy entry-point alias; both the installed console
  command and root launcher use `src.__main__:main`.
- Unused maze color constants and the unused stored Draw reference.
- Game/Player screen-size fields and constructor arguments that had no readers,
  plus the redundant Game level counter; GameController owns progression.

Required resources were selected from both literal and formatted asset paths.
Menu loading, all actor directions, wall masks and the ten-level skip flow were
checked after the moves. Public launch commands and gameplay behavior remain
the same; the open bugs are recorded separately rather than repaired here.
