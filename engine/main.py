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
player = entities.Entity((420.0, 100.0, 30.0, 20.0), None)


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

	manrise = 0 # <-- debug, this code should be removed eventually....

	while 1:

		screen.blit(background, (0, 0))

		croom = current_level.croom

		# process events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.velx = -200
				elif event.key == pygame.K_RIGHT:
					player.velx = 200
				elif event.key == pygame.K_UP:
					if player.grounded:
						player.vely = -300
						player.geom.top -= 2
				elif event.key == pygame.K_c:
					player.geom.center = (200, 100)
				elif event.key == pygame.K_m:
					manrise = 0
				elif event.key == pygame.K_w:
					manrise = -1
					for a in croom.geometry:
						if a.geom.height < 50:
							a.vely = -500
				elif event.key == pygame.K_s:
					manrise = 1
					for a in croom.geometry:
						if a.geom.height < 50:
							a.vely = 500
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					player.velx = 0



		# update movement
		for e in croom.all:
			e.update(0.016)

		player.update(0.016)

				
		# detect collisions
		for a in croom.geometry:
			if a is player: continue

			if a.geom.height < 50:
				if a.vely < 0 and a.geom.top < 100:
					if manrise == 0:
						a.vely = 100
					else:
						a.vely = 0
				elif a.vely > 0 and a.geom.top > 380:
					if manrise == 0:
						a.vely = -100
					else:
						a.vely = 0
				elif a.vely == 0 and not manrise:
					a.vely = -100

			if a.intersects(player):
				a.collision(player)

			#if a.geom.top - player.geom.bottom <= 3:
			#	player.grounded = True

		if not player.grounded:
			player.acy = 192 # 9.8 m/s, according to the art team's scale
		else:
			player.acy = 0

		wid, hig = screen.get_size()
		wd = player.geom.centerx - wid/2
		hd = 0
		if player.geom.top < 0:
			hd = player.geom.top
		elif player.geom.bottom > hig:
			hd = player.geom.bottom - hig 

		for a in croom.all:
			a.geom.x -= wd
			a.geom.y -= hd
		player.geom.centerx = wid/2
		player.geom.centery -= hd

		# draw everything
		for e in croom.all:
			e.updateArt(0.016)
			e.draw(artist)
		player.updateArt(0.016)
		player.draw(artist)

		pygame.display.update(last_drects)
		pygame.display.update(drects)
		move(drects, last_drects, True)

		clock.tick(60)


if __name__ == "__main__":
	main()
