"""Launch the game in a fixed-size desktop window."""

import sys

import pygame

from .game_controller import GameController
from .parsing import Parser
from .ui import Draw, Menu
from .ui.state_machine import StateMachine


CANVAS_SIZE = (2100, 1800)


def main() -> int:
    """Validate configuration, run the game, and report errors cleanly.

    Returns:
        int: Zero on success, or one after a reported application error.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        return 1
    try:
        config = Parser(sys.argv[1]).parser()
        pygame.init()
        canvas = pygame.display.set_mode(CANVAS_SIZE)
        pygame.display.set_caption("Pac-Man")
        clock = pygame.time.Clock()
        menu = Menu(Draw(canvas))
        game = GameController(canvas, config)
        machine = StateMachine(menu, game)
        menu.set_machine(machine)
        game.set_machine(machine)
        while machine.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    machine.running = False
            if not machine.running:
                break
            machine.run_state(events)
            pygame.display.flip()
            clock.tick(60)
        return 0
    except Exception as error:
        print(f"Pac-Man: {error}")
        return 1
    finally:
        pygame.quit()


if __name__ == "__main__":
    raise SystemExit(main())
