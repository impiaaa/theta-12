import sys, os, random, math
import pygame
from pygame.locals import *
import physics, entities, graphwrap, level

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

current_level = level.tlevel
player = entities.Entity(physics.RotRect(420, 100, 30, 20, 0), None)

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

		croom = current_level.croom

		# process events
		# ...

		player.vely = 200


		# detect collisions
		for a in croom.geometry:
			if a.smearsIntersect(player, 0.016):
				player.vely = -50

		for e in croom.all:
			e.update(0.016)
			e.updateArt(0.016)
			e.draw(artist)
			e.move_allowed = True # reset flag for next iteration
			artist.drawPolyPoints(e.getMotionSmear(0.016))
		player.update(0.016)
		player.updateArt(0.016)
		player.draw(artist)

		artist.drawPolyPoints(player.getMotionSmear(0.016))
				

		# draw everything

		pygame.display.update(last_drects)
		pygame.display.update(drects)
		move(drects, last_drects, True)

		clock.tick(60)


if __name__ == "__main__":
	main()
