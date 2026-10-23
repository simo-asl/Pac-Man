import sys

import pygame

from .game_controller import GameController
from .parsing import Parser
from .ui import Draw, Menu
from .ui.state_machine import StateMachine


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src <config_file>")
        return

    pygame.init()

    try:
        config = Parser(sys.argv[1]).parser()

        screen = pygame.display.set_mode((1800, 1200))
        pygame.display.set_caption("Pac-Man")

        clock = pygame.time.Clock()

        draw = Draw(screen)
        menu = Menu(draw)
        game = GameController(screen, config)

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

        pygame.quit()
    except Exception as error:
        print(f"Error: {error}")

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
