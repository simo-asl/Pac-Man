from mazegenerator import MazeGenerator


class Draw:
    def __init__(self, scren, cell_size: int = 20):
        self.CELL_SIZE = cell_size
        self.scren = scren

    def draw_horizontal_line(
        self, start_x: int, y: int, end_x: int, color, thickness=1
    ):
        for offset in range(thickness):
            for x in range(start_x, end_x):
                self.scren.set_at((x, y + offset), color)

    def draw_vertical_line(self, x: int, start_y: int, end_y: int, color, thickness=1):
        for offset in range(thickness):
            for y in range(start_y, end_y):
                self.scren.set_at((x + offset, y), color)

    def draw_maze(self, cell_x, cell_y, cell, color, thickness=1):
        x = cell_x * self.CELL_SIZE
        y = cell_y * self.CELL_SIZE
        x2 = x + self.CELL_SIZE
        y2 = y + self.CELL_SIZE

        if cell & 1:
            self.draw_horizontal_line(x, y, x2, color, thickness)
        if cell & 2:
            self.draw_vertical_line(x2, y, y2, color, thickness)
        if cell & 4:
            self.draw_horizontal_line(x, y2, x2, color, thickness)
        if cell & 8:
            self.draw_vertical_line(x, y, y2, color, thickness)
