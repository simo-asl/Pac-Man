# Team contributions and decisions

## Contributions visible in Git

The README identifies the team as `tlaghzal` and `mel-asla`. Git contains the
author names below. The variants of Mohammed El Aslaouy / Moha Del Rey share
the same recorded email address. Commit authorship establishes who recorded
a change; it does not establish exclusive ownership or hours worked.

| Git identity | Work visible in representative commits |
| --- | --- |
| tlaghzal | Draw, maze adapter and parser foundations (`a8ae643`, `551ca1c`, `d7e178a`); ghost graphics/movement (`523f750`, `77dd2cf`); cached drawing (`a0080d7`); menu and wall work (`5a41a1b`, `219caa7`); recent integration and cleanup (`975ae67`, `e61b8fc`, `04f958e`) |
| Mohammed El Aslaouy / Moha Del Rey / Moha del rey | Player/game/pellet logic (`09292ce`); integration (`ea02bf2`); cheats (`fcc2722`); graphics restrictions (`662efad`); timer and pause (`fb87fd8`, `7609758`); highscore validation (`50b47d9`, `d830d4c`); controller and progression (`7bfb2b2`, `0c42a12`) |

The [timeline](TIMELINE.md) links the main commits. No formal initial task
allocation or meeting record was found. Both contributors should be able to
explain the complete game during evaluation.

## Current technical choices

These explanations describe the code and its tradeoffs; they are not invented
minutes of earlier discussions.

| Choice | Reason and tradeoff |
| --- | --- |
| Pygame behind Draw | Keep a Python window/input backend while using image and pixel operations comparable to MLX42. See [the API comparison](../MLX.md). |
| External MazeGenerator wheel | Use the assigned generator unchanged. Maze adapts its grid and wall masks rather than modifying the dependency. |
| Hjson and Pydantic | Delegate comment parsing and validation to libraries; small recovery functions preserve valid sibling values. Hjson accepts more syntax than strict JSON. |
| Menu plus MenuView | Navigation and score submission stay separate from page drawing without introducing a UI framework. |
| Pre-drawn Tamzen BDF font | Read existing bitmap glyphs through bdfparser; no TrueType rasterization is needed. The font license is bundled. |
| Cached maze and bitmap rows | Load the maze image and decoded bitmap rows once; draw letters with plain pixel loops and integer scales. |
| JSON top-ten highscores | Small, inspectable local storage without a database. File errors are handled, but writes are not transactional. |
| Temporary test programs | Run focused checks outside the submitted source, consistent with the subject's testing guidance; keep repeatable procedures in the acceptance record. |

## Blockers and changes in direction

- Graphics restrictions required replacing unsupported helpers and documenting
  the Paris/Codam API differences; the project still uses Pygame as its backend.
- Passing `None` as a later-level seed caused the assigned generator to fail.
  Explicit random integer seeds now support the `S` skip flow.
- The merged architecture/artwork version was not kept wholesale. History was
  reconciled without force-pushing, preserving the selected earlier baseline.
- A small test window was tried, then restored to 1800×1200 at the user's request.
- No evidence of a personal team conflict was found; no such conflict is claimed.
