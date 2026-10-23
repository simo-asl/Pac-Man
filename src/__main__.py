import sys

import pygame

from .game_controller import GameController
from .parsing import Parser


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src <config_file>")
        return

    pygame.init()

    try:
        config = Parser(sys.argv[1]).parser()

        screen = pygame.display.set_mode((1800, 1200))
        pygame.display.set_caption("Pac-Man")

        controller = GameController(screen, config)
        clock = pygame.time.Clock()

        while controller.running:
            for event in pygame.event.get():
                controller.handle_event(event)

            controller.update()
            controller.draw()

            pygame.display.flip()
            clock.tick(60)

    except Exception as error:
        print(f"Error: {error}")

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
