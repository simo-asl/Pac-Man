# Timeline and progress

This is a retrospective timeline based on commit dates and changed files.
Dates are those recorded by Git authors; merges can make adjacent entries
appear out of date order. They do not measure hours worked.

## Actual milestones

| Date | Work visible in history | Evidence |
| --- | --- | --- |
| 4 October | Graphics choice, Draw, maze adapter, movement checks, initial parser | [9c39b4d](https://github.com/simo-asl/Pac-Man/commit/9c39b4d), [a8ae643](https://github.com/simo-asl/Pac-Man/commit/a8ae643), [d7e178a](https://github.com/simo-asl/Pac-Man/commit/d7e178a) |
| 5 October | Player, game and pellet integration; initial cheats | [09292ce](https://github.com/simo-asl/Pac-Man/commit/09292ce), [bbb2c8d](https://github.com/simo-asl/Pac-Man/commit/bbb2c8d), [fcc2722](https://github.com/simo-asl/Pac-Man/commit/fcc2722) |
| 7 October | Ghost images and smoother movement | [523f750](https://github.com/simo-asl/Pac-Man/commit/523f750), [77dd2cf](https://github.com/simo-asl/Pac-Man/commit/77dd2cf) |
| 15 October | Integration and removal of unsupported drawing methods | [27af9c3](https://github.com/simo-asl/Pac-Man/commit/27af9c3), [662efad](https://github.com/simo-asl/Pac-Man/commit/662efad) |
| 17 October | Timer, pause, pellet placement and cached maze drawing | [fb87fd8](https://github.com/simo-asl/Pac-Man/commit/fb87fd8), [7609758](https://github.com/simo-asl/Pac-Man/commit/7609758), [a0080d7](https://github.com/simo-asl/Pac-Man/commit/a0080d7) |
| 20–21 October | Highscore work and invalid-JSON feedback | [133ffc0](https://github.com/simo-asl/Pac-Man/commit/133ffc0), [50b47d9](https://github.com/simo-asl/Pac-Man/commit/50b47d9), [d830d4c](https://github.com/simo-asl/Pac-Man/commit/d830d4c) |
| 22–23 October | Menu progress, state machine, controller, level skipping and result screens | [11266e2](https://github.com/simo-asl/Pac-Man/commit/11266e2), [f9644b2](https://github.com/simo-asl/Pac-Man/commit/f9644b2), [7bfb2b2](https://github.com/simo-asl/Pac-Man/commit/7bfb2b2), [5a41a1b](https://github.com/simo-asl/Pac-Man/commit/5a41a1b) |
| 24 October | Wall artwork, ten default levels and a controller indexing fix | [219caa7](https://github.com/simo-asl/Pac-Man/commit/219caa7), [f94d34f](https://github.com/simo-asl/Pac-Man/commit/f94d34f), [7c7bd16](https://github.com/simo-asl/Pac-Man/commit/7c7bd16) |
| 25 October | Bitmap font, setup, parser/UI repairs, level-skip recovery and documentation | [975ae67](https://github.com/simo-asl/Pac-Man/commit/975ae67) |
| 25 October | Ghost routing and respawn checks, pause instructions, loss messages | [e61b8fc](https://github.com/simo-asl/Pac-Man/commit/e61b8fc) |
| 25 October | Separate menu input and drawing; simplify configuration recovery | [04f958e](https://github.com/simo-asl/Pac-Man/commit/04f958e) |

## Integration history

`8ba0653` merged the architecture branch. `477e187` later reconciled that
history while keeping the earlier selected game baseline plus the new fixes.
The current tree, not every historical implementation, defines the release.
For example, older packaging files are not present in the current tree.

## Progress against the required deliverables

| Deliverable | Current position | Next acceptance step |
| --- | --- | --- |
| Playable game loop | Implemented; selected automated scenarios pass | Complete a manual game from start to name entry |
| Configuration and recovery | Nineteen edge cases pass | Edit the supplied config during a manual run |
| Highscores and required screens | Implemented; save/retry and rendering scenarios pass | Check persistence across two real launches |
| Code quality | Required Flake8 and Mypy commands pass | Re-run before each release |
| Documentation | README and management records prepared in this review | Team checks factual accuracy |
| Packaging | Pending | Add root build script/spec and rebuild on a clean setup |
| Platform release | Pending | Upload and test a free unlisted/private build |

There is no original committed deadline baseline, so schedule variance cannot
be calculated honestly. The pending rows above are the forward release plan.
