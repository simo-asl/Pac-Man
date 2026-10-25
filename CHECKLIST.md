# Pac-Man checklist

Current implementation and verification against `en.subject.pdf` v1.5.
Checked items are implemented or tested as described. External submission and
manual acceptance steps stay unchecked. Source is delivered on
`refactor/game-architecture`; the push result is reported separately.

## Window and layout

- [x] Fixed 2100×1800 window, as requested.
- [x] Windowed mode; no fullscreen flag.
- [x] Drag resizing disabled.
- [x] Size fits the detected 3840×2160 display.
- [x] Shared maze coordinates align walls, actors and pellets.
- [x] Maze centered between the HUD and controls footer.
- [x] Default maze is 39 columns × 29 rows.
- [x] Allowed width is 15–61 columns.
- [x] Allowed height is 11–43 rows.
- [x] Default tiles are 47 pixels.
- [x] Largest permitted maze keeps tiles at least 32 pixels.
- [x] Minimum and maximum dimension combinations tested.
- [x] Invalid dimensions restore only invalid fields to defaults.
- [x] Valid sibling settings survive invalid-value recovery.

## Artwork and colors

- [x] Classic yellow Pac-Man shape retained, with no extra eye or accessories.
- [x] Player source remastered from 30×30 to 314×314.
- [x] All four player directions use the same remastered design.
- [x] Red, pink, cyan and orange ghosts use matching high-resolution artwork.
- [x] Frightened ghost remains distinct blue with a white face.
- [x] Sprite surroundings and Pac-Man's mouth are transparent.
- [x] Smooth scaling from large sources replaces enlarged low-resolution pixels.
- [x] PNG assets remain lossless.
- [x] Native-resolution background replaces the enlarged decorative bitmap.
- [x] Background is cached rather than generated each frame.
- [x] Charcoal panels, off-white text, soft blue walls and warm yellow selection.
- [x] Error and low-time colors remain distinguishable.
- [x] Walls use geometric shapes, not stretched tile images.
- [x] Rounded wall ends and restrained inner highlights.
- [x] Static walls rendered at double resolution and downsampled once.
- [x] Maze, HUD and text remain visually separated.
- [x] Artwork prompts and provenance documented.
- [x] No unused downloaded asset pack remains.

## Main menu

- [x] Start Game starts a fresh run.
- [x] Highscores opens the saved top-ten list.
- [x] Instructions opens controls and rules.
- [x] Exit stops the application cleanly.
- [x] Up/Down changes the highlighted option.
- [x] Selection wraps at the first/last option.
- [x] Enter confirms the highlighted option.
- [x] Highlight agrees with the action Enter activates.
- [x] Keyboard hint visible without a mouse requirement.
- [x] New game clears previous name, save flag and error feedback.
- [x] Generator failures are shown on the menu.

## Highscores and instructions

- [x] Persistent JSON score file is configurable.
- [x] Highest score appears first.
- [x] Only the top ten are stored and displayed.
- [x] Rank, player and score have separate columns.
- [x] Score values are right aligned.
- [x] Maximum-length names fit the table.
- [x] Large score values fit their column.
- [x] Empty score list has a useful message.
- [x] Missing, empty, corrupt and unreadable score files handled.
- [x] Instructions describe movement and pause/resume.
- [x] Instructions describe pellets, power pellets, ghosts, lives and timer.
- [x] Evaluation cheat keys documented.
- [x] Instructions has no unnecessary selection state.
- [x] Enter/Escape returns from both static pages.

## HUD, pause and results

- [x] Current score visible during gameplay.
- [x] Remaining lives visible during gameplay.
- [x] Current and total levels visible.
- [x] Remaining level time visible as minutes:seconds.
- [x] Low-time warning uses the actual timer.
- [x] Best score comes from saved/current values.
- [x] No fabricated HUD values.
- [x] HUD has a quiet solid backing.
- [x] Gameplay footer contains only movement and pause controls.
- [x] P/Escape pauses active play.
- [x] Pause stops gameplay and level/power timers.
- [x] Resume and Main Menu are available in pause.
- [x] Up/Down and Enter work in pause.
- [x] P/Escape resumes directly.
- [x] Pausing during automatic death delay cannot corrupt pause state.
- [x] Game Over shows the actual final score.
- [x] Victory includes congratulations and the actual final score.
- [x] Level Complete shows the accumulated score and continue action.
- [x] Results share a consistent score-card layout.
- [x] Win and loss both lead to name entry.
- [x] Name input has a focused field and placeholder.
- [x] Character count shows the ten-character limit.
- [x] Backspace edits the name.
- [x] Empty/all-space names rejected with visible feedback.
- [x] Only ASCII letters, digits and spaces accepted, maximum ten characters.
- [x] Surrounding spaces trimmed before saving.
- [x] Save failure retains the typed name and permits retry.
- [x] Successful save returns to the main menu.
- [x] Save uses a temporary file and replacement.
- [x] Simulated replacement failure preserves the old score file.
- [x] Temporary score files cleaned up after success/failure.

## Gameplay and ghost movement

