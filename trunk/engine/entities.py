import pygame
import graphwrap, math, t12
import math

def entity_named(name):
	""" Returns the game entity with the specified name. """
	for i in game_entities:
		if game_entities[i] == name:
			return game_entities[i]

class Entity:
	def __init__(self, geom, anim):
		""" geom should be a rectangle or a tuple in rectangle format: (x, y, w, h) or pygame.rect.Rect
			anim should be an AnimSprite (see graphwrap.py) or None or -1. If it is None, a simple
			bounding rectangle will be shown. If it is -1, it will be entirely invisible. 
			All subclasses MUST call this constructer or things will BREAK. """

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
		self.name = None # may be used for identification. Only used for "player", for now.
		self.spawn = [] # this is a list of entities that should be spawned by the main loop.
						  # this allows entities to create other entities and be multi-part.
		self.attributes = [] # this contains a list of the names of what lists this should go in (geometry, activators, etc)
							 # see level.Room.add()
		self.id = t12.ent_currentid
		t12.game_entities[self.id] = self
		t12.ent_currentid += 1
		self.stretchArt = True # stretch the art to fill the geometry, or center the art if the sizes aren't the same?
		
	def adjustGeomToImage(self):
		if self.anim == None or self.anim == -1: return
		m = self.anim.getImage()
		if m == None: return
		self.geom.width, self.geom.height = m.get_size()
		self.last.size = self.geom.size

	def draw(self, artist):
		if self.anim is None:
			artist.drawRect(self.geom.topleft, self.geom.size)
		elif self.anim == -1:
			return
		else:
			m = self.anim.getImage()
			if self.stretchArt:
				artist.drawImage(m, self.geom.topleft, self.geom.size)
			else:
				artist.drawImage(m, (self.geom.centerx - m.get_width()/2, self.geom.centery - m.get_height()/2))

		artist.addDirtyRect(self.geom)
		artist.addDirtyRect(self.last)

	def updateArt(self, time):
		if self.anim is not None and self.anim != -1:
			self.anim.update(time)

	def updatelast(self):
		self.last.left = self.geom.left
		self.last.top = self.geom.top

	def update(self, time):
		self.updatelast()

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
		self.attributes.append("geometry")

	def intersects(self, other_entity):
		if Entity.intersects(self, other_entity):
			return True
		if self.geom.top - other_entity.geom.bottom <= 3 and (self.geom.right > other_entity.geom.right > self.geom.left
				or self.geom.right > other_entity.geom.left > self.geom.left):
			return True
		return False

	def collision(self, other):
		if other.vely >= 0:
			other.vely = self.vely
			if other.acy > 0:
				other.acy = 0 # stop accelerating downwards...
			other.geom.bottom = self.geom.top
		other.grounded = True

class Block(FloorBlock):
	def __init__(self, geom, anim):
		FloorBlock.__init__(self, geom, anim)
		self.sticky = False

	def update(self, time):
		Entity.update(self, time)

	def intersects(self, other_entity):
		if Entity.intersects(self, other_entity):
			return True
		if self.geom.top - other_entity.geom.bottom <= 3 and (self.geom.right > other_entity.geom.right > self.geom.left
				or self.geom.right > other_entity.geom.left > self.geom.left) and other_entity.geom.top < self.geom.bottom:
			return True
		return False

	def collision(self, other):
		if other.geom.bottom < self.geom.top:
			other.grounded = True
			if self.sticky or other.vely >= 0 and self.vely < other.vely:
				other.vely = self.vely
				other.geom.bottom = self.geom.top
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
			if self.sticky or other.vely >= 0 and self.vely < other.vely:
				other.vely, other.acy = self.vely, 0
		elif wleft and not left:
			other.geom.right = self.geom.left
			other.velx = self.velx
		elif wright and not right:
			other.geom.left = self.geom.right
			other.velx = self.velx
		elif wbelow and not below or not (abs(other.geom.bottom - self.geom.top) < abs(self.geom.bottom - other.geom.top)):
			other.geom.top = self.geom.bottom
			other.vely = self.vely
			other.updatelast()
		else:
			if not above:
				other.geom.bottom = self.geom.top
				other.grounded = True
				if other.vely > 0:
					other.vely, other.acy = self.vely, 0

class TriggerEntity(Entity):
	def __init__(self, geom, anim):
		""" This entity has one added method: trigger(par=None). 
			It simply iterates through all the functions in the list TriggerEntity.reactors and
			calls them, along with the optional "par" variable. It is up to the subclasses of
			this function to actually call the trigger() method and to decide whether to actually
			use the "par" argument. """
		Entity.__init__(self, geom, anim)
		self.reactors = [] # list of functions that are called when this is triggered

	def trigger(self, par=None):
		for r in self.reactors:
			r(par)

