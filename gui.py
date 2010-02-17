import os, pygame, graphwrap
import math, physics
from pygame.locals import *

def main():
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption("CODE Game Testing")

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	screen.blit(background, (0, 0))
	pygame.display.flip()

	clock = pygame.time.Clock()

	artist = graphwrap.Artist(screen)

	while 1:
		clock.tick(60)
		# calculate time passed here ...

		screen.blit(background, (0, 0))

		# iterate through all entities and update (then draw) them ...

		pygame.display.flip()

if __name__ == "__main__": main()
