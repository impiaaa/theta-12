import os, pygame
import math, physics, entities, graphwrap
from pygame.locals import *

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

def inrange(num, start, stop):
		return num >= start and num <= stop

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

	pygame.draw.line(screen, (250, 0, 0), (50, 80), (100, 20))

	pygame.display.flip()

	angle = 0
	length = 50
	origin = [screen.get_size()[0]/2.0, 30]

	rect = physics.RotRect(290, 290, 20, 20, 0)

	tri = physics.RotPoly((screen.get_size()[0]/2, 50), ((0, -30), (-50, 50), (50, 50)), 0)

	tri2 = physics.RotPoly((screen.get_size()[0]/2, 280), ((-50, -50), (50, -5), (60, -10), (70, 0), (60, 10), (50, 5), (-50, 50)), 0)

	steve = entities.Entity(tri2, None)

	drects = []
	last_drects = []

	jim = graphwrap.Artist(screen, screen.get_size(), drects)

	testp = physics.RotPoly((200, 200), ((-20, 3), (50, 3), (100, -320), (40, 10), (37, 29)), 0)

	greg = entities.Entity(testp, None)

	turnleft, turnright, forward = False, False, True

	while 1:
		clock.tick(60)


		screen.blit(background, (0, 0))

		# vector test
		p = physics.rotatedPointAbsolute(origin, (origin[0], origin[1] + length), angle)
		pygame.draw.line(screen, (250, 0, 0), origin, p, 2)

		a1 = physics.rotatedPointRelative(origin, p, p, (p[0], p[1]+10), math.radians(135))
		pygame.draw.line(screen, (0, 250, 0), p, a1, 2)

		a2 = physics.rotatedPointRelative(origin, p, p, (p[0], p[1]+10), math.radians(-135))
		pygame.draw.line(screen, (0, 0, 250), p, a2, 2)

		pr = graphwrap._findRect((origin, p, a1, a2))

		drects.append(pr)

		#triangle drawing
		trilines = tri.getLines()
		for l in trilines:
			pygame.draw.line(screen, (255, 0, 255), l[0], l[1], 2)

		# rectangle test
		rect.angle = angle

		if rect.intersects(tri) or rect.intersects(tri2):
			thick = 5
		else:
			thick = 1

		colors = ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255))
		rlines = rect.getLines()
		rc = 0
		for rl in rlines:
			pygame.draw.line(screen, colors[rc], rl[0], rl[1], thick)
			#pygame.draw.line(screen, (0, 0, 0), rl[0], (rect.centerx, rect.centery), thick)
			rc += 1
			if (rc >= len(colors)): rc = 0
		drects.append(graphwrap._findRect(rect.getPoints()))

		jim.color = (0, 0, 255)
		steve.draw(jim)
		jim.color = (255, 0, 0)
		jim.drawPolyPoints(steve.getMotionSmear(1))

		ainc = math.radians(1)
		events = pygame.event.get(pygame.KEYDOWN)
		for e in events:
			if e.key == pygame.K_LEFT: turnleft = True
			elif e.key == pygame.K_RIGHT: turnright = True
		events = pygame.event.get(pygame.KEYUP)
		for e in events:
			if e.key == pygame.K_LEFT: turnleft = False
			elif e.key == pygame.K_RIGHT: turnright = False
			elif e.key == pygame.K_SPACE: forward = not forward

		if turnleft:
			steve.geom.angle -= ainc
		if turnright:
			steve.geom.angle += ainc

		steverect = graphwrap._findRect(steve.geom.getPoints())
		#jim.drawRect((steverect[0], steverect[1]), (steverect[2], steverect[3]))


		"""
		# recalculate origin
		vel = physics.rotatedPointAbsolute((0, 0), (0, 2), angle)
		origin[0] += vel[0]
		origin[1] += vel[1]
		rect.moveCenterTo(origin[0], origin[1])

		# spin everything
		angle += math.radians(1)

		testp.angle = angle

		vel = physics.rotatedPointAbsolute((0, 0), (0, 0.5), tri.angle)
		tri.centerx += vel[0]
		tri.centery += vel[1]

		vel = physics.rotatedPointAbsolute((0, 0), (0, 0.5), tri2.angle)
		tri2.centerx += vel[0]
		tri2.centery += vel[1]
		"""

		if forward:
			steve.velx, steve.vely = physics.rotatedPointAbsolute((0, 0), (50, 0), steve.geom.angle)
		else:
			steve.velx, steve.vely = 0, 0
		steve.update(clock.get_time()/1000.)

		pygame.display.update(last_drects)
		pygame.display.update(drects)

		move(drects, last_drects, True)

		pygame.display.flip() # just for now

if __name__ == "__main__": main()
