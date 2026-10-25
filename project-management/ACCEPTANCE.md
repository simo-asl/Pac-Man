# Acceptance checks

Review date: 25 October 2026. The checks below cover the reviewed source tree;
they do not certify an unpublished standalone package.

## Checks executed

The required lint commands were run through `make lint`. Focused temporary
Python harnesses were run outside the submitted repository. The procedures
below record what they checked; they are not a claim of a manual playthrough.

| Check | Result | Scope |
| --- | --- | --- |
| Flake8 and subject Mypy flags | Pass | Current Python source |
| Parser edge cases | Pass, 19 cases | Empty/malformed input, unterminated comments, wrong root types, comment-only input, wrong numeric types, invalid levels and seeds, level count, deep nesting, quoted comment markers, sibling recovery, missing/non-JSON files, UTF-8 and permission errors |
| Menu/parser regressions | Pass, 6 tests | Config recovery, comments, invalid input, save/retry and win/loss navigation, all menu/result pages, generation-error recovery |
| Level skip | Pass | Press `S` through all ten levels; preserve score/lives; reach victory; handle a generation failure |
| Ghost checks | Pass | Detour around walls, respawn while between cells, return edible when power remains |
| Pause and loss screens | Pass | Instructions keep the game paused; Back returns to pause; resume; life-loss/game-over text |
| Runtime assets | Checked after organization | Every retained PNG is loaded through the game/menu paths; font and license are retained |
| Gameplay timing | Pass | Ghost respawn, power and level time survive pause; movement matches at 20/30/60/144 render FPS |
| Error handling | Pass | Failed gameplay screen returns to menu; main-menu/startup failures and Ctrl+C produce clear messages; missing-image errors identify the path |
| Open-bug reproduction | B01 confirmed | Same-frame power-pellet/ghost contact remains open; B02 and B03 are fixed |

## Manual procedures still required

| ID | Procedure | Expected outcome | Status |
| --- | --- | --- | --- |
| A01 | Install dependencies on a clean machine; run `python3 pac-man.py config.json` | Menu opens; no missing assets or traceback | Pending clean-machine test |
| A02 | Start a game, move against walls, collect normal/power pellets and contact ghosts | Walls hold; scoring and lives follow the rules | Pending manual play; B01 remains open |
| A03 | Pause, open Instructions, return, resume, then choose Main Menu | Game remains frozen until resume; all choices work | Automated checks pass; manual confirmation pending |
| A04 | Run the timer out, save a valid name, exit and relaunch | Final score shown; saved name/score persists | Save flow checked; two-launch manual test pending |
| A05 | Enter an empty name, invalid punctuation, and more than ten characters | Invalid input is rejected without leaving the form | Empty-name check passes; full manual input check pending |
| A06 | Prepare more than ten scores and a corrupt/unwritable score file | Top ten shown; file errors handled and retry remains possible | Retry checked; complete persistence matrix pending |
| A07 | Finish every level by collecting pellets rather than using `S` | Score/lives carry forward; victory leads to name entry | Pending full playthrough |
| A08 | Edit dimensions, score values, seed and lives in a commented config | Valid changes apply; invalid fields default with clear messages | Automated parser cases pass; live review pending |
| A09 | Rebuild a package from a root script/spec and launch it on a clean setup | Controls, configuration and persistence work without the source checkout | Pending; packaging script/spec missing |
| A10 | Launch the free unlisted/private platform build | Installation and play work through the selected platform | Pending; no release verified |

## Repeating source checks

```sh
make install
make lint
make run
```

For a parser case, create a temporary `.json` file with one changed field and
launch it with `make run ARGS=/path/to/case.json`. Confirm the warning and the
resulting setting. For a ghost/skip check, use the documented cheats and verify
the HUD, state transition and saved score. Keep test-generated highscores out of
source commits unless deliberately updating the example data.
