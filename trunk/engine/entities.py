import pygame
import graphwrap, math, t12, physics
import math

def entity_named(name):
	""" Returns the game entity with the specified name. """
	for i in game_entities:
		if game_entities[i] == name:
			return game_entities[i]

class Weapon:
	""" The Weapon is NOT an entity. """
	def __init__(self):
		self.name = "Untitled Weapon"
		self.icon = None
		self.graphic = None

	def use(self, by, startpoint, tar_polar):
		""" This doesn't do anything in the base Weapon class.
		    	Subclasses should override it. 'by' should be whatever entity
			fired the weapon. tar_ent is the target entity, tar_point is the
			target point, tar_polar is as trajectory (angle and magnitude). startpoint
			is a tuple, and it's purpose should be self-explanatory. """
		return None

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
		if self.anim != None and self.anim != -1:
			self.anim = self.anim.clone() # without this, really strange stuff will occur
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

		self.collidedWith = [] # list of things I collided with this frame
		self.artAngle = 0
		self.flagForRemoval = False
		self.possibleCrosses = []
		self.checkedCol = {}
		self.disruptive = False # if this is false, fast-moving objects will know to go through this without stopping.
		self.more_vx, self.more_vy = 0, 0
		self.push_vx, self.push_vy = 0, 0 # not used for movement, just for tracking it
		self.autoconform_geom = False # if true, the geometry of this object will automatically scale to the size of its graphics
		self.mobile = True # set this to false if this object never moves, or it is moved by a parent object.
		self.flags = {'push left':False, 'push right':False, 'push up':False, 'push down':False, 
						'stay left':False, 'stay right':False, 'stay up':False, 'stay down':False} # these are reset every frame
		self.was_grounded = False

	def flag(self, key):
		self.flags[key] = True
	def unflag(self, key):
		self.flags[key] = False

	def closest(self, ents):
		""" returns the entity which is closest to me """
		shortestDist = 0
		closestEnt = None
		for e in ents:
			xd = math.min(e.geom.right - self.geom.left, self.geom.right - e.geom.left)
			yd = math.min(e.geom.bottom - self.geom.top, self.geom.bottom - e.geom.top)
			if (self.geomtop < self.geomtop < self.geombottom or self.geomtop < self.geombottom < self.geombottom) or (
				e.geomtop < self.geomtop < e.geombottom or e.geomtop < self.geombottom < e.geombottom):
				yd = 0
			if (self.geomleft < self.geomleft < self.geomright or self.geomleft < self.geomright < self.geomright) or (
				e.geomleft < self.geomleft < e.geomright or e.geomleft < self.geomright < e.geomright):
				xd = 0
			dist = math.sqrt(xd**2 + yd**2)
			if closestEnt == None or dist < shortestDist:
				shortestDist = dist
				closestEnt = e
		return closestEnd

	def was_closest(self, ents):
		""" returns the entity which was closest to me at the last frame """
		shortestDist = 0
		closestEnt = None
		for e in ents:
			xd = min(e.last.right - self.last.left, self.last.right - e.last.left)
			yd = min(e.last.bottom - self.last.top, self.last.bottom - e.last.top)
			if (self.last.top < self.last.top < self.last.bottom or self.last.top < self.last.bottom < self.last.bottom) or (
				e.last.top < self.last.top < e.last.bottom or e.last.top < self.last.bottom < e.last.bottom):
				yd = 0
			if (self.last.left < self.last.left < self.last.right or self.last.left < self.last.right < self.last.right) or (
				e.last.left < self.last.left < e.last.right or e.last.left < self.last.right < e.last.right):
				xd = 0
			dist = math.sqrt(xd**2 + yd**2)
			if closestEnt == None or dist < shortestDist:
				shortestDist = dist
				closestEnt = e
		return closestEnt
		

	def adjustGeomToImage(self):
		if self.anim == None or self.anim == -1: return
		m = self.anim.getImage()
		if m == None: return
		centx = self.geom.centerx
		geomb, lastb = self.geom.bottom, self.last.bottom
		self.geom.width, self.geom.height = m.get_size()
		self.last.size = self.geom.size
		self.geom.bottom, self.last.bottom, self.geom.centerx = geomb, lastb, centx

	def _xdist(self):
		""" returns the x distance travelled since last frame """
		return self.geom.x - self.last.x
	def _ydist(self):
		""" returns the y distance travelled since last frame """
		return self.geom.y - self.last.y

	def _lint(self, la, lb, thresh=1):
		""" Returns True if the line segments (a,b,c,d) la and lb intersect. """
		pa1, pa2 = (la[0], la[1]), (la[2], la[3])
		pb1, pb2 = (lb[0], lb[1]), (lb[2], lb[3])

		atop = min(pa1[1], pa2[1])
		abot = max(pa1[1], pa2[1])
		aleft= min(pa1[0], pa2[0])
		aright=max(pa1[0], pa2[0])

		btop = min(pb1[1], pb2[1])
		bbot = max(pb1[1], pb2[1])
		bleft= min(pb1[0], pb2[0])
		bright=max(pb1[0], pb2[0])

		# calculate slope, or set to None if it is undefined.
		if pa2[0]-pa1[0] != 0:
			ma = (pa2[1]-pa1[1])/(pa2[0]-pa1[0])
		else:
			ma = None
			ba = None
		if pb2[0]-pb1[0] != 0:
			mb = (pb2[1]-pb1[1])/(pb2[0]-pb1[0])
		else:
			mb = None
			bb = None

		# calculate y-intercept
		if ma != None:
			ba = pa1[1] - ma*pa1[0]
		if mb != None:
			bb = pb1[1] - mb*pb1[0]
		

		if ma == None: # la is vertical
			if mb == None: # both lines vertical
				if abs(pa1[0] - pb1[0]) > thresh: return False # can only intersect if they are on top of each other
				return (atop <= btop <= abot or atop <= bbot <= abot) and pa1[0] == pb1[0]
			else:
				if bleft <= aleft <= bright and atop <= btop <= abot and atop <= bbot <= abot:
					return True
				yb = mb * pa1[0] + bb
				return atop <= yb <= abot and btop <= yb <= bbot
		elif mb == None:
			if aleft <= bleft <= aright and btop <= atop <= bbot and btop <= abot <= bbot: return True
			ya = ma * pb1[0] + ba
			return btop <= ya <= bbot and atop <= ya <= abot
		else: # normal testing
			if ma == mb: # darnit already there are so many edge-cases! This is if they both have the same slope.
				return (aleft <= bleft <= aright or aleft <= bright <= aright) and (atop <= btop <= abot or
						atop <= bbot <= abot)
			px = (bb - ba)/(ma-mb)

			# set py to the f= of the more accurate formula (lower slope)
			if abs(ma) < abs(mb):
				py = ma * px + ba
			else:
				py = mb * px + bb

			#if abs(py - ma * px - ba) > thresh or abs(py - mb * px - bb) > thresh: return False
			if aleft <= px <= aright and atop <= py <= abot and bleft <= px <= bright and btop <= py <= bbot:
				return True
		return False
		
	def _between(self, a, b, c):
		""" tests is c is between a and b """
		return a < c < b or a > c > b

	def _inpath(self, other):
		""" Returns true if the other entity is between my first and last positions. """
		if (self._between(self.last.centerx, self.geom.centerx, other.last.centerx) or 
				self._between(self.last.centerx, self.geom.centerx, other.geom.centerx)):
			return True
		if (self._between(self.last.centery, self.geom.centery, other.last.centery) or 
				self._between(self.last.centery, self.geom.centery, other.geom.centery)):
			return True
		return False

	def _crossed(self, other):
		""" Returns true if the paths of these objects crossed in the last frame.
			This should be used for fast-moving projectiles to make sure they
			are not going through things. This is /not/ very precise. """

		if not other.disruptive and not self.disruptive and not (self.attributes.count("touch_player")!=0
				 and other is t12.player) and not (self.attributes.count("touch_enemies")!=0 and other.attributes.count("actors")!=0
				 and other is not t12.player):
			return False

		# let other=O, last=L, current=C
		# O   L-----------C
		# see, if O is way over there on the left, who cares about it?
		if not self._inpath(other):
			return False

		# wow, how awesome! The line widths match up! Who knew that "top bottom" has the same number of characters as "left right"?!
		if self.last.top >= other.last.bottom and self.geom.top >= other.geom.bottom: return False
		if self.last.bottom <= other.last.top and self.geom.bottom <= other.geom.top: return False
		if self.last.right <= other.last.left and self.geom.right <= other.geom.left: return False
		if self.last.left >= other.last.right and self.geom.left >= other.geom.right: return False

		mlines = ( (self.last.centerx, self.last.centery, self.geom.centerx, self.geom.centery), # 0 - path line
			(self.geom.left+1, self.geom.top+1, self.geom.left+1, self.geom.bottom-1), # 1 - left line
			(self.geom.right-1, self.geom.top+1, self.geom.right-1, self.geom.bottom-1), # 2 - right line
			(self.geom.left+1, self.geom.top+1, self.geom.right-1, self.geom.top+1), # 3 - top line
			(self.geom.left+1, self.geom.bottom-1, self.geom.right-1, self.geom.bottom-1), # 4 - bottom line
			(self.last.left+1, self.last.top+1, self.geom.left+1, self.geom.top+1),
			(self.last.right-1, self.last.top+1, self.geom.right-1, self.geom.top+1),
			(self.last.left+1, self.last.bottom-1, self.geom.left+1, self.geom.bottom-1),
			(self.last.right-1, self.last.bottom-1, self.geom.right-1, self.geom.bottom-1)
			)

		olines = ( (other.last.centerx, other.last.centery, other.geom.centerx, other.geom.centery), # 0 - path line
			(other.geom.left+1, other.geom.top+1, other.geom.left+1, other.geom.bottom-1), # 1 - left line
			(other.geom.right-1, other.geom.top+1, other.geom.right-1, other.geom.bottom-1), # 2 - right line
			(other.geom.left+1, other.geom.top+1, other.geom.right-1, other.geom.top+1), # 3 - top line
			(other.geom.left+1, other.geom.bottom-1, other.geom.right-1, other.geom.bottom-1), # 4 - bottom line
			(other.last.left+1, other.last.top+1, other.geom.left+1, other.geom.top+1),
			(other.last.right-1, other.last.top+1, other.geom.right-1, other.geom.top+1),
			(other.last.left+1, other.last.bottom-1, other.geom.left+1, other.geom.bottom-1),
			(other.last.right-1, other.last.bottom-1, other.geom.right-1, other.geom.bottom-1)
			)

		for m in mlines:
			for o in olines:
				if self._lint(m, o):
					return True
		return False


	def checkCollision(self, other):
		if self.checkedCol.has_key(other.id):
			return
		self.checkedCol[other.id] = other

		if self.intersects(other):
			self.collision(other)
		
		if ((abs(self._xdist()) > self.geom.width or abs(self._ydist()) > self.geom.height)):
			if self._crossed(other):
				self.possibleCrosses.append(other)

		other.checkCollision(self)

	def finalizeCollision(self):
		if len(self.possibleCrosses) > 0:
			cross = self.was_closest(self.possibleCrosses)
			self.collision(cross)
			self.possibleCrosses = []
		self.checkedCol.clear()

	def draw(self, artist):
		if self.anim is None:
			artist.drawRect(self.geom.topleft, self.geom.size)
		elif self.anim == -1:
			return
		elif self.anim.getImage() != None:
			m = self.anim.getImage()
			if self.stretchArt:
				z = artist.drawImage(m, self.geom.topleft, self.geom.size, self.artAngle)
				rect = (self.geom.left, self.geom.top, z.get_width(), z.get_height())
				artist.addDirtyRect(rect)
			else:
				mrect = (self.geom.centerx - m.get_width()/2, self.geom.centery - m.get_height()/2)
				z = artist.drawImage(image=m, pos=mrect, angle=self.artAngle)
				rect = (mrect[0], mrect[1], z.get_width(), z.get_height())
				artist.addDirtyRect(rect)
			#artist.drawRect(rect[0:2], rect[2:4])
		
		artist.addDirtyRect(self.geom)
		artist.addDirtyRect(self.last)

	def updateArt(self, time):
		if self.anim is not None and self.anim != -1:
			self.anim.update(time)

	def updatelast(self):
		self.last.x = self.geom.x
		self.last.y = self.geom.y
		self.last.width = self.geom.width
		self.last.height = self.geom.height

	def goNextPos(self):
		self._updateMovement(self, t12.seconds_passed)
	def goPrevPos(self):
		self._updateMovement(self, -t12.seconds_passed)

	def _updateMovement(self, time):
		self.velx += self.acx * time
		self.vely += self.acy * time
		self._incx += (self.velx+self.more_vx) * time
		self._incy += (self.vely+self.more_vy) * time
		

		if abs(self._incx) > 0:
			val = int(self._incx)
			self.geom.centerx += val
			self._incx -= val
		if abs(self._incy) > 0:
			val = int(self._incy)
			self.geom.centery += val
			self._incy -= val


	def update(self, time, move=True):
		self.updatelast()

		if self.autoconform_geom and self.anim is not None and self.anim != -1:
			img = self.anim.getImage()
			if img != None:
				iw, ih = img.get_size()
				if self.geom.width != iw or self.geom.height != ih:
					self.adjustGeomToImage()

		if move and self.mobile:
			self._updateMovement(time)

		self._extraUpdate(self)

		self.was_grounded = self.grounded
		self.more_vx, self.more_vy = 0, 0
		self.grounded = False # reset grounded
		self.collidedWith = [] # clear list of things I collided with
		for k in self.flags:
			self.flags[k] = False

	def _extraUpdate(self, par=None):
		return None

	def intersects(self, other):
		return self.geom.colliderect(other.geom)

	def collision(self, other):
		""" Called by external classes and should never be overriden. """
		# prevent things from hitting themselves
		if other is self: return
		# things cannot hit each other more than once in a frame!
		if self.collidedWith.count(other) >= 1: return
		if other.collidedWith.count(self) >= 1: return
		self.collidedWith.append(other)
		other.collidedWith.append(self)
		# call the code that actually does something with the collision
		self._collision(other)
		other._collision(self)

	def _collision(self, other):
		""" This method is called when this entity hits another entity.
			Subclasses are expected to override it to make it do something useful. """
		return None

