import pygame
import graphwrap, math

class Entity:
	def __init__(self, geom, anim):
		self.geom = geom # pygame.rect.Rect or tuple
		if geom.__class__ != pygame.rect.Rect:
			self.geom = pygame.rect.Rect(geom) # convert to pygame.rect.Rect
		self.anim = anim # AnimSprite
		self.velx, self.vely = 0, 0
		self.move_allowed = True # flag set to false if collision is imminent
		
	def draw(self, artist):
		if self.anim is None:
			artist.drawRect(self.geom.topleft, self.geom.size) # this is throwing an exception in graphwrap.Artist for some reason

		artist.addDirtyRect(self.geom)

	def updateArt(self, time):
		if self.anim is not None:
			self.anim.update(time)

	def update(self, time):
		self.geom.centerx += self.velx * time
		self.geom.centery += self.vely * time

	def intersects(self, other_entity):
		return self.geom.colliderect(other_entity.geom)
		

