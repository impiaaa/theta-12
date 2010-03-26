import entities, graphwrap, t12

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
		self.actors = []

		# these groups are used for layering the graphics.
		# general guidlines for what to put where:
		# back - background objects like trees/bushes/decorations/etc
		# mid - geometry, walls, floors, platforms, buttons...
		# front - npcs
		# over - explosions and particle effects and such
		self.art_back, self.art_mid, self.art_front, self.art_over = [], [], [], []

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
		if entity.attributes.count("actor") >= 1 or entity.attributes.count("actors") >= 1:
			self.actors.append(entity)

		if entity.attributes.count("art_back") >= 1:
			self.art_back.append(entity)
		elif entity.attributes.count("art_front") >= 1:
			self.art_front.append(entity)
		elif entity.attributes.count("art_over") >= 1:
			self.art_over.append(entity)
		else:
			self.art_mid.append(entity)
		



class Level:
	""" this should just be a list of rooms and maybe meta-data on how they attach to each other.
		It should also have a reference to the current room (the room the player is now in), which
		should be set to the starting room by default. """
	def __init__(self):
		""" probably should init level name/number here """
		self.rooms = [] # all rooms
		self.croom = Room() # current room
		self.rooms.append(self.croom)

	def load(self):
		print "no loader"


# This is the code for the "test level" that is currently displayed when main.py is run.
tlevel = Level()

def tload():
	troom = tlevel.croom

	button_anim = graphwrap.AnimSprite()
	button_anim.putSequence("unpressed", graphwrap.staticSequence(t12.imageLoader.getImage("global/sprites/button.png")))
	button_anim.putSequence("pressed", graphwrap.staticSequence(t12.imageLoader.getImage("global/sprites/button-pressed.png")))
	button_anim.runSequence("unpressed")

	trig = entities.Activator((200, 350, 50, 50), button_anim) # this trigger has its .anim set to None, 
															# but most motion triggers will probably be invisible (-1)
	trig2 = entities.Activator((325, 350, 50, 50), button_anim)
	trig3 = entities.MotionTrigger((-1000, 1000, 30000, 100), -1)

	trig.adjustGeomToImage()
	trig2.adjustGeomToImage()
	trig.geom.bottom, trig2.geom.bottom = 400, 400

	troom.add(trig)
	troom.add(trig2)
	troom.add(trig3)

	for i in range(24):
		tblock = entities.Block((50*i, 400, 50, 20), None)
		tblock.attributes.append("geometry")
		if i % 2 == 0:
			tblock.sticky = True
		troom.add(tblock)
	
	fblock = entities.Block((300, 200, 50, 50), graphwrap.staticSprite(t12.imageLoader.getImage("global/sprites/box.png")))
	def reactor(par=None):
		fblock.geom.centerx = trig.geom.centerx
		trig.anim.runSequence("pressed")
		trig2.anim.runSequence("unpressed")
	def reactor2(par=None):
		fblock.geom.centerx = trig2.geom.centerx
		trig2.anim.runSequence("pressed")
		trig.anim.runSequence("unpressed")
	def react3(par=None):
		if t12.player != None:
			if t12.player.lastFloor == None:
				t12.player.geom.bottom = fblock.geom.top-5
				t12.player.geom.centerx = fblock.geom.centerx
			else:
				t12.player.geom.centerx, t12.player.geom.bottom = t12.player.lastFloor.geom.centerx, t12.player.lastFloor.geom.top
				t12.player.updatelast()
	trig.reactors.append(reactor)
	trig2.reactors.append(reactor2)
	trig3.reactors.append(react3)

	troom.add(fblock)

	wall = entities.Block((100, 200, 50, 200), None)
	troom.add(wall)
	
	elevator = entities.Elevator((600, 200, 150, 200), 100, 0.5)
	troom.add(elevator)

	for i in range(20):
		# xpos calculation
		if i < 8:
			blah = 1000 + 200*i
		else:
			blah = 1000 + 200*7 - 200*(i-6)
		b = entities.Block((blah, 380-30*i, 100, 20), None)
		troom.add(b)

tlevel.load = tload
