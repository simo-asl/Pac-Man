"""Validate configuration and launch the Pac-Man application."""

import sys
import time

import pygame

from .game_controller import GameController
from .parsing import Parser
from .ui import Draw, Menu
from .ui.state_machine import StateMachine


WINDOW_SIZE = (960, 640)


def main() -> int:
    """Validate arguments, run the game loop and report failures.

    Returns:
        Zero on normal exit, or one for invalid usage or startup failure.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        return 1

    try:
        pygame.init()
        config = Parser(sys.argv[1]).parser()

        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Pac-Man")

        draw = Draw(screen)
        menu = Menu(draw)
        game = GameController(screen, config)

        machine = StateMachine(menu, game)

        menu.set_machine(machine)
        game.set_machine(machine)
        while machine.running:
            frame_start = time.monotonic()
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    machine.running = False

            if not machine.running:
                break

            machine.run_state(events)

            pygame.display.flip()
            delay = 1 / 60 - (time.monotonic() - frame_start)
            if delay > 0:
                time.sleep(delay)

        return 0
    except Exception as error:
        print(f"Pac-Man: {error}")
        return 1

    finally:
        pygame.quit()


if __name__ == "__main__":
    raise SystemExit(main())
