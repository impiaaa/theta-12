import pygame
import graphwrap, math

class Entity:
	def __init__(self, geom, anim):
		self.geom = geom # pygame.rect.Rect or tuple
		if not isinstance(geom, pygame.rect.Rect):
			self.geom = pygame.rect.Rect(geom) # convert to pygame.rect.Rect
		self.anim = anim # AnimSprite
		self.velx, self.vely = 0, 0
		self.move_allowed = True # flag set to false if collision is imminent
		self.acx, self.acy = 0, 0 # constant acceleration (use acy for gravity)
		self.grounded = False # used by things that can fall

		self._incx, self._incy = 0, 0 # necessary because pygame.rect.Rect uses integers =/
		
	def draw(self, artist):
		if self.anim is None:
			artist.drawRect(self.geom.topleft, self.geom.size) # this is throwing an exception in graphwrap.Artist for some reason

		artist.addDirtyRect(self.geom)

	def updateArt(self, time):
		if self.anim is not None:
			self.anim.update(time)

	def update(self, time):
		self.velx += self.acx * time

		self.vely += self.acy * time
		self._incx += self.velx * time
		self._incy += self.vely * time

		if abs(self._incx) > 0:
			val = int(self._incx)
			self.geom.centerx += val
			self._incx -= val
		if abs(self._incy) > 0:
			val = int(self._incy)
			self.geom.centery += val
			self._incy -= val

		self.grounded = False # reset grounded

	def intersects(self, other_entity):
		return self.geom.colliderect(other_entity.geom)

	def collision(self, other):
		""" This method is called when this entity hits another entity.
			Subclasses are expected to override it to make it do something useful. """
		return None

class FloorBlock(Entity):
	def __init__(self, geom, anim):
		Entity.__init__(self, geom, anim)

	def collision(self, other):
		if other.vely >= 0:
			other.vely = 0
			if other.acy > 0:
				other.acy = 0 # stop accelerating downwards...
		if other.geom.bottom > self.geom.top:
			other.geom.bottom = self.geom.top
		other.grounded = True
