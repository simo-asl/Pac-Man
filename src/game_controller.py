"""Coordinate gameplay, keyboard input and screen transitions."""

import time
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.ui.state_machine import StateMachine

from src.game import Game
from src.game.cheats import Cheats
from src.game.ghost_manger import GhostsManager
from src.game.player import Player
from src.game.pacgum import Pacgum, SuperPacgum
from src.maze import Maze
from src.parsing.parser import GameConfig
from src.ui import Draw
from src.ui.content import INSTRUCTIONS
from src.ui.game_ui import GameUi
from src.ui.state import GameState


UPDATE_INTERVAL = 1 / 60


class GameController:
    """Connect gameplay objects to menu and gameplay screens."""

    player: Player
    maze: Maze
    cheats: Cheats
    game_ui: GameUi
    ghosts: GhostsManager
    pacgums: list[Pacgum]
    superpacgums: list[SuperPacgum]

    def __init__(
        self,
        screen: pygame.Surface,
        config: GameConfig,
    ) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            screen: Surface used as the drawing target or game window.
            config: Validated game configuration.

        Returns:
            None.
        """
        self.screen = screen
        self.config = config
        self.drawer = Draw(screen)
        self.machine: StateMachine | None = None
        self.started = False
        self.pause_selected = 0
        self.pause_instructions = False
        self.last_update_time = time.monotonic()
        self.update_accumulator = 0.0

    def set_machine(self, machine: "StateMachine") -> None:
        """Attach the state machine used for screen transitions.

        Args:
            machine: State machine coordinating menu and gameplay screens.

        Returns:
            None.
        """
        self.machine = machine

    def start_game(self) -> None:
        """Reset score, lives and progression for a new game.

        Returns:
            None.
        """
        self.level = 0
        self.started = True

        self.game = Game(config=self.config)

        self.remaining_lives = self.config.lives

        self._setup_safely()

    def setup_level(self) -> None:
        """Create the current maze, actors, pellets and drawing cache.

        Returns:
            None.
        """
        if self.machine is None:
            return
        if self.level >= len(self.config.levels):
            self.machine.change_state(GameState.VICTORY)
            return
        self.maze = Maze(
            self.config,
            self.drawer,
            self.level,
            self.screen.get_size(),
        )

        center = self.maze.grid_to_pixel(
            self.maze.columns // 2, self.maze.rows // 2
        )
        # The generator's central 42 motif can contain blocked cells.
        player_spawn = min(
            self.maze.get_walkable_positions(),
            key=lambda point: (point[0] - center[0]) ** 2
            + (point[1] - center[1]) ** 2,
        )

        self.player = Player(
            player_spawn[0],
            player_spawn[1],
            max(2, self.maze.CELL_SIZE * 2 // 5),
            lives=self.remaining_lives,
        )
        self.game_ui = GameUi(self.drawer, self.player, self.game, self.maze)

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
        """Advance progression while retaining score and remaining lives.

        Returns:
            None.
        """
        self.remaining_lives = self.player.lives

        self.game.next_level()
        self.level += 1

        self._setup_safely()

    def _setup_safely(self) -> None:
        """Return to the menu with feedback if level creation fails.

        Returns:
            None.
        """
        try:
            self.setup_level()
        except Exception as error:
            self.started = False
            if self.machine is not None:
                self.machine.menu.error_message = (
                    f"Cannot start level: {error}"
                )
                self.change_state(GameState.MENU)

    def change_state(self, new_state: GameState) -> None:
        """Select the screen to process on the next frame.

        Args:
            new_state: Screen state to activate.

        Returns:
            None.

        Raises:
            RuntimeError: No state machine has been attached.
        """
        if self.machine is None:
            raise RuntimeError(
                "GameController needs set_machine(machine) first"
            )
        self.machine.change_state(new_state)
        self.last_update_time = time.monotonic()
        self.update_accumulator = 0.0

    def handle_keys(
        self,
        state: GameState,
        event: pygame.event.Event,
    ) -> None:
        """Apply keyboard events to the current screen state.

        Args:
            state: Screen state whose input or content is being processed.
            event: Pygame keyboard event to process.

        Returns:
            None.
        """
        if event.type != pygame.KEYDOWN or self.machine is None:
            return

        match state:
            case GameState.PLAYING:
                if event.key in (pygame.K_p, pygame.K_ESCAPE):
                    if not self.game.paused:
                        self.pause_selected = 0
                        self.pause_instructions = False
                        self.game.toggle_pause(self.player, self.ghosts)
                        self.change_state(GameState.PAUSED)
                elif self.cheats.handle_key(event.key):
                    self.next_level()

            case GameState.PAUSED:
                if self.pause_instructions:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE,
                                     pygame.K_p):
                        self.pause_instructions = False
                    return
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    step = -1 if event.key == pygame.K_UP else 1
                    self.pause_selected = (self.pause_selected + step) % 3
                elif event.key in (pygame.K_p, pygame.K_ESCAPE) or (
                    event.key == pygame.K_RETURN and self.pause_selected == 0
                ):
                    self.game.toggle_pause(self.player, self.ghosts)
                    self.change_state(GameState.PLAYING)
                elif event.key == pygame.K_RETURN:
                    if self.pause_selected == 1:
                        self.pause_instructions = True
                    else:
                        self.change_state(GameState.MENU)

            case GameState.GAME_OVER:
                if event.key == pygame.K_RETURN:
                    self.machine.menu.begin_name_input()

            case GameState.LEVEL_COMPLETE:
                if event.key == pygame.K_RETURN:
                    self.next_level()

    def run(
        self,
        state: GameState,
        keys: pygame.event.Event | list[pygame.event.Event] | None = None,
    ) -> None:
        """Handle input, run fixed gameplay updates, and draw one frame.

        Args:
            state: Screen state whose input or content is being processed.
            keys: Keyboard events collected for the current frame.

        Returns:
            None.
        """
        if not self.started or self.machine is None:
            return

        if keys is not None:
            events = (
                [keys] if isinstance(keys, pygame.event.EventType) else keys
            )
            for event in events:
                self.handle_keys(state, event)
                if self.machine.state != state:
                    return

        current_time = time.monotonic()
        elapsed_time = current_time - self.last_update_time
        self.last_update_time = current_time

        if state == GameState.PLAYING:
            self.update_accumulator += elapsed_time
            while self.update_accumulator >= UPDATE_INTERVAL:
                self.update_accumulator -= UPDATE_INTERVAL
                self.update_playing()
                if self.machine.state != state:
                    return
        else:
            self.update_accumulator = 0.0

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
        """Advance movement, collisions and gameplay transitions.

        Returns:
            None.
        """
        self.game.update_death(self.player, self.ghosts)

        if (not self.game.manual_pause
                and self.game.level_time_remaining() == 0):
            self.player.dead()

        if (not self.game.paused and not self.game.manual_pause
                and self.player.alive):
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
        """Draw the maze, live HUD, pellets, player and ghosts.

        Returns:
            None.
        """
        self.game_ui.draw_game()

        for pacgum in self.pacgums:
            pacgum.draw(self.drawer)

        for superpac in self.superpacgums:
            superpac.draw(self.drawer)

        self.player.draw(self.drawer)
        self.ghosts.draw_all()
        if self.game.paused and self.player.alive:
            self.game_ui.draw_panel('LIFE LOST', (
                f'LIVES LEFT: {self.player.lives}', 'GET READY TO CONTINUE',
            ))

    def draw_paused(self) -> None:
        """Show pause choices or instructions without updating gameplay.

        Returns:
            None.
        """
        self.draw_playing()
        if self.pause_instructions:
            self.game_ui.draw_panel('HOW TO PLAY', (
                *INSTRUCTIONS, 'ENTER / ESC BACK TO PAUSE',
            ))
        else:
            choices = tuple(
                ('> ' if index == self.pause_selected else '') + label
                for index, label in enumerate(
                    ('RESUME', 'INSTRUCTIONS', 'MAIN MENU')
                )
            )
            self.game_ui.draw_panel('PAUSED', (
                *choices, 'UP / DOWN SELECT   ENTER CONFIRM',
            ))

    def draw_game_over(self) -> None:
        """Show the final score and prompt for highscore entry.

        Returns:
            None.
        """
        self.draw_playing()
        reason = ('TIME RAN OUT' if self.game.level_time_remaining() == 0
                  else 'NO LIVES LEFT')
        self.game_ui.draw_panel('GAME OVER - YOU LOST', (
            reason, f'FINAL SCORE: {self.game.score}',
            'ENTER SAVE YOUR SCORE',
        ))

    def draw_level_complete(self) -> None:
        """Show the current score before advancing to the next level.

        Returns:
            None.
        """
        self.draw_playing()
        self.game_ui.draw_panel('LEVEL COMPLETE', (
            f'SCORE: {self.game.score}', 'ENTER NEXT LEVEL',
        ))
