import pygame


pygame.init()
surface = pygame.Surface((500, 300))
screen = pygame.display.set_mode((800, 600))
screen.blit(surface, (0, 0))
pygame.display.flip()
