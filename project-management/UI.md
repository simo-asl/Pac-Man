# Simple UI pass

Reviewed the UI requirements in `en.subject.pdf`, section VI.8. The fixed
2100×1800 window retains its simple keyboard flow. The latest quality
pass remasters the character sprites, renders native-resolution backgrounds,
and smooths wall geometry. Ghost movement and maze limits are covered separately
in CHECKLIST.md and CHANGES.md.

## Screen behavior

| Required screen | Current presentation |
| --- | --- |
| Main menu | Start Game, Highscores, Instructions, Exit; one gold keyboard selection |
| High scores | Top ten with separate rank, player and right-aligned score columns |
| Instructions | Static controls and rules; Enter/Escape returns |
| Gameplay HUD | Lives, level, score, remaining time; saved best also visible |
| Pause | Resume and Main Menu; selection and resume shortcuts visible |
| Game Over | Final score and Enter to name entry |
| Victory | Congratulations, final score and Enter to name entry |
| Name entry | Focused field, placeholder, 10-character counter and save feedback |

The same dark panels, muted labels and gold highlights are reused throughout.
Native background details stay outside the playable grid. The HUD has a solid dark
backing, with a larger current score and a red time warning near zero. Gameplay's
footer shows movement and pause; cheat controls remain on Instructions.

## Small files with clear jobs

- `src/ui/menu.py`: existing input, navigation, required-name validation and saving.
- `src/ui/menu_view.py`: drawing for the menu, table, instructions and name entry.
- `src/ui/panels.py`: shared colors, option highlight, pause panel and result card.
- `src/ui/game_ui.py`: cached maze background, live HUD and overlay calls.
- `src/ui/draw.py`: raster helpers, cached fonts, text measurement and fitting.
- `src/ui/background.py`: cached native-resolution gradient and corner details.

No screen framework, extra state machine or inheritance hierarchy was introduced.

## Code snippets

Menu rendering now delegates after existing keyboard handling:

```python
case GameState.INSTRUCTIONS:
    self.view.instructions()
case GameState.VICTORY:
    self.view.victory(self.machine.game.game.score)
case GameState.NAME_INPUT:
    self.view.name_input(
        self.machine.game.game.score, self.player_name, self.name_error,
    )
```

`MenuView` only receives the values it displays. It does not read game state,
change screens, or save files. Menu's input handling retains those jobs.

Menu and pause options use the same highlight:

```python
panel(draw, rect, GOLD if active else LINE)
if active:
    draw.screen.fill(GOLD, (rect.x, rect.y, 5, rect.height))
```

The thin gold edge and border mark the actual keyboard selection. Options are
spaced using the available panel dimensions; text uses measured font height.

Win, loss and level completion share one result renderer:

```python
result(
    self.draw,
    "GAME OVER",
    self.game.score,
    "ENTER  SAVE YOUR SCORE",
    ERROR,
)
```

It draws the heading, optional congratulatory message, score label, large score
and next action in consistent positions. The caller supplies the real score.

Text fitting handles large scores without overflowing their columns:

```python
def fit_text(self, text: str, size: int, max_width: int) -> int:
    width = self.measure_text(text, size)[0]
    if width > max_width:
        size = max(1, size * max_width // width)
        while size > 1 and self.measure_text(text, size)[0] > max_width:
            size -= 1
    return size
```

The existing font cache supplies the measurements. Size is reduced only when
text exceeds its assigned space; ordinary labels keep their normal size.

## Verification

- `make lint`: flake8 and all required mypy flags pass.
- Python compilation and whitespace checks pass.
- Headless checks cover all four main-menu paths, pause/resume, both game endings,
  empty names, save failure/retry, successful saves, and return to the menu.
- Rendering checks cover all screens at 2100×1800, ten maximum-length player
  names, empty scores, unusually large scores, and text staying inside the window.
- Menu, populated score table, instructions, victory, name entry and pause
  screenshots were inspected. Tests use temporary score files.
- Real-monitor interactive playthrough remains an external acceptance step.