class FloorBlock(Entity):
	def __init__(self, geom, anim):
		""" Use Block instead of FloorBlock, please. """
		Entity.__init__(self, geom, anim)
		self.attributes.append("geometry")
		self.attributes.append("art_mid")

	def intersects(self, other_entity):
		if Entity.intersects(self, other_entity):
			return True
		if self.geom.top - other_entity.geom.bottom <= 3 and (self.geom.right > other_entity.geom.right > self.geom.left
				or self.geom.right > other_entity.geom.left > self.geom.left):
			return True
		return False

	def _collision(self, other):
		if other.vely >= 0:
			other.vely = self.vely
			if other.acy > 0:
				other.acy = 0 # stop accelerating downwards...
			other.geom.bottom = self.geom.top
		other.grounded = True

class Block(FloorBlock):
	def __init__(self, geom, anim):
		FloorBlock.__init__(self, geom, anim)
		self.sticky = True # I decided to set this to true by default because this is how most platformers behave.
		self.disruptive = True # yes, fast moving objects should stop when they hit this.

	def intersects(self, other_entity):
		if Entity.intersects(self, other_entity):
			return True
		if self.geom.top - other_entity.geom.bottom <= 3 and (self.geom.right > other_entity.geom.right > self.geom.left
				or self.geom.right > other_entity.geom.left > self.geom.left) and other_entity.geom.top < self.geom.bottom:
			return True
		return False

	def _collision(self, other):
		if other.geom.bottom < self.geom.top and other.last.bottom < self.last.top:
			other.grounded = True
			other.lastFloor = self

			if self.sticky or (other.vely + other.more_vy) > 0:
				other.geom.bottom = self.geom.top

			if self.sticky:
				other.push_vy = self.vely
				if self.vely > 0:
					other.more_vy = self.vely
				if other.vely > 0:
					other.vely = 0
			else:
				other.more_vy = 0
				if (self.vely > other.vely and other.vely >= 0) or (self.vely < other.vely and self.vely < 0):
					other.vely = self.vely

			if self.vely < 0: other.flag('push up')
			else: other.flag('stay up')

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
			other.lastFloor = self
			other.more_vx = self.velx

			if self.sticky:
				other.push_vy = self.vely
				if self.vely > 0:
					other.more_vy = self.vely
				if other.vely > 0:
					other.vely = 0
			else:
				other.more_vy = 0
				if (self.vely > other.vely and other.vely >= 0) or (self.vely < other.vely and self.vely < 0):
					other.vely = self.vely

			if self.vely < 0: other.flag('push up')
			else: other.flag('stay up')
		elif wleft and not left:
			other.geom.right = self.geom.left
			other.velx = self.velx
			if self.velx < 0: other.flag('push left')
			else: other.flag('stay left')
		elif wright and not right:
			other.geom.left = self.geom.right
			other.velx = self.velx
			if self.velx > 0: other.flag('push right')
			else: other.flag('stay right')
		elif wbelow and not below or not (abs(other.geom.bottom - self.geom.top) < abs(self.geom.bottom - other.geom.top)):
			other.geom.top = self.geom.bottom
			other.vely = self.vely
			if self.vely > 0: other.flag('push down')
			else: other.flag('stay down')
		elif not above:
			other.geom.bottom = self.geom.top
			other.grounded = True
			other.lastFloor = self

			if self.sticky:
				other.push_vy = self.vely
				if self.vely > 0:
					other.more_vy = self.vely
				if other.vely > 0:
					other.vely = 0
			else:
				other.more_vy = 0
				if (self.vely > other.vely and other.vely >= 0) or (self.vely < other.vely and self.vely < 0):
					other.vely = self.vely

			if self.vely < 0: other.flag('push up')
			else: other.flag('stay up')

		if self.sticky and (other.vely + other.more_vy) < self.vely:
			other.vely = 0
			other.more_vy = self.vely

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

