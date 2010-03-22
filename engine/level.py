import entities

# this is just a basic template for now and will likely be expanded upon.

# the main.py file should contain a single current_level. various entities or perhaps the Rooms should have code to transport the player to the next level when certain conditions are met (a point is reached, a time limit is met, and item is secured, etc etc)

class Room:
	""" Defines all the entities in a screen. Should define things like player starting point. """

	def __init__(self):
		""" probably should init things like level title or something here """
		# these lists contain all the entities in the level. Entities will almost certainly be in at least two of these lists.
		self.all = [] # all the entities in the level. should iterate through this for drawing graphics. do not use this to test collision, it is too slow that way
		self.background = [] # entities that have no collision detection - just decor. like clouds, walls, plants
		self.touch_player = [] # entities that can potentially collide with the player (eg bullets)
		self.touch_enemies = [] # entities that can hit enemies (bullets the player shoots, etc)
		self.activators = [] # entities that do something when the player comes near them or clicks them or something (like buttons or traps)
		self.geometry = [] # objects everything can collide with

	def add(self, entity):
		""" Adds the entity to the appropriate lists based on its attributes """
		self.all.append(entity)
		if entity.attributes.count("background") >= 1:
			self.background.append(entity)
		if entity.attributes.count("touch_player") >= 1:
			self.touch_player.append(entity)
		if entity.attributes.count("touch_enemies") >= 1:
			self.touch_enemies.append(entity)
		if entity.attributes.count("activators") >= 1:
			self.activators.append(entity)
		if entity.attributes.count("geometry") >= 1:
			self.geometry.append(entity)



class Level:
	""" this should just be a list of rooms and maybe meta-data on how they attach to each other.
		It should also have a reference to the current room (the room the player is now in), which
		should be set to the starting room by default. """
	def __init__(self):
		""" probably should init level name/number here """
		self.rooms = [] # all rooms
		self.croom = Room() # current room
		self.rooms.append(self.croom)


# This is the code for the "test level" that is currently displayed when main.py is run.
tlevel = Level()
troom = tlevel.croom
trig = entities.MotionTrigger((100, 100, 50, 50), None) # this trigger has its .anim set to None, 
														# but most motion triggers will probably be invisible (-1)
troom.all.append(trig)
troom.geometry.append(trig)
for i in range(0, 20):
	tblock = entities.Block((50*i, 400, 50, 20), None)
	if i % 2 == 0:
		tblock.sticky = True
	troom.all.append(tblock)
	troom.geometry.append(tblock)

fblock = entities.Block((300, 200, 50, 100), None)
def reactor(par=None):
	fblock.geom.topleft = (200, 200)
trig.reactors.append(reactor)
troom.all.append(fblock)
troom.geometry.append(fblock)

elevator = entities.Elevator((1000, 100, 150, 200), 400, 2)
troom.add(elevator)
