# Risks and release gates

Review date: 25 October 2026. These are risks and follow-up actions, not claims
that the actions have already been completed.

| Risk | Impact | Current mitigation | Remaining action |
| --- | --- | --- | --- |
| No standalone package or platform build | Required delivery cannot be demonstrated | Source launch and installed entry point are available | Add a root packaging script/spec; build, upload and test the distribution |
| Gameplay defects | Incorrect life loss, pause timing or movement speed | The remaining same-frame collision bug and two timing fixes are recorded in [BUGS.md](BUGS.md) | Team prioritizes and fixes them separately |
| Graphics-equivalence interpretation | Evaluators may question library calls | Bitmap font and pixel/image operations are documented in [MLX.md](../MLX.md) | Review the comparison with evaluators; do not claim Paris Linux PNG support |
| Generator reinstallation or interface differences | Levels may fail to load during review | Use the supplied wheel unchanged and return to the menu on generation failure | Reinstall the assigned package on a clean setup and repeat generation checks |
| Highscore destination unwritable | Player cannot persist a score | Error feedback leaves name entry open for retry | Test the packaged build's writable destination |
| Interrupted highscore write | Local scores may be lost | Load errors produce an empty leaderboard rather than a crash | Consider safe replacement writes in a later change |
| Fixed 1800×1200 window | Parts of the game can be offscreen on a small monitor | Size and limitation are documented | Choose a suitable evaluation display or agree on a later sizing change |
| Cleanup removes a dynamically loaded file | Missing images can prevent startup or a later screen | Keep explicit manifests and run all screens, sprites and levels after moves | Repeat the asset audit whenever paths change |
| Incomplete historical planning evidence | The management account could overstate the process | Clearly label the timeline as reconstructed from commits | Team confirms contributions and adds any genuine existing records |

Release gate: required code checks, the acceptance scenarios, the open-bug
review, a clean-install package test, and a platform-launch test must be reviewed
before declaring the project ready for defense.