class Activator(TriggerEntity):
	def __init__(self, geom, anim):
		TriggerEntity.__init__(self, geom, anim)
		self.attributes.append("activators")
		self.activated = False
		self.allowActivation = True

	def update(self, time):
		TriggerEntity.update(self, time)
		if self.activated:
			self.allowActivation = False
		else:
			self.allowActivation = True
		self.activated = False

	def activate(self, par=None):
		self.activated = True
		if self.allowActivation:
			self.trigger(par)
	

class MotionTrigger(TriggerEntity):
	def __init__(self, geom, anim):
		TriggerEntity.__init__(self, geom, anim)
		self.attributes.append("geometry")

	def _collision(self, other):
		if isinstance(other, Actor):
			TriggerEntity.trigger(self, other)

class Elevator(Entity):
	def _collisionF(self, other):
		Block._collision(self.floor, other)
		if other is not t12.player: return
		if self.state == 0 and self.playerref == None:
			if self.geom.y == self.y1:
				self.state = 1
			else:
				self.state = -1
			
		self.playerref = other

	def _collisionR(self, other):
		Block._collision(self.roof, other)
		if other is not t12.player: return
		if self.state == 0 and self.playerref == None:
			if self.geom.y == self.y1:
				self.state = 1
			else:
				self.state = -1
			
		self.playerref = other

	def __init__(self, geom, targety, duration):
		""" Paramaters: geometry (rectangle),  targety (where the elevator will go), and duration (the 
			time in seconds it will take to get there) """
		Entity.__init__(self, geom, -1)
		self.floor = Block((self.geom.left, self.geom.bottom-20, self.geom.width, 20), None)
		self.roof = Block((self.geom.left, self.geom.top, self.geom.width, 20), None)
		self.floor.sticky = True
		self.roof.sticky = True
		self.roof.name = "Elevator Roof"
		self.floor.name = "Elevator Floor"
		self.name = "Elevator"
		self.floor._collision = self._collisionF
		self.roof._collision = self._collisionR
		self.floor.mobile, self.roof.mobile = False, False
		self.spawn.append(self.floor)
		self.spawn.append(self.roof)
		self.y1 = self.geom.top
		self.y2 = targety
		self.state = 0 # 0 = stopped, 1 = go towards position 1, -1 = go towards position 0
		self.duration = duration
		self.disruptive = False
		if self.y2 - self.y1 > 0:
			self.dir = 1
		else:
			self.dir = -1
		self.speed = abs( (self.y2 - self.y1) / duration)
		self.attributes.append("geometry")
		self.playerref = None

	def intersects(self, other_entity):
		if Entity.intersects(self, other_entity):
			return True
		if self.geom.top - other_entity.geom.bottom <= 3 and (self.geom.right > other_entity.geom.right > self.geom.left
				or self.geom.right > other_entity.geom.left > self.geom.left) and self.geom.bottom > other_entity.geom.top:
			return True
		return False

	def update(self, time):
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

		self.floor.vely = self.vely
		self.roof.vely = self.vely

		Entity.update(self, time)

		self.floor.updatelast()
		self.roof.updatelast()
		self.floor.geom.top = self.geom.bottom - 20
		self.roof.geom.top = self.geom.top

		if self.playerref != None:
			if not self.roof.intersects(self.playerref) and not self.floor.intersects(self.playerref):
				self.playerref = None

