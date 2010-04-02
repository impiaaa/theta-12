import entities, graphwrap, t12, pygame

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
		self.touch_geom = [] # things that collide with geometry

		# these groups are used for layering the graphics.
		# general guidlines for what to put where:
		# back - background objects like trees/bushes/decorations/etc
		# mid - geometry, walls, floors, platforms, buttons...
		# front - npcs
		# over - explosions and particle effects and such
		self.art_back, self.art_mid, self.art_front, self.art_over = [], [], [], []
		self.playerstart = (320, 240) # this probably should left as default, but should be defined in the level editor.

	def _removeFrom(self, entity, entities):
		while entities.count(entity) > 0: entities.remove(entity)

	def remove(self, entity):
		""" Removes this entity from all lists where it is found. """
		self._removeFrom(entity, self.all)
		self._removeFrom(entity, self.background)
		self._removeFrom(entity, self.geometry)
		self._removeFrom(entity, self.touch_geom)
		self._removeFrom(entity, self.touch_player)
		self._removeFrom(entity, self.touch_enemies)
		self._removeFrom(entity, self.activators)
		self._removeFrom(entity, self.actors)
		self._removeFrom(entity, self.art_back)
		self._removeFrom(entity, self.art_front)
		self._removeFrom(entity, self.art_over)
		self._removeFrom(entity, self.art_mid)

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
		if entity.attributes.count("touch_geom") >= 1:
			self.touch_geom.append(entity)

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
	trig3.name = "Steve"

	trig.adjustGeomToImage()
	trig2.adjustGeomToImage()
	trig.geom.bottom, trig2.geom.bottom = 400, 400


	troom.add(trig)
	troom.add(trig2)
	troom.add(trig3)

	for i in range(24):
		tblock = entities.Block((50*i, 400, 50, 20), None)
		tblock.attributes.append("geometry")
		tblock.name = str(i)
		if i % 2 == 0:
			tblock.sticky = True
		troom.add(tblock)
	
	fblock = entities.Block((300, 200, 50, 50), graphwrap.staticSprite(t12.imageLoader.getImage("global/sprites/box.png")))
	fblock.name = "Block"
	def reactor(par=None):
		fblock.geom.centerx = trig.geom.centerx
		trig.anim.runSequence("pressed")
		trig2.anim.runSequence("unpressed")
	def reactor2(par=None):
		fblock.geom.centerx = trig2.geom.centerx
		trig2.anim.runSequence("pressed")
		trig.anim.runSequence("unpressed")
	def react3(par=None):
		if par != None and isinstance(par, entities.Actor):
			if par.lastFloor == None:
				par.geom.bottom = fblock.geom.top-5
				par.geom.centerx = fblock.geom.centerx
			else:
				par.geom.centerx, par.geom.bottom = par.lastFloor.geom.centerx, par.lastFloor.geom.top
				par.updatelast()
	trig.reactors.append(reactor)
	trig2.reactors.append(reactor2)
	trig3.reactors.append(react3)

	troom.add(fblock)

	wall = entities.Block((100, 200, 50, 200), None)
	wall.name = "Joe"
	troom.add(wall)
	
	elevator = entities.Elevator((600, 200, 150, 200), 100, 0.5)
	troom.add(elevator)

	for i in xrange(18):
		# xpos calculation
		if i < 8:
			blah = 1000 + 200*i
		else:
			blah = 1000 + 200*7 - 200*(i-6)
		b = entities.Block((blah, 380-30*i, 100, 20), None)
		b.name = "Step " + str(i)
		troom.add(b)

	shifter = entities.Block((-100, 420, 100, 20), None)
	shifter.name = "shifter"
	shifter.shiftdir = 0
	shifter.start = shifter.geom.left

	shifter2 = entities.Block((shifter.geom.left - 1200, -580, 100, 20), None)
	shifter2.name = "shifter2"
	shifter2.shiftdir = 0
	shifter2.start = shifter2.geom.left

	def shifterShift(par):
		if par.name == "shifter" and pygame.key.get_pressed()[pygame.K_i]:
			t12.player.geom.centerx = par.geom.centerx
			t12.player.geom.bottom = par.geom.top

		if par.shiftdir == -1:
			if par.geom.left <= par.start-1000:
				par.velx = 500
				par.vely = 500
				par.shiftdir = 1
		elif par.shiftdir == 1 or par.shiftdir == 0:
			if par.geom.left >= par.start or par.shiftdir == 0:
				par.velx = -500
				par.vely = -500
				par.shiftdir = -1
	shifter._extraUpdate = shifterShift
	shifter2._extraUpdate = shifterShift
	troom.add(shifter)
	troom.add(shifter2)
	troom.add(entities.Block((shifter.geom.left - 1100, -580, 100, 20), None))

	guyanim = graphwrap.AnimSprite()
	guyanim.putSequence("right", graphwrap.staticSequence(
						t12.imageLoader.getImage("global/sprites/person_stand.png")))
	guyanim.putSequence("left", graphwrap.staticSequence(
						pygame.transform.flip(t12.imageLoader.getImage("global/sprites/person_stand.png"), 1, 0)))
	guyanim.putSequence("right punch", graphwrap.staticSequence(
						t12.imageLoader.getImage("global/sprites/person_punch.png")))
	guyanim.putSequence("left punch", graphwrap.staticSequence(
						pygame.transform.flip(t12.imageLoader.getImage("global/sprites/person_punch.png"), 1, 0)))
	guyanim.runSequence("left")
	guy = entities.Actor((0, 0, 1, 1), guyanim)
	guy.name = "Guy"
	guy.jumpheight = 300
	guy.speed = 200
	guy.acceleration = 100
	guy.geom.centerx = elevator.geom.centerx
	guy.geom.bottom = elevator.geom.top - 1
	guy.autoconform_geom = True

	fireballanim = graphwrap.AnimSprite()
	fireseq = graphwrap.AnimSequence(["global/sprites/fire1.png", "global/sprites/fire2.png", "global/sprites/fire3.png"], 0.2, False)
	fireballanim.runSequence(fireseq)

	def guythink():
		guy.lastThrow = 0
		if guy.geom.centerx < t12.player.geom.centerx:
			if guy.anim.seq_name == "left": guy.anim.runSequence("right")
			if guy.anim.seq_name == "left punch": guy.anim.runSequence("right punch")
		elif guy.geom.centerx > t12.player.geom.centerx:
			if guy.anim.seq_name == "right": guy.anim.runSequence("left")
			if guy.anim.seq_name == "right punch": guy.anim.runSequence("left punch")

		if guy.geom.left > t12.player.geom.right+50:
			guy.left()
			guy.anim.runSequence("left")
		elif guy.geom.right < t12.player.geom.left-50:
			guy.right()
			guy.anim.runSequence("right")
		else:
			guy.velx = 0

		if guy.geom.bottom > t12.player.geom.bottom and guy.grounded:
			guy.jump()
			if guy.anim.seq_name == "left punch": guy.anim.runSequence("left")
			elif guy.anim.seq_name == "right punch": guy.anim.runSequence("right")
		elif t12.player.geom.bottom > guy.geom.bottom > t12.player.geom.top or t12.player.geom.bottom > guy.geom.top > t12.player.geom.top:
			if guy.anim.seq_name == "left": guy.anim.runSequence("left punch")
			elif guy.anim.seq_name == "right": guy.anim.runSequence("right punch")

			tt = int(t12.game_time * 100)
			if tt != guy.lastThrow and tt % 10 == 0:
				guy.lastThrow = tt
				meat = entities.DamageProjectile((0, 0, 1, 1), fireballanim, 90, 500, 1)
				meat.adjustGeomToImage()
				meat.geom.center = guy.geom.center
				meat.attributes.append("touch_player")
				meat.name = "Doom"
				if guy.anim.seq_name == "left punch": meat.setAngle(180)
				elif guy.anim.seq_name == "right punch": meat.setAngle(0)
				guy.spawn.append(meat)
		else:
			if guy.anim.seq_name == "left punch": guy.anim.runSequence("left")
			elif guy.anim.seq_name == "right punch": guy.anim.runSequence("right")
				
				
	guy.think = guythink

	troom.add(guy)

tlevel.load = tload
