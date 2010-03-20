import pygame
import graphwrap, math

class Entity:
	def __init__(self, geom, anim):
		self.geom = geom # pygame.rect.Rect or tuple
		if not isinstance(geom, pygame.rect.Rect):
			self.geom = pygame.rect.Rect(geom) # convert to pygame.rect.Rect
		self.last = pygame.rect.Rect((self.geom.left, self.geom.top, self.geom.width, self.geom.height))
		self.anim = anim # AnimSprite
		self.velx, self.vely = 0, 0
		self.move_allowed = True # flag set to false if collision is imminent
		self.acx, self.acy = 0, 0 # constant acceleration (use acy for gravity)
		self.grounded = False # used by things that can fall
		self.sticking = False # true if it is sitting on a "sticky" surface
		self._incx, self._incy = 0, 0 # necessary because pygame.rect.Rect uses integers =/
		
	def draw(self, artist):
		if self.anim is None:
			artist.drawRect(self.geom.topleft, self.geom.size) # this is throwing an exception in graphwrap.Artist for some reason

		artist.addDirtyRect(self.geom)
		artist.addDirtyRect(self.last)

	def updateArt(self, time):
		if self.anim is not None:
			self.anim.update(time)

	def update(self, time):
		self.last.left = self.geom.left
		self.last.top = self.geom.top

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
		if self.geom.top - other_entity.geom.bottom <= 3 and (self.geom.right > other_entity.geom.right > self.geom.left
				or self.geom.right > other_entity.geom.left > self.geom.left):
			return True
		return False

	def collision(self, other):
		if other.vely >= 0:
			other.vely = 0
			if other.acy > 0:
				other.acy = 0 # stop accelerating downwards...
			other.geom.bottom = self.geom.top
		other.grounded = True

class Block(FloorBlock):
	def __init__(self, geom, anim):
		FloorBlock.__init__(self, geom, anim)
		self.sticky = False # if set to true, things sitting on this
							# will descend at the same rate as this
		self.sitters = [] # list of the things sitting on me

	def update(self, time):
		Entity.update(self, time)

		if self.sticky:
			for sitter in self.sitters:
				if (sitter.vely < 0 or sitter.geom.right < self.geom.left
					or sitter.geom.left > self.geom.right or (sitter.geom.bottom < self.geom.top and sitter.grounded)):
					self.sitters.remove(sitter)
					sitter.sticking = False
				elif sitter.geom.bottom < self.geom.top and not sitter.grounded:
					sitter.geom.bottom = self.geom.top

	def intersects(self, other_entity):
		if Entity.intersects(self, other_entity):
			return True
		if self.geom.top - other_entity.geom.bottom <= 3 and (self.geom.right > other_entity.geom.right > self.geom.left
				or self.geom.right > other_entity.geom.left > self.geom.left) and other_entity.geom.top < self.geom.bottom:
			return True
		return False

	def collision(self, other):
		if other.geom.bottom < self.geom.top:
			other.geom.bottom = self.geom.top
			other.grounded = True
			return

		above = other.geom.bottom < self.geom.top
		below = other.geom.top > self.geom.bottom
		left = other.geom.right < self.geom.left
		right = other.geom.left > self.geom.right

		wabove = other.last.bottom <= self.last.top
		wbelow = other.last.top >= self.last.bottom
		wleft = other.last.right <= self.last.left
		wright = other.last.left >= self.last.right

		if wabove:
			other.geom.bottom = self.geom.top
			other.grounded = True
			other.vely, other.acy = 0, 0
			if self.sticky and not other.sticking:
				self.sitters.append(other)
				other.sticking = True
		elif wleft and not left:
			other.geom.right = self.geom.left
			other.velx = 0
		elif wright and not right:
			other.geom.left = self.geom.right
			other.velx = 0
		elif wbelow and not below:
			other.geom.top = self.geom.bottom
			other.vely = 0
		else:
			if not above:
				other.geom.bottom = self.geom.top
				other.grounded = True
				other.vely, other.acy = 0, 0
				if self.sticky and not other.sticking:
					self.sitters.append(other)
					other.sticking = True
