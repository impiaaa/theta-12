import sys, os, random, math
import pygame
from pygame.locals import *
import t12, physics, entities, graphwrap, level
import time

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
	seq = graphwrap.staticSequence(t12.imageLoader.getImage("global/sprites/Velociraptor2.png"))
	seq2 = graphwrap.staticSequence(pygame.transform.flip(t12.imageLoader.getImage("global/sprites/Velociraptor2.png"), 1, 0))
	an = graphwrap.AnimSprite()
	an.putSequence("left", seq)
	an.putSequence("right", seq2)
	an.runSequence("left")
	
	
	t12.current_level = level.tlevel
	t12.current_level.load()
	croom = t12.current_level.croom

	t12.player = entities.Actor((420.0, 100.0, 30.0, 20.0), an)
	t12.player.name = "player"
	t12.player.jumpheight = 250 # wikianswers says this number should be 72, but that is boring.
	t12.player.speed = 396 # 396 in/2s according to wikianswers

	t12.player.adjustGeomToImage()
	t12.player.stretchArt = False
	t12.player.geom.width = 20 # testing things

	croom.add(t12.player)
	

	firstframe = True
	last_time = 0
	seconds = 0
	ctime = 0

	while 1:
		ctime = time.time()
		seconds = ctime - last_time
		last_time = time.time()
		if firstframe:
			seconds = 0
			firstframe = False

		screen.blit(background, (0, 0))

		# process events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					t12.player.left()
					an.runSequence("left")
				elif event.key == pygame.K_RIGHT:
					t12.player.right()
					an.runSequence("right")
				elif event.key == pygame.K_UP:
					if t12.player.grounded:
						t12.player.jump()
				elif event.key == pygame.K_c:
					t12.player.geom.center = (200, 100)
					t12.player.velx, t12.player.vely = 0, 0
				elif event.key == pygame.K_m:
					manrise = 0
				elif event.key == pygame.K_w:
					t12.player.geom.y -= 100
				elif event.key == pygame.K_s:
					t12.player.geom.y += 100
				elif event.key == pygame.K_a:
					t12.player.velx = -100000
				elif event.key == pygame.K_d:
					t12.player.velx =  100000
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					t12.player.velx = 0


		# update movement/spawn things
		for e in croom.all:
			e.update(seconds)
			if len(e.spawn) > 0:
				for s in e.spawn:
					croom.add(s)
				e.spawn = []

				
		# detect collisions
		for a in croom.geometry:
			if a is t12.player: continue

			if a.intersects(t12.player):
				a.collision(t12.player)

		if not t12.player.grounded:
			t12.player.acy = t12.gravity
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
		for e in croom.art_back:
			e.updateArt(seconds)
			e.draw(artist)
		for e in croom.art_mid:
			e.updateArt(seconds)
			e.draw(artist)
		for e in croom.art_front:
			e.updateArt(seconds)
			e.draw(artist)
		for e in croom.art_over:
			e.updateArt(seconds)
			e.draw(artist)
		#t12.player.updateArt(seconds)
		#t12.player.draw(artist)

		pygame.display.update(last_drects)
		pygame.display.update(drects)
		move(drects, last_drects, True)

		clock.tick(60)


if __name__ == "__main__":
	main()
