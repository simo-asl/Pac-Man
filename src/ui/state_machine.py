import pygame

from ..game_controller import GameController
from .menu import Menu
from .state import GameState


class StateMachine:
    def __init__(self, menu: Menu, game: GameController):
        self.menu = menu
        self.game = game
        self.state = GameState.MENU

    # def select(self, )
    def change_state(self, new_state: GameState) -> None:
        self.state = new_state

    def handle_menu_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_DOWN:
            self.menu.move_selection(1)

        elif event.key == pygame.K_UP:
            self.menu.move_selection(-1)

        elif event.key == pygame.K_RETURN:
            action = self.menu.select()

            match action:
                case "START GAME":
                    self.game.start_game()

                case "HIGHSCORES":
                    self.change_state(GameState.HIGHSCORES)

                case "INSTRUCTIONS":
                    self.change_state(GameState.INSTRUCTIONS)

                case "EXIT":
                    self.running = False

        elif event.key == pygame.K_ESCAPE:
            self.running = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type != pygame.KEYDOWN:
            return

        match self.state:
            case GameState.MENU:
                self.handle_menu_event(event)

            case GameState.PLAYING:
                self.handle_playing_event(event)

            case GameState.PAUSED:
                self.handle_paused_event(event)

            case GameState.HIGHSCORES:
                self.handle_highscores_event(event)

            case GameState.INSTRUCTIONS:
                self.handle_instructions_event(event)

            case GameState.GAME_OVER:
                self.handle_game_over_event(event)

            case GameState.NAME_INPUT:
                self.handle_name_input_event(event)

            case GameState.LEVEL_COMPLETE:
                self.handle_level_complete_event(event)

    def run(self):
        self.select
