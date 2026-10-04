import pygame


def draw_horizental_line(scren, h: int, w: int, stop: int, color):
    for x in range(w, stop):
        scren.set_at((x, h), color)


def draw_vertical_line(scren, h: int, w: int, stop: int, color):
    for x in range(h, stop):
        scren.set_at((w, x), color)


WHITE = (255, 255, 255)
pygame.init()
WI = 800
HE = 600
runing = True
screen = pygame.display.set_mode((WI, HE))
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        draw_vertical_line(screen, 10, 20, 100, WHITE)
        draw_horizental_line(screen, 60, 60, 500, WHITE)
    pygame.display.flip()
