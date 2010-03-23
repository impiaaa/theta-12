import sys, os, random, math
import pygame
from pygame.locals import *
import t12, physics, entities, graphwrap, level

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


	#test code for loading velociraptor anim
	seq = graphwrap.AnimSequence((t12.imageLoader.getImage("global/sprites/Velociraptor2.png"),), 1000)
	an = graphwrap.AnimSprite()
	an.runSequence(seq)
	
	t12.current_level = level.tlevel
	t12.player = entities.Entity((420.0, 100.0, 30.0, 20.0), an)
	t12.player.name = "player"

	t12.player.adjustGeomToImage()

	while 1:

		screen.blit(background, (0, 0))

		croom = t12.current_level.croom

		# process events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					t12.player.velx = -200
				elif event.key == pygame.K_RIGHT:
					t12.player.velx = 200
				elif event.key == pygame.K_UP:
					if t12.player.grounded:
						t12.player.vely = -600
						t12.player.geom.top -= 2
				elif event.key == pygame.K_c:
					t12.player.geom.center = (200, 100)
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
					t12.player.velx = 0


		# update movement/spawn things
		for e in croom.all:
			e.update(0.016)
			if len(e.spawn) > 0:
				for s in e.spawn:
					croom.add(s)
				e.spawn = []

		t12.player.update(0.016)

				
		# detect collisions
		for a in croom.geometry:
			if a is t12.player: continue

			""" debug code not wanted for now
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
			"""

			if a.intersects(t12.player):
				a.collision(t12.player)

		if not t12.player.grounded:
			t12.player.acy = 386 # 9.8 m/s, according to the art team's scale
		else:
			t12.player.acy = 0

		wid, hig = screen.get_size()
		wd = t12.player.geom.centerx - wid/2
		hd = 0
		if t12.player.geom.top < 0:
			hd = t12.player.geom.top - 50
		elif t12.player.geom.bottom > hig:
			hd = t12.player.geom.bottom - hig + 50 

		xinc = abs(artist.offsetx+wd)/5
		yinc = abs(artist.offsety+hd)/5

		if artist.offsetx < -wd:
			artist.offsetx += xinc
		elif artist.offsetx > -wd:
			artist.offsetx -= xinc

		if artist.offsety < -hd:
			artist.offsety += yinc
		elif artist.offsety > -hd:
			artist.offsety -= yinc

		# draw everything
		for e in croom.all:
			e.updateArt(0.016)
			e.draw(artist)
		t12.player.updateArt(0.016)
		t12.player.draw(artist)

		pygame.display.update(last_drects)
		pygame.display.update(drects)
		move(drects, last_drects, True)

		clock.tick(60)


if __name__ == "__main__":
	main()
