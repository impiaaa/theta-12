import os, pygame, graphwrap
import math, physics
from pygame.locals import *

class gui(Object):
	def __init__(self):
		pygame.init()
		self.dirty_rects = []
		self.screen = pygame.display.set_mode((640, 480))
		pygame.display.set_caption("CODE Game Testing")
	
		self.background = pygame.Surface(self.screen.get_size())
		self.background = background.convert()
		self.background.fill((250, 250, 250))
	
		self.screen.blit(background, (0, 0))
		pygame.display.flip()
	
		self.artist = graphwrap.Artist(screen)

	def update(self):
		pygame.display.update(self.dirty_rects)
