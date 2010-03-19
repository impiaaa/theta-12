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

	def intersects(self, other_entity):
		if Entity.intersects(self, other_entity):
			return True
		if self.geom.top - other_entity.geom.bottom <= 3 and (other_entity.geom.right > self.geom.right > other_entity.geom.left
				or other_entity.geom.right > self.geom.left > other_entity.geom.left) and other_entity.geom.top < self.geom.bottom:
			return True
		return False

	def collision(self, other):
		if other.vely >= 0:
			other.vely = 0
			if other.acy > 0:
				other.acy = 0 # stop accelerating downwards...
		if other.geom.bottom > self.geom.top:
			other.geom.bottom = self.geom.top
		other.grounded = True

class Block(FloorBlock):
	def __init(self, geom, anim):
		FloorBlock.__init__(self, geom, anim)

	def collision(self, other):
		above = other.geom.bottom <= self.geom.top + 3
		left = other.geom.right <= self.geom.left + 3
		right = other.geom.left >= self.geom.right - 3
		below = other.geom.top >= self.geom.centery and other.vely < 0 and other.geom.bottom > self.geom.bottom and (
				other.geom.right > self.geom.left or other.geom.left < self.geom.right)


		if above:
			other.geom.bottom = self.geom.top
			other.grounded = True
			if other.vely >= 0:
				other.vely = 0
				other.acy = 0
		elif left:
			other.geom.right = self.geom.left
			if other.velx > 0: other.velx = 0
		elif right:
			other.geom.left = self.geom.right
			if other.velx < 0: other.velx = 0
		if below:
			other.geom.top = self.geom.bottom
			if other.vely < 0:
				other.vely = 0

