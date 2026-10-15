import pygame

# all initialized vars are temp for the beta version
# so i'll update them once u parse the fkn conf file
# read the comments u will find them funny and hopefully helpful


class Player:
    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        s_width: int = 900,
        s_height: int = 900,
        speed: int = 7,
    ):

        self.x: int = x
        self.y: int = y
        self.lives: int = 3
        self.radius: int = radius
        self.s_width: int = s_width
        self.s_height: int = s_height
        self.speed: int = speed
        self.alive: bool = True
        self.powered_up: bool = False
        self.power_start_time: int = 0
        self.power_duration: int = 10000
        self.target_x: int = x
        self.target_y: int = y
        self.color: tuple[int, int, int] = (255, 255, 0)
        self.invincible: bool = False
        # TODO ADD IT THIS FOR GHOSTS |
        self.direction: int = 2

    def dead(self) -> None:
        self.alive = False

    def lose_life(self) -> None:

        if self.lives > 0:
            self.lives -= 1
        if self.lives <= 0:
            self.dead()

    def add_life(self) -> None:
        self.lives += 1

    def activate_power(self) -> None:
        self.powered_up = True
        self.power_start_time = pygame.time.get_ticks()

    def toggle_invincibility(self) -> None:
        self.invincible = not self.invincible

    def update_power(self) -> None:
        if self.powered_up:
            if pygame.time.get_ticks() - self.power_start_time >= self.power_duration:
                self.powered_up = False

    def move(self, maze) -> None:
        keys = pygame.key.get_pressed()

        if self.x == self.target_x and self.y == self.target_y:
            cell_x = self.x // maze.CELL_SIZE
            cell_y = self.y // maze.CELL_SIZE

            if keys[pygame.K_LEFT] and maze.can_move(cell_x, cell_y, 8):
                self.target_x -= maze.CELL_SIZE
                self.direction = 8

            elif keys[pygame.K_RIGHT] and maze.can_move(cell_x, cell_y, 2):
                self.target_x += maze.CELL_SIZE
                self.direction = 2

            elif keys[pygame.K_UP] and maze.can_move(cell_x, cell_y, 1):
                self.target_y -= maze.CELL_SIZE
                self.direction = 1

            elif keys[pygame.K_DOWN] and maze.can_move(cell_x, cell_y, 4):
                self.target_y += maze.CELL_SIZE
                self.direction = 4

        if self.x < self.target_x:
            self.x += min(self.speed, self.target_x - self.x)
        elif self.x > self.target_x:
            self.x -= min(self.speed, self.x - self.target_x)
        elif self.y < self.target_y:
            self.y += min(self.speed, self.target_y - self.y)
        elif self.y > self.target_y:
            self.y -= min(self.speed, self.y - self.target_y)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
