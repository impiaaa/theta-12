import sys, os, random, math
import pygame
from pygame.locals import *
import physics, entities, graphwrap

# helper functions
def empty(stuff):
	""" Removes every item from list 'stuff' """
	for i in range(len(stuff)):
		stuff.pop()

def copy(list1, list2):
	for i in range(len(list1)):
		list2.append(list1[i])

def move(list1, list2, clearFirst=False):
	if clearFirst:
		empty(list2)
	for i in range(len(list1)):
		list2.append(list1.pop())

# testing only
def randomEntity():
	points = ((-10, -10), (-5, -20), (0, -10), (5, 7), (30, 20), (50, -30))
	geom = physics.RotPoly((320, 240), points, random.random()*math.radians(360))
	e = entities.Entity(geom, None)
	speed = random.random() * 100
	e.velx, e.vely = math.cos(e.geom.angle)*speed, math.sin(e.geom.angle)*speed
	print str(e.geom.getPoints())
	return e

things = []

def main():
	pygame.init()
	drects, last_drects = [], []
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption("Theta 12")
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	
	screen.blit(background, (0, 0))
	pygame.display.flip()
		
	artist = graphwrap.Artist(screen, screen.get_size(), drects)
	

	clock = pygame.time.Clock()
	
	while 1:

		screen.blit(background, (0, 0))

		# process events
		# ...

		for e in pygame.event.get(pygame.KEYDOWN):
			if e.key == pygame.K_SPACE:
				things.append(randomEntity())

		# detect collisions
		for a in things:
			for b in things:
				if a is b: continue
				if a.smearsIntersect(b, 0.016):
					a.move_allowed = False
					b.move_allowed = False

		for e in things:
			if not e.move_allowed:
				e.geom.angle += math.radians(1)
			e.update(0.016)
			e.updateArt(0.016)
			e.draw(artist)
			e.move_allowed = True # reset flag for next iteration
				

		# draw everything

		pygame.display.update(last_drects)
		pygame.display.update(drects)
		move(drects, last_drects, True)

		clock.tick(60)


if __name__ == "__main__":
	main()