class MotionTrigger(TriggerEntity):
	def __init__(self, geom, anim):
		TriggerEntity.__init__(self, geom, anim)

	def collision(self, other):
		if other.name == "player":
			TriggerEntity.trigger(self)

class Elevator(Entity):
	def __init__(self, geom, targety, duration):
		""" Paramaters: geometry (rectangle),  targety (where the elevator will go), and duration (the 
			time in seconds it will take to get there) """
		Entity.__init__(self, geom, -1)
		self.floor = Block((self.geom.left, self.geom.bottom-20, self.geom.width, 20), None)
		self.roof = Block((self.geom.left, self.geom.top, self.geom.width, 20), None)
		self.floor.sticky = True
		self.roof.sticky = True
		self.spawn.append(self.floor)
		self.spawn.append(self.roof)
		self.y1 = self.geom.top
		self.y2 = targety
		self.state = 0 # 0 = stopped, 1 = go towards position 1, -1 = go towards position 0
		self.duration = duration
		if self.y2 - self.y1 > 0:
			self.dir = 1
		else:
			self.dir = -1
		self.speed = abs( (self.y2 - self.y1) / duration)
		self.attributes.append("geometry") # this is in so it can move automatically when the player steps on it
		self.playerref = None			   # this will be taken out because we'll probably want the elevator to be
										   # activated by external means a lot of the time.


	def intersects(self, other_entity):
		if Entity.intersects(self, other_entity):
			return True
		if self.geom.top - other_entity.geom.bottom <= 3 and (self.geom.right > other_entity.geom.right > self.geom.left
				or self.geom.right > other_entity.geom.left > self.geom.left) and self.geom.bottom > other_entity.geom.top:
			return True
		return False

	def collision(self, other):
		if other.name == "player" and self.state == 0 and self.playerref == None:
			if self.geom.y == self.y1:
				self.state = 1
			else:
				self.state = -1
			
			self.playerref = other

	def update(self, time):
		Entity.update(self, time)
		if self.state == 0:
			self.vely = 0
		elif self.state == 1:
			if self.dir == 1 and self.geom.y < self.y2:
				self.vely = self.speed
			elif self.dir == -1 and self.geom.y > self.y2:
				self.vely = -self.speed
			else:
				self.vely = 0
				self.geom.y = self.y2
				self.state = 0
		elif self.state == -1:
			if self.dir == 1 and self.geom.y > self.y1:
				self.vely = -self.speed
			elif self.dir == -1 and self.geom.y < self.y1:
				self.vely = self.speed
			else:
				self.vely = 0
				self.geom.y = self.y1
				self.state = 0

		self.floor.updatelast()
		self.roof.updatelast()
		self.floor.geom.top = self.geom.bottom - 20
		self.roof.geom.top = self.geom.top

		if self.playerref != None:
			if not self.intersects(self.playerref):
				self.playerref = None

class Actor(Entity):
	def __init__(self, geom, anim, feet=None):
		""" geom and anim are as normal, and the "feet" paramater should
			be a tuple for the startx and endx of the feet on the sprite.
			If it is set to None, the feet are assumed to be the bounds of
			the geometry. """
		Entity.__init__(self, geom, anim)

		# the self.specialFeet boolean keeps track of whether the feet value
		# should change if the geometry is changed.
		if feet == None:
			self.specialFeet = False
			self.feet = (0, self.geom.width)
		else:
			self.specialFeet = True
			self.feet = feet

		self.feetbox = pygame.rect.Rect((0, 0, 1, 1))

		self.health = 10 # arbitrary default
		self.jumpheight = 50 # arbitrary
		self.speed = 100 # horizontal movement speed. may be replaced by acceleration at some point.

		self.update(0) # for the feetbox

	def update(self, time):
		Entity.update(self, time)
		if not self.specialFeet:
			self.feetbox.width = self.geom.width
		else:
			self.feetbox.width = self.feet[1] - self.feet[0]
		self.feetbox.left = self.geom.left + self.feet[0]
		self.feetbox.top, self.feetbox.height = self.geom.bottom - 2, 2

	def jump(self):
		self.vely = -math.sqrt(t12.gravity * self.jumpheight * 2)
		self.geom.top -= 3

	def left(self):
		self.velx = -self.speed

	def right(self):
		self.velx = self.speed

	def stopX(self):
		self.velx = 0

	def decelerate(self, x, y):
		""" Decelerates in the given x/y directions. It will NOT
			accelerate in the other direction if the result is less
			than zero. It will just stop. """
		x, y = abs(x), abs(y)

		if abs(self.velx) - x < 0:
			self.velx = 0
		elif self.velx != 0:
			sign = abs(self.velx)/self.velx
			self.velx -= sign * x

		if abs(self.vely) - y < 0:
			self.vely = 0
		elif self.vely != 0:
			sign = abs(self.vely)/self.vely
			self.vely -= sign * y
