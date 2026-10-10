from .draw import Draw


class Menu:
    def __init__(self, draw: Draw):
        self.draw = draw
        self.selected = 0

        self.options = [
            "START GAME",
            "HIGHSCORES",
            "INSTRUCTIONS",
            "EXIT",
        ]


    def move_selection(self,direction: int) -> None:
        self.selected = (self.selected + direction) % len(self.options)


    def write_screens(self):
