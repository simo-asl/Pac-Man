import pygame

from src.ui.state import GameState
from src.ui import Draw
from src.ui.menu import Menu
from src.game.player import Player
from src.maze import Maze
from src.game.ghost_manger import GhostsManager
from src.game import Game
from src.game.cheats import Cheats
from src.parsing.parser import GameConfig
from src.game.highscore import High


class GameController:
    def __init__(
        self,
        screen: pygame.Surface,
        config: GameConfig,
    ) -> None:
        self.screen = screen
        self.config = config
        self.state = GameState.MENU
        self.running = True

        self.drawer = Draw(screen)
        self.menu = Menu(self.drawer)

        self.highscores = High("highscores.json")
        self.player_name = ""
        self.name_error = ""

    def start_game(self) -> None:
        self.level = 0

        self.game = Game(
            self.screen,
            self.screen.get_width(),
            self.screen.get_height(),
            config=self.config,
        )

        self.remaining_lives = self.config.lives

        self.setup_level()

    def setup_level(self) -> None:
        self.maze = Maze(
            self.config,
            self.drawer,
            self.level,
            self.screen.get_size(),
        )

        self.maze_surface = pygame.Surface(self.screen.get_size())
        self.maze_surface.fill((0, 0, 0))

        original_screen = self.drawer.screen
        self.drawer.screen = self.maze_surface

        try:
            self.maze.draw_maze()
        finally:
            self.drawer.screen = original_screen

        player_spawn = self.maze.grid_to_pixel(5, 5)

        self.player = Player(
            player_spawn[0],
            player_spawn[1],
            10,
            self.maze.WI,
            self.maze.HE,
            lives=self.remaining_lives,
        )

        self.game.s_width = self.maze.WI
        self.game.s_height = self.maze.HE

        ghost_corners = [
            (self.maze.columns - 1, 0),
            (0, 0),
            (self.maze.columns - 1, self.maze.rows - 1),
            (0, self.maze.rows - 1),
        ]

        superpac_positions = [
            self.maze.grid_to_pixel(x, y)
            for x, y in ghost_corners
        ]

        positions = self.maze.get_walkable_positions()

        for position in superpac_positions:
            if position in positions:
                positions.remove(position)

        if player_spawn in positions:
            positions.remove(player_spawn)

        self.pacgums = self.game.create_pacgums(positions)
        self.superpacgums = self.game.create_superpac(superpac_positions)

        self.ghosts = GhostsManager(
            self.drawer,
            self.maze,
            self.player,
        )

        ghosts_config = [
            ("blinky", 2),
            ("pinky", 2),
            ("inky", 1),
            ("clyde", 2),
        ]

        for (kind, direction), corner in zip(ghosts_config, ghost_corners):
            self.ghosts.create_ghost(
                corner[0],
                corner[1],
                direction,
                corner,
                kind,
            )

        self.cheats = Cheats(
            self.player,
            self.game,
            self.ghosts,
        )

        self.change_state(GameState.PLAYING)

    def next_level(self) -> None:
        # hadi 7et lmaze zwina dyalk ma kadirch check lconfig.levels ch7al
        # une fois kaytsalaw levels kayt7sb bli khssr so 9ad chi l3ba dl victory
        if self.level + 1 >= len(self.config.levels):
            self.change_state(GameState.GAME_OVER)
            return

        self.remaining_lives = self.player.lives

        self.game.next_level()
        self.level += 1

        self.setup_level()

    def change_state(self, new_state: GameState) -> None:
        self.state = new_state

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

    def handle_menu_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_DOWN:
            self.menu.move_selection(1)

        elif event.key == pygame.K_UP:
            self.menu.move_selection(-1)

        elif event.key == pygame.K_RETURN:
            action = self.menu.select()

            match action:
                case "START GAME":
                    self.start_game()

                case "HIGHSCORES":
                    self.change_state(GameState.HIGHSCORES)

                case "INSTRUCTIONS":
                    self.change_state(GameState.INSTRUCTIONS)

                case "EXIT":
                    self.running = False

        elif event.key == pygame.K_ESCAPE:
            self.running = False

    def handle_playing_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_p:
            self.game.toggle_pause(self.player)
            self.change_state(GameState.PAUSED)

        elif self.cheats.handle_key(event.key):
            self.next_level()

    def handle_paused_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_p:
            self.game.toggle_pause(self.player)
            self.change_state(GameState.PLAYING)

    def handle_highscores_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.change_state(GameState.MENU)

    def handle_instructions_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.change_state(GameState.MENU)

    # hna khoud input mn 3nd luser gamestate.NAME_INPUT
    def handle_game_over_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RETURN:
            self.player_name = ""
            self.name_error = ""
            self.change_state(GameState.NAME_INPUT)

    def handle_name_input_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]

        elif event.key == pygame.K_RETURN:
            if not self.highscores.valid_name(self.player_name):
                self.name_error = "INVALID NAME"
                return

            if self.highscores.add_score(self.player_name, self.game.score):
                self.change_state(GameState.HIGHSCORES)
            else:
                self.name_error = "COULD NOT SAVE SCORE"

        elif len(self.player_name) < 8:
            char = event.unicode

            if char.isascii() and (char.isalnum() or char == " _"):
                self.player_name += char
                self.name_error = ""

    def handle_level_complete_event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RETURN:
            self.next_level()

    def update(self) -> None:
        if self.state == GameState.PLAYING:
            self.update_playing()

    def update_playing(self) -> None:
        self.game.update_death(self.player, self.ghosts)

        if not self.game.manual_pause and self.game.level_time_remaining() == 0:
            self.player.dead()

        if (
            not self.game.paused
            and not self.game.manual_pause
            and self.player.alive
        ):
            self.player.move(self.maze)
            self.player.update_power()

            if self.player.powered_up:
                self.ghosts.frighten_all()
            else:
                self.ghosts.restore_all()

            self.ghosts.move_all()

            self.game.check_all_collisions(
                self.player,
                self.superpacgums,
                self.pacgums,
                self.ghosts,
            )

            self.ghosts.update_all()

            if self.player.alive and self.game.level_complete(
                self.pacgums,
                self.superpacgums,
            ):
                self.change_state(GameState.LEVEL_COMPLETE)
                return

        if not self.player.alive:
            self.change_state(GameState.GAME_OVER)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))

        match self.state:
            case GameState.MENU:
                self.draw_menu()

            case GameState.PLAYING:
                self.draw_playing()

            case GameState.PAUSED:
                self.draw_paused()

            case GameState.HIGHSCORES:
                self.draw_highscores()

            case GameState.INSTRUCTIONS:
                self.draw_instructions()

            case GameState.GAME_OVER:
                self.draw_game_over()

            case GameState.NAME_INPUT:
                self.draw_name_input()

            case GameState.LEVEL_COMPLETE:
                self.draw_level_complete()

    # tempo + not my part
    def draw_menu(self) -> None:
        self.menu.draw_menu()

    # t3deb aw9 khdem l HUD
    def draw_hud(self) -> None:
        pass

    def draw_playing(self) -> None:
        self.screen.blit(self.maze_surface, (0, 0))

        for pacgum in self.pacgums:
            pacgum.draw(self.drawer)

        for superpac in self.superpacgums:
            superpac.draw(self.drawer)

        self.player.draw(self.screen)
        self.ghosts.draw_all()

    # tempo + not my part
    # kanktb ghir paused nta dir features jdad la bghtiti
    def draw_paused(self) -> None:
        self.draw_playing()

        self.drawer.draw_text(
            "PAUSED",
            self.screen.get_width() // 2,
            self.screen.get_height() // 2,
            80,
            (255, 255, 255),
            True,
        )

    # tempo + not my part
    def draw_highscores(self) -> None:
        scores = self.highscores.get_top_scores()
        self.menu.draw_highscore(scores)

    # tempo + not my part + don't forget to add cheats
    def draw_instructions(self) -> None:
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        instructions = [
            "HOW TO PLAY",
            "ARROW KEYS - MOVE",
            "P - PAUSE / RESUME",
            "EAT PACGUMS TO SCORE",
            "SUPER PACGUMS GIVE YOU POWER",
            "AVOID GHOSTS",
            "ESC - BACK TO MENU",
        ]

        for index, text in enumerate(instructions):
            self.drawer.draw_text(
                text,
                center_x,
                center_y - 240 + index * 80,
                45 if index else 70,
                (255, 255, 0) if index == 0 else (255, 255, 255),
                True,
            )

    # tempo + not my part + rsem chi l3ba wla animation
    def draw_game_over(self) -> None:
        self.draw_playing()

        self.drawer.draw_text(
            "DIR CHI KHRYA",
            self.screen.get_width() // 2,
            self.screen.get_height() // 2,
            90,
            (255, 0, 0),
            True,
        )

    # tempo + not my part + khssha khdma kter
    def draw_name_input(self) -> None:
        self.screen.fill((0, 0, 0))

        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        self.drawer.draw_text(
            "ENTER YOUR NAME",
            center_x,
            center_y - 100,
            70,
            (255, 255, 0),
            True,
        )

        self.drawer.draw_text(
            self.player_name + "_",
            center_x,
            center_y,
            55,
            (255, 255, 255),
            True,
        )

        self.drawer.draw_text(
            f"SCORE: {self.game.score}",
            center_x,
            center_y + 80,
            45,
            (255, 255, 255),
            True,
        )

        if self.name_error:
            self.drawer.draw_text(
                self.name_error,
                center_x,
                center_y + 150,
                35,
                (255, 0, 0),
                True,
            )

    # dir chi pic wla whatever
    def draw_level_complete(self) -> None:
        self.draw_playing()

        self.drawer.draw_text(
            "DIR CHI KHRYA",
            self.screen.get_width() // 2,
            self.screen.get_height() // 2,
            80,
            (255, 255, 0),
            True,
        )
