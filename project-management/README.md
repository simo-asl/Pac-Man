# Project management

Review date: 25 October 2026. Historical baseline: `04f958e`.

This directory reconstructs the work from Git history and records the current
release checklist. It does not claim that a planning document existed before
implementation: no original dated schedule or meeting notes were found.

## Documents

| Document | Purpose |
| --- | --- |
| [Timeline](TIMELINE.md) | Actual milestones, commit evidence, and remaining work |
| [Team and decisions](TEAM_AND_DECISIONS.md) | Observed contributions and technical choices |
| [Risks](RISKS.md) | Delivery risks and practical mitigations |
| [Acceptance tests](ACCEPTANCE.md) | Checks run, results, and manual test procedures |
| [Open bugs](BUGS.md) | Reproduced defects, listed without changing behavior |
| [Cleanup](CLEANUP.md) | Asset inventory and dead-code removal |

## How progress is recorded

Each completed milestone links to a commit or a recorded check. A commit
message is evidence of a change, not proof that every affected feature passed
review. Test results distinguish automated headless checks from manual play.
Remaining tasks are marked pending rather than assigned invented dates or
owners. Both contributors should review the release checklist before defense.

## Current status

- Implemented: configuration recovery, ten-level progression, player and ghost
  behavior, scoring, persistent highscores, menus, pause, instructions and cheats.
- Checked: lint, parser edge cases, menu flows, level skipping and selected ghost
  behavior. See the acceptance record for the scope of these checks.
- Open: three reproduced gameplay bugs and the fixed-window display limitation.
- Pending: a full manual playthrough, a root packaging script/spec, a tested
  standalone distribution, and an unlisted/private platform release.

## Evidence

The history can be inspected without relying on this summary:

```sh
git log --all --date=short --format='%h %ad %an | %s'
git show --stat 7bfb2b2
git show --stat e61b8fc
git show --stat 04f958e
```
