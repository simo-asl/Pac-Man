from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from ..game.highscore import score
    from .state_machine import StateMachine

from .draw import Draw
from .state import GameState


class Menu:
    def __init__(self, draw: Draw):
        self.draw = draw
        self.selected = 0
        self.height = self.draw.screen.get_height()
        self.title_size = max(36, self.height // 9)
        self.options_size = max(20, self.height // 20)
        self.spacing = max(35, self.height // 14)
        self.width = self.draw.screen.get_width()
        self.options = [
            "START GAME",
            "HIGHSCORES",
            "INSTRUCTIONS",
            "EXIT",
        ]
        self.backgrounds = {
            GameState.HIGHSCORES: "highscores.png",
            GameState.INSTRUCTIONS: "instructions.png",
            GameState.VICTORY: "victory.png",
            GameState.NAME_INPUT: "name_input.png",
            GameState.MENU: "main_menu.png",
        }
        self.images = {}
        for state, back in self.backgrounds.items():
            image = self.draw.load_image(f"src/game/assets/backgrounds/{back}")
            resu = pygame.transform.scale(image, (self.width, self.height))
            self.images[state] = resu

        self.machine = None

    def move_selection(self, direction: int) -> None:
        self.selected = (self.selected + direction) % len(self.options)

    def select(self) -> str:
        return self.options[self.selected]

    def draw_menu(self):
        self.draw.screen.fill((0, 0, 0))
        self.draw.draw_image(self.images[GameState.MENU], 0, 0)
        title_y = self.height // 8
        self.draw.draw_text(
            "PAC-MAN", self.width // 2, title_y, self.title_size, (255, 220, 50), True
        )
        menu_start_y = self.height // 3 - 50
        box_width = self.width // 3
        box_height = min(self.spacing - 8, self.options_size + 20)
        box_x = (self.width - box_width) // 2
        for i, op in enumerate(self.options):
            color = (255, 220, 50) if i == self.selected else (220, 220, 220)
            self.draw.draw_rect(
                box_x,
                menu_start_y - 25,
                box_width,
                box_height,
                color,
                10,
            )
            text = f"▶ {op}" if i == self.selected else f"  {op}"
            self.draw.draw_text(
                text, self.width // 2, menu_start_y, self.options_size, color, True
            )
            menu_start_y += self.spacing

    def draw_highscore(self, scores: list[score]) -> None:
        self.draw.screen.fill((0, 0, 0))
        self.draw.draw_image(self.images[GameState.HIGHSCORES], 0, 0)
        high_h = 150
        self.draw.draw_text(
            "HighScore",
            (self.width // 2),
            high_h,
            90,
            (155, 255, 252),
            centre=True,
        )
        t = 0
        space = int((self.height * 0.07) + self.height // 9)
        for i, s in enumerate(scores):
            self.draw.draw_text(
                f"{i + 1}--{s.name}:",
                (self.width // 2) - 50,
                (250) + t,
                43,
                (244, 244, 244),
                True,
            )
            self.draw.draw_text(
                str(s.score),
                (self.width // 2) + 50,
                (250) + t,
                43,
                (244, 244, 244),
                True,
            )
            t += space

    def set_machine(self, state_machine: StateMachine):
        self.machine = state_machine

    def _handle_menu_keys(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self.move_selection(1)
            elif event.key == pygame.K_RETURN:
                selected = self.select()
                if self.machine is None:
                    return
                if selected == "START GAME":
                    self.machine.change_state(GameState.PLAYING)
                elif selected == "HIGHSCORES":
                    self.machine.change_state(GameState.HIGHSCORES)
                elif selected == "INSTRUCTIONS":
                    self.machine.change_state(GameState.INSTRUCTIONS)
                else:
                    self.machine.running = False

    def handle_keys(
        self,
        state: GameState,
        event: pygame.event.Event,
    ) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self.machine is None:
            return
        match state:
            case GameState.MENU:
                if event.key == pygame.K_UP:
                    self.move_selection(-1)

                elif event.key == pygame.K_DOWN:
                    self.move_selection(1)

                elif event.key == pygame.K_RETURN:
                    selected = self.select()

                    if selected == "START GAME":
                        self.machine.game.start_game()

                    elif selected == "HIGHSCORES":
                        self.machine.change_state(GameState.HIGHSCORES)

                    elif selected == "INSTRUCTIONS":
                        self.machine.change_state(GameState.INSTRUCTIONS)

                    elif selected == "EXIT":
                        self.machine.running = False

            case GameState.HIGHSCORES | GameState.INSTRUCTIONS:
                if event.key == pygame.K_ESCAPE:
                    self.machine.change_state(GameState.MENU)

            case GameState.NAME_INPUT:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]

                elif event.key == pygame.K_RETURN:
                    if self.player_name.strip():
                        self.machine.change_state(GameState.HIGHSCORES)

                elif (
                    event.unicode.isascii()
                    and (event.unicode.isalnum() or event.unicode == " ")
                    and len(self.player_name) < 10
                ):
                    self.player_name += event.unicode

            case GameState.VICTORY:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.machine.change_state(GameState.MENU)

    def _draw_screen(self, state: GameState):
        self.draw.screen.fill((0, 0, 0))
        self.draw.draw_image(self.images[state], 0, 0)

    def run(
        self,
        state: GameState,
        keys: list[pygame.event.Event],
        **kwargs,
    ) -> None:
        for event in keys:
            self.handle_keys(state, event)
            if self.machine is not None and self.machine.state != state:
                return
        match state:
            case GameState.HIGHSCORES:
                self.draw_highscore(kwargs["scores"])
            case GameState.MENU:
                self.draw_menu()
            case GameState.INSTRUCTIONS:
                self._draw_screen(state)
            case GameState.VICTORY:
                self._draw_screen(state)
            case GameState.NAME_INPUT:
                self._draw_screen(state)