class Actor(Entity):
	def __init__(self, geom, anim):
		""" geom and anim are as normal, and the "feet" paramater should
			be a tuple for the startx and endx of the feet on the sprite.
			If it is set to None, the feet are assumed to be the bounds of
			the geometry. """
		Entity.__init__(self, geom, anim)

		self.attributes.append("actors")
		self.attributes.append("art_front")
		self.attributes.append("touch_geom")

		self.weapon = None

		self.maxhealth = 10 # arbitrary default
		self.health = self.maxhealth
		self.jumpheight = 50 # arbitrary
		self.speed = 100 # maximum horizontal movement speed (pixels/second)
		self.acceleration = 500 # pixels/sec^2 acceleration
								# if you want the player to accelerate to max-speed
								# instantly just set this to a really big number (like self.speed * 10**3)
		self.lastFloor = None # the last entity I stood on
		self.update(0) # for the feetbox
		self.think() # for AI

	def attack(self, direction, target=None):
		""" Direction is an integer. see t12.dir_up, t12.dir_left, et cetera """
		if self.weapon != None:
			if direction == t12.dir_up:
				angle = 270
			elif direction == t12.dir_down:
				angle = 90
			elif direction == t12.dir_left:
				angle = 180
			elif direction == t12.dir_right:
				angle = 0
			self.weapon.use(self, self.geom.center, (angle, 1000))
		return None


	def think(self):
		return None

	def _isSquashed(self):
		flags = self.flags # convenience
		if flags['push up'] and (flags['push down'] or flags['stay down']): return True
		if flags['push down'] and flags['stay up']: return True
		if flags['push left'] and (flags['push right'] or flags['stay right']): return True
		if flags['push right'] and flags['stay left']: return True
		return False

	def update(self, time):
		self.think()

		if self._isSquashed():
			print self.name + " was just squashed."

		Entity.update(self, time)

		if self.was_grounded and not self.grounded:
			if self.vely > 0:
				self.vely = 0

	def jump(self):
		self.vely = -math.sqrt(t12.gravity * self.jumpheight * 2)
		self.geom.top -= 3
		self.vely += self.push_vy
		self.more_vy = 0

	def left(self):
		if self.anim != None: self.anim.runSequence("go left", "left")
		self.velx = max(-self.speed, self.velx - self.acceleration)

	def right(self):
		if self.anim != None: self.anim.runSequence("go right", "right")
		self.velx = min(self.speed, self.velx + self.acceleration)

	def stopX(self):
		self.velx = 0
		if self.anim.seq_name == "go right": self.anim.runSequence("right")
		if self.anim.seq_name == "go left": self.anim.runSequence("left")

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

