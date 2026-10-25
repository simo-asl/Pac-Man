# Acceptance checks — October 25, 2026

Checks use SDL dummy/offscreen for repeatable behavior. Temporary test programs
live under `/tmp`, following the subject's note that test programs are not graded.

## Automated checks

- flake8 and mypy with every mandatory subject flag.
- Compilation; all function parameters/returns annotated; classes/functions have
  purpose docstrings and applicable Google-style Args/Returns/Raises sections.
- Root CLI: usage, missing file, wrong extension, malformed JSON, non-object root.
- Config: comments, missing/unknown keys, strict integer types, invalid nested
  values, dimension limits, and preservation of valid sibling settings.
- Maze: min/max dimension combinations, tile size at least 32 pixels, panel bounds,
  walkable-cell reachability, and no movement through outer entry/exit.
- UI: all menu options, static-page return, ten long names, large scores, pause,
  Enter selection, both endings, required names, failure/retry and persistence.
- Gameplay: power before same-frame collision, edible ghost scoring, life loss,
  respawn, score/lives across ten levels and final victory.
- Ghosts: consistent travel at 30/60/120 FPS, legal center-to-center turns, no
  overshoot, 50ms lag cap, frozen state, invalid ambush targets and increasing
  maze-path distance when frightened.
- File errors: broken/unreadable scores, failed replacement preserving old file,
  temporary-file cleanup, simulated generator/asset/display failures.
- Neovim: LSP/Conform use the same editor-only Ruff file; 79 columns and E/F/W.
- Final release: build and off-directory startup recorded in CHECKLIST.md.

## Visual review

Inspected menu, ten populated score rows, instructions, victory, name entry,
pause and gameplay previews. Source sprites are 314×314 transparent PNGs.
Background and walls render from code without enlarged bitmap textures. Colors
and focus indicators are consistent; playable pellets remain distinct.

## Remaining manual steps

On the real desktop: play a level, test powered pause/resume, resize prevention,
cheats, final score entry, relaunch persistence and comfortable readability.
On a second compatible Linux machine: verify the packaged game end to end.
Record evaluator approval of the graphics API and the gaming-platform hosting
URL in READINESS.md before final submission.

Final delivery audit: 122 functions have explicit parameter/return types and
Args/Returns documentation. Google-style docstring checks, flake8 and mandatory
mypy flags pass. The final Linux build and ZIP inventory pass; its menu starts
from a separate directory under SDL dummy. The startup test terminates it after
three seconds and does not replace a real interactive packaged playthrough.
