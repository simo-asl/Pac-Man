# Subject readiness — October 25, 2026

This is the current audit against `en.subject.pdf` version 1.5, not a claim that
all external submission requirements are finished.

| Subject area | Current evidence / status |
| --- | --- |
| Python / modular classes | Implemented in `src/`; Python 3.12 selected |
| flake8 / required mypy flags | `make lint` passes |
| Type hints and docstrings | All 122 functions audited; Google Args/Returns, relevant Raises, explicit parameter/return types |
| Required Makefile targets | install, run, debug, clean, lint present |
| One JSON argument / no traceback | Usage, missing file, invalid extension and syntax checked |
| Config comments / defaults / ignored keys | Full-line # and //; invalid fields recover independently |
| Assigned generator / perfect=False | Explicit call, supplied wheel unchanged |
| Generation failure | Mocked failure returns to menu with an error |
| Ten levels / fixed first seed / random later | Implemented; all ten transitions exercised |
| Player / corridors / respawn / life loss | Bounds, collision and respawn checked |
| Four corner ghosts and power pellets | Created at level setup |
| Ghost chase / flee / eaten respawn | Frame-independent speed, legal turns, chase/flee routes, frozen state and timer checks pass |
| Most corridors contain pellets | At least 70% coverage; reachable positions checked |
| Score and lives persist between levels | Checked across all ten levels |
| Level timer / pause | Timer excludes pauses; timeout ends the game |
| Menu / HUD / pause / instructions | Rendered and keyboard paths checked |
| Win/loss final score / required name | Shared name entry and persistence checked |
| Top-ten persistent highscores | Missing/corrupt input, sorting and save flow checked |
| Cheat mode | I/F/L/S available; instructions document keys |
| Packaging sources | `make package` succeeds; executable error handling and off-directory menu startup checked |
| Public free restricted/unlisted deployment | **Pending**: upload the release to a gaming platform and record URL |
| Project-management documentation | This audit and acceptance notes in this directory |
| Required README sections | Included; controls, config/defaults, architecture and credits |
| MLX-equivalent graphical functions | **Peer review required**: see note below |
| Real desktop / full interactive playthrough | **Pending**: this environment reports offscreen SDL |

The subject restricts graphics APIs to functions with MLX equivalents. The app
uses Pygame window/events, image buffers, blitting, text, pixel filling, and image
loading, with its own line/circle/wall drawing. `pygame.draw` calls have been
removed. Sprite scaling, alpha overlays, and font rendering still
use Pygame APIs. Review their equivalence with the evaluator; this audit does not
certify that the chosen library is accepted merely because the game runs.

No hosting account was configured or published during this work. No historical
team plan or authorship allocation was invented.