class Projectile(Entity):
	def __init__(self, geom, anim, angle, magnitude):
		Entity.__init__(self, geom, anim)
		self.velx = magnitude * math.cos(math.radians(angle))
		self.vely = magnitude * math.sin(math.radians(angle))
		self.baseAngle = angle
		self.artAngle = 360 - angle # flip vertically
		self.moveAngle = angle
		self.attributes.append("touch_geom")

	def setAngle(self, angle):
		self.artAngle = 360 - (self.baseAngle + angle)
		if self.artAngle >= 360: self.artAngle = self.artAngle % 360
		self.moveAngle = angle
		self.setMagnitude(math.sqrt(self.velx**2 + self.vely**2))

	def setMagnitude(self, magnitude):
		self.velx = magnitude * math.cos(math.radians(self.moveAngle))
		self.vely = magnitude * math.sin(math.radians(self.moveAngle))

	def _collision(self, other):
		if (other.disruptive and other.attributes.count("geometry") > 0) or isinstance(other, Actor):
			self.anim.runSequence("hit")
			self.flagForRemoval = True
			return True
		return False

class DamageProjectile(Projectile):
	def __init__(self, geom, anim, angle, magnitude, damage):
		Projectile.__init__(self, geom, anim, angle, magnitude)
		self.damage = damage
		self.ignorelist = [] # list of entities I can't hit
		self.anim.current_seq.flipy = True

	def finalizeCollision(self):
		Entity.finalizeCollision(self)

	def _collision(self, other):
		#print self.name, "hit", other.name
		if not Projectile._collision(self, other): return
		if self.ignorelist.count(other) > 0: return
		if isinstance(other, Actor):
			other.health -= self.damage

class FireballGun(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.name = "Fireball Gun"

	def use(self, by, startpoint, tar_polar):
		ball = DamageProjectile((0, 0, 10, 1), t12.sprites["Firebolt"], 90, tar_polar[1], 1)
		ball.setAngle(tar_polar[0])
		ball.adjustGeomToImage()
		ball.geom.center = startpoint
		ball.attributes.append("touch_enemies")
		ball.name = "FireballGun Fireball"
		by.spawn.append(ball)
