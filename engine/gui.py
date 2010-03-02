import os, pygame, graphwrap
import math, physics
from pygame.locals import *

started = False


pygame.init()
dirty_rects = []
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Theta 12")
background = pygame.Surface(self.screen.get_size())s
background = background.convert()
background.fill((250, 250, 250))

screen.blit(background, (0, 0))
pygame.display.flip()
	
artist = graphwrap.Artist(screen)

def update(self):
	pygame.display.update(self.dirty_rects)
