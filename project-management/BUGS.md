# Bug tracker

These defects were reproduced on 25 October 2026. B01 remains open.
B02 and B03 were fixed in a later timing change and have regression checks.

## B01 — Power pellet and ghost contact in the same update

- **Priority:** high.
- **Location:** `Game.check_all_collisions` and `GameController.update_playing`.
- **Reproduction:** place an uneaten power pellet at the player position and
  collide with a ghost still in `chase` mode during the same collision pass.
- **Observed:** the player becomes powered but loses a life, from three to two.
- **Expected:** collecting the power pellet protects the player during the
  subsequent ghost collision in that pass.
- **Cause:** the ghost-mode update happens before pellet collection, and the
  collision code relies on the ghost's previous mode.

## B02 — Ghost respawn time continues during manual pause (fixed)

- **Priority:** medium.
- **Location:** `Game.toggle_pause`, `Ghost.time_eaten`, `GhostsManager.move_all`.
- **Reproduction:** eat a ghost, pause for longer than five seconds, then resume.
- **Observed:** the ghost can respawn immediately after resume. A simulated
  ten-second pause advanced the level's excluded pause time by 10,000 ms but
  left the ghost's eaten timestamp unchanged.
- **Expected:** a paused game also suspends this gameplay cooldown.
- **Original cause:** ghost respawn used monotonic elapsed time without a pause
  adjustment.
- **Fix:** on resume, add the paused duration to each eaten ghost's timestamp,
  alongside the existing level and player-power timer adjustments.
- **Regression:** a ten-second pause preserves all three timers. The ghost stays
  eaten at 4.9 active seconds and respawns after five active seconds.

## B03 — Actor movement depends on frame rate (fixed)

- **Priority:** medium.
- **Location:** `Player.move`, `Ghost.update`, and the main update loop.
- **Reproduction:** compare one second of updates at 30 FPS and 60 FPS while
  holding the same movement direction on an open route.
- **Observed:** the controlled player check moved 200 pixels in 30 updates and
  400 pixels in 60 updates. Each actor uses a fixed distance per update.
- **Expected:** distance per elapsed second should stay consistent when rendering
  slows down.
- **Fix:** GameController accumulates elapsed time and runs gameplay at sixty
  fixed updates per second. State transitions reset the accumulator, so menu and
  pause time do not become movement updates on resume.
- **Regression:** ten-second simulations at 20, 30, 60 and 144 render FPS each
  performed 600 updates, moving the player 4,200 pixels and a ghost 1,200 pixels
  on the controlled test route.

## Display limitation

The requested 1800×1200 window exceeds the inspected PC's 1024×768 desktop.
This is retained by request, not silently changed as part of cleanup.