- [x] Assigned MazeGenerator wheel preserved without modification.
- [x] Explicit `perfect=False` call.
- [x] At least ten levels configured.
- [x] First default level uses seed 42.
- [x] Later levels receive fresh seeds unless configured.
- [x] Generator exceptions return to the menu with a clear error.
- [x] Player starts near the middle on a usable cell.
- [x] Four ghosts and four power pellets start in corners.
- [x] Pellets cover most available corridors.
- [x] Player/power-pellet cells excluded from normal pellets.
- [x] Pellet positions reachable from the player spawn.
- [x] Wall bits and destination bounds constrain movement.
- [x] Open generator entry/exit cannot move actors outside the grid.
- [x] Ghosts select only open adjacent cells.
- [x] Ghosts turn only at tile centers.
- [x] Chase routing uses actual open shortest paths.
- [x] Invalid/blocked ambush targets fall back to the player.
- [x] Nearby ghosts chase the player directly.
- [x] Normal ghost speed is 2.5 tiles/second.
- [x] Frightened speed is 1.5 tiles/second.
- [x] Ghost travel is consistent at 30, 60 and 120 FPS.
- [x] Fractional movement is retained between frames.
- [x] Movement stops at its target without overshooting.
- [x] Large frame gaps are capped at a 50ms movement step.
- [x] Frightened choices increase actual maze-path distance from Pac-Man.
- [x] Frightened ghosts can wait when trapped instead of circling a wall.
- [x] Freeze stops both ghost target selection and pixel updates.
- [x] Eaten ghosts return after five active seconds.
- [x] Manual pause excludes time from eaten-ghost return countdown.
- [x] Power-pellet pickup applies before same-frame ghost contact.
- [x] Ghost points awarded once when entering eaten mode.
- [x] Collision sizes match displayed actor sizes.
- [x] Life loss and respawn checked.
- [x] Score and lives persist across levels.
- [x] All ten level transitions and final victory exercised.
- [x] Timeout ends the game and permits score entry.
- [x] I/F/L/S cheats retained for evaluation.

## Configuration and errors

- [x] Exactly one JSON path required by the CLI.
- [x] Root `pac-man.py` matches subject usage.
- [x] Module and installed console command launch the same application.
- [x] Full-line `#` and `//` comments supported.
- [x] Comment-like characters inside strings left intact.
- [x] Unknown configuration keys ignored.
- [x] Missing keys receive defaults with messages.
- [x] Invalid types/values receive defaults with messages.
- [x] Integer fields reject booleans and numeric strings.
- [x] Invalid nested level fields recover independently.
- [x] Fewer than ten levels restores the ten-level defaults.
- [x] Bad usage, missing file and wrong extension report clear errors.
- [x] Malformed JSON and non-object root report clear errors.
- [x] Missing/corrupt image errors handled at startup.
- [x] Display initialization failures handled.
- [x] Pygame shuts down after normal exit and startup errors.
- [x] Tested error paths produce no Python traceback.
- [x] File handles and temporary writes use context managers.
- [x] Packaging file errors report a message and nonzero status.

## Code, editor and documentation

- [x] Python 3.12 selected, satisfying the subject's Python minimum.
- [x] Explicit parameter annotations on application functions.
- [x] Explicit return annotations, including constructors.
- [x] Functions/classes have purpose docstrings.
- [x] Google-style `Args` and `Returns` sections describe the API.
- [x] Raised errors documented where relevant.
- [x] Docstring/style audit passes.
- [x] Subject flake8 command passes.
- [x] Subject mypy command and all required flags pass.
- [x] No blanket mypy-disable configuration added.
- [x] UI input separated from screen drawing.
- [x] Shared panel helpers avoid duplicated layouts.
- [x] Fonts, background and static walls cached.
- [x] Unused duplicate menu handler removed.
- [x] Duplicate assets/ZIPs/preview files removed.
- [x] Unused vendor dependency and duplicate wheel removed.
- [x] Root generator wheel retained for installation.
- [x] Ruff removed from project dependencies/configuration.
- [x] Neovim-only Ruff uses 79-column Flake8-style checks.
- [x] Neovim LSP and Conform share editor settings.
- [x] Editor settings stay outside this game repository.
- [x] README has all subject-required sections and current defaults.
- [x] Change snippets and artwork provenance documented.
- [x] Project-management evidence records real checks and pending steps.
- [x] Python compilation and whitespace checks pass.

## Packaging and external acceptance

- [x] Makefile has install, run, debug, clean and lint.
- [x] Packaging spec and archive script included at the root.
- [x] Build outputs, environments and caches ignored by Git.
- [x] Final Linux executable/ZIP rebuilt after this last revision.
- [x] Final packaged startup checked outside the project directory.
- [ ] Full interactive playthrough on the real desktop.
- [ ] Packaged game checked on a second compatible Linux machine.
- [ ] Graphics API equivalence under the subject's MLX rule reviewed by evaluator.
- [ ] Free restricted/unlisted gaming-platform release published.
- [ ] Hosting URL recorded in readiness notes.
- [ ] Peer review and author understanding confirmed before submission.
