import pygame

from src.game import Game
from src.game.cheats import Cheats
from src.game.ghost_manger import GhostsManager
from src.game.player import Player
from src.maze import Maze
from src.parsing.parser import GameConfig
from src.ui import Draw
from src.ui.game_ui import GameUi
from src.ui.state import GameState


class GameController:
    def __init__(
        self,
        screen: pygame.Surface,
        config: GameConfig,
    ) -> None:
        self.screen = screen
        self.config = config
        self.drawer = Draw(screen)
        self.machine = None
        self.started = False

    def set_machine(self, machine) -> None:
        self.machine = machine

    def start_game(self) -> None:
        self.level = 0
        self.started = True

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

        player_spawn = self.maze.grid_to_pixel(5, 5)

        self.player = Player(
            player_spawn[0],
            player_spawn[1],
            10,
            self.maze.WI,
            self.maze.HE,
            lives=self.remaining_lives,
        )
        self.game_ui = GameUi(self.drawer, self.player, self.game, self.maze)

        self.game.s_width = self.maze.WI
        self.game.s_height = self.maze.HE

        ghost_corners = [
            (self.maze.columns - 1, 0),
            (0, 0),
            (self.maze.columns - 1, self.maze.rows - 1),
            (0, self.maze.rows - 1),
        ]

        superpac_positions = [self.maze.grid_to_pixel(x, y) for x, y in ghost_corners]

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
            self.change_state(GameState.VICTORY)
            return

        self.remaining_lives = self.player.lives

        self.game.next_level()
        self.level += 1

        self.setup_level()

    def change_state(self, new_state: GameState) -> None:
        if self.machine is None:
            raise RuntimeError("GameController needs set_machine(machine) first")
        self.machine.change_state(new_state)

    def handle_keys(
        self,
        state: GameState,
        event: pygame.event.Event,
    ) -> None:
        if event.type != pygame.KEYDOWN:
            return

        match state:
            case GameState.PLAYING:
                if event.key == pygame.K_p:
                    self.game.toggle_pause(self.player)
                    self.change_state(GameState.PAUSED)
                elif self.cheats.handle_key(event.key):
                    self.next_level()

            case GameState.PAUSED:
                if event.key == pygame.K_p:
                    self.game.toggle_pause(self.player)
                    self.change_state(GameState.PLAYING)

            case GameState.GAME_OVER:
                if event.key == pygame.K_RETURN:
                    self.change_state(GameState.NAME_INPUT)

            case GameState.LEVEL_COMPLETE:
                if event.key == pygame.K_RETURN:
                    self.next_level()

    def run(
        self,
        state: GameState,
        keys: pygame.event.Event | list[pygame.event.Event] | None = None,
        **kwargs,
    ) -> None:
        if not self.started:
            return

        if keys is not None:
            events = [keys] if isinstance(keys, pygame.event.EventType) else keys
            for event in events:
                self.handle_keys(state, event)
                if self.machine.state != state:
                    break

        # A transition (e.g. pause) must not update gameplay again.
        if state == GameState.PLAYING and self.machine.state == state:
            self.update_playing()

        self.screen.fill((0, 0, 0))
        match state:
            case GameState.PLAYING:
                self.draw_playing()
            case GameState.PAUSED:
                self.draw_paused()
            case GameState.GAME_OVER:
                self.draw_game_over()
            case GameState.LEVEL_COMPLETE:
                self.draw_level_complete()

    def update_playing(self) -> None:
        self.game.update_death(self.player, self.ghosts)

        if not self.game.manual_pause and self.game.level_time_remaining() == 0:
            self.player.dead()

        if not self.game.paused and not self.game.manual_pause and self.player.alive:
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

    def draw_playing(self) -> None:
        self.game_ui.menu_game()

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
