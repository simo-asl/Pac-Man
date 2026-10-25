"""Connect gameplay objects, keyboard input and screen states."""

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.ui.state_machine import StateMachine

from src.game.pacgum import Pacgum, SuperPacgum

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
    """Connect gameplay objects to the screen state machine."""

    def __init__(
        self,
        screen: pygame.Surface,
        config: GameConfig,
    ) -> None:
        """Initialize this object and its dependencies.

        Args:
            screen: Surface used to display or draw the game.
            config: Validated gameplay configuration.

        Returns:
            None.
        """
        self.screen = screen
        self.config = config
        self.drawer = Draw(screen)
        self.machine: StateMachine | None = None
        self.game: Game
        self.maze: Maze
        self.player: Player
        self.ghosts: GhostsManager
        self.cheats: Cheats
        self.game_ui: GameUi
        self.pacgums: list[Pacgum]
        self.superpacgums: list[SuperPacgum]
        self.started = False
        self.pause_selected = 0
        self.frame_clock = pygame.time.Clock()

    def set_machine(self, machine: "StateMachine") -> None:
        """Connect this screen to the application state machine.

        Args:
            machine: Application state machine connected to this scene.

        Returns:
            None.
        """
        self.machine = machine

    def start_game(self) -> None:
        """Create a new game with the configured lives and score reset.

        Returns:
            None.
        """
        self.level = 0
        self.started = True

        self.game = Game(
            self.screen,
            self.screen.get_width(),
            self.screen.get_height(),
            config=self.config,
        )

        self.remaining_lives = self.config.lives

        try:
            self.setup_level()
        except (ValueError, RuntimeError, IndexError, OSError) as error:
            self.started = False
            if self.machine is not None:
                self.machine.menu.name_error = f"Cannot start level: {error}"
                self.change_state(GameState.MENU)

    def setup_level(self) -> None:
        """Create the maze, actors, pellets and UI for this level.

        Returns:
            None.
        """
        if self.machine is None:
            return
        if len(self.config.levels) <= self.level:
            self.machine.change_state(GameState.VICTORY)
            return
        self.maze = Maze(
            self.config,
            self.drawer,
            self.level,
            self.screen.get_size(),
        )

        player_spawn = self.maze.grid_to_pixel(
            *self.maze.get_the_midlle_possitions()
        )

        self.player = Player(
            player_spawn[0],
            player_spawn[1],
            max(3, self.maze.CELL_SIZE * 2 // 5),
            self.maze.WI,
            self.maze.HE,
            lives=self.remaining_lives,
            speed=max(1, self.maze.CELL_SIZE // 5),
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

        superpac_positions = [
            self.maze.grid_to_pixel(x, y) for x, y in ghost_corners
        ]

        positions = self.maze.get_walkable_positions()

        for position in superpac_positions:
            if position in positions:
                positions.remove(position)

        if player_spawn in positions:
            positions.remove(player_spawn)

        self.pacgums = self.game.create_pacgums(positions)
        self.superpacgums = self.game.create_superpac(superpac_positions)
        for pellet in self.pacgums:
            pellet.radius = max(1, self.maze.CELL_SIZE // 10)
        for pellet in self.superpacgums:
            pellet.radius = max(2, self.maze.CELL_SIZE // 4)

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

        self.frame_clock.tick()
        self.change_state(GameState.PLAYING)

    def next_level(self) -> None:
        """Advance the level while retaining score and remaining lives.

        Returns:
            None.
        """
        self.remaining_lives = self.player.lives

        self.game.next_level()
        self.level += 1

        try:
            self.setup_level()
        except (ValueError, RuntimeError, IndexError, OSError) as error:
            if self.machine is not None:
                self.machine.menu.name_error = f"Cannot start level: {error}"
                self.change_state(GameState.MENU)

    def change_state(self, new_state: GameState) -> None:
        """Select the next screen.

        Args:
            new_state: Screen to activate next.

        Returns:
            None.
        """
        if self.machine is None:
            raise RuntimeError(
                "GameController needs set_machine(machine) first"
            )
        self.machine.change_state(new_state)

    def handle_keys(
        self,
        state: GameState,
        event: pygame.event.Event,
    ) -> None:
        """Handle a keyboard event for the current screen.

        Args:
            state: Screen currently handling input and rendering.
            event: Pygame keyboard event to process.

        Returns:
            None.
        """
        if event.type != pygame.KEYDOWN:
            return

        match state:
            case GameState.PLAYING:
                if self.game.paused:
                    return
                if event.key in (pygame.K_p, pygame.K_ESCAPE):
                    self.pause_selected = 0
                    self.game.toggle_pause(self.player)
                    self.change_state(GameState.PAUSED)
                elif self.cheats.handle_key(event.key):
                    self.next_level()

            case GameState.PAUSED:
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.pause_selected = 1 - self.pause_selected
                elif event.key in (pygame.K_p, pygame.K_ESCAPE) or (
                    event.key == pygame.K_RETURN and self.pause_selected == 0
                ):
                    duration = (
                        pygame.time.get_ticks() - self.game.manual_pause_start
                    ) / 1000
                    for ghost in self.ghosts.ghosts:
                        if ghost.mode == "eaten":
                            ghost.time_eaten += duration
                    self.game.toggle_pause(self.player)
                    self.change_state(GameState.PLAYING)
                elif event.key == pygame.K_RETURN:
                    self.change_state(GameState.MENU)

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
    ) -> None:
        """Handle queued input and render the current screen.

        Args:
            state: Screen currently handling input and rendering.
            keys: Keyboard events collected for this frame.

        Returns:
            None.
        """
        if not self.started or not self.machine:
            return

        delta_time = min(self.frame_clock.tick() / 1000, 0.05)
        if keys is not None:
            events = (
                [keys] if isinstance(keys, pygame.event.EventType) else keys
            )
            for event in events:
                self.handle_keys(state, event)
                if self.machine.state != state:
                    break

        # A transition (e.g. pause) must not update gameplay again.
        if state == GameState.PLAYING and self.machine.state == state:
            self.update_playing(delta_time)

        self.screen.fill((0, 0, 0))
        match state:
            case GameState.PLAYING:
                self.draw_playing()
            case GameState.PAUSED:
                self.draw_playing()
                self.game_ui.draw_paused(self.pause_selected)
            case GameState.GAME_OVER:
                self.draw_playing()
                self.game_ui.draw_game_over()
            case GameState.LEVEL_COMPLETE:
                self.draw_playing()
                self.game_ui.draw_level_complete()

    def update_playing(self, delta_time: float = 1 / 60) -> None:
        """Advance active gameplay and detect wins or losses.

        Args:
            delta_time: Elapsed active-frame time in seconds.

        Returns:
            None.
        """
        self.game.update_death(self.player, self.ghosts)

        if (
            not self.game.manual_pause
            and self.game.level_time_remaining() == 0
        ):
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

            self.ghosts.update_all(delta_time)

            if self.player.alive and self.game.level_complete(
                self.pacgums,
                self.superpacgums,
            ):
                self.change_state(GameState.LEVEL_COMPLETE)
                return

        if not self.player.alive:
            self.change_state(GameState.GAME_OVER)

    def draw_playing(self) -> None:
        """Render the maze, pellets, player and ghosts.

        Returns:
            None.
        """
        self.game_ui.menu_game()

        for pacgum in self.pacgums:
            pacgum.draw(self.drawer)

        for superpac in self.superpacgums:
            superpac.draw(self.drawer)

        self.player.draw(self.screen)
        self.ghosts.draw_all()
