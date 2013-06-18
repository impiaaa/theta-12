import sys, os, random, math
import pygame
from pygame.locals import *
import t12, physics, entities, graphwrap, level
import time
import inventory

# helper functions
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

# testing only
def randomEntity():
	points = ((-10, -10), (-5, -20), (0, -10), (5, 7), (30, 20), (50, -30))
	geom = physics.RotPoly((320, 240), points, random.random()*math.radians(360))
	e = entities.Entity(geom, None)
	speed = random.random() * 100
	e.velx, e.vely = math.cos(e.geom.angle)*speed, math.sin(e.geom.angle)*speed
	#print str(e.geom.getPoints())
	return e


class Engine(object):
	def init(self):
		pygame.init()
		self.drects, self.last_drects = [], []
		self.screen = pygame.display.set_mode((640, 480))
		pygame.display.set_caption("Theta 12")
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))
		
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()
	
		self.font = pygame.font.Font(None, 24) 
			
		self.artist = graphwrap.Artist(self.screen, self.screen.get_size(), self.drects)
		
	
		self.clock = pygame.time.Clock()
		
		t12.current_level = level.tlevel
		t12.current_level.load()
		self.croom = t12.current_level.croom
	
		t12.player = entities.Actor((420.0, 100.0, 30.0, 20.0), t12.sprites["Velociraptor"])
		t12.player.name = "player"
		t12.player.jumpheight = 72 # wikianswers says this number should be 72, but that is boring.
		t12.player.speed = 396 # 396 in/2s according to wikianswers
		t12.player.setHealth(30)
		t12.player.hands = (55, 20)
		t12.player.showhealthbar = False
		
		t12.player.adjustGeomToImage()
		t12.player.stretchArt = False
		t12.player.geom.width = 20 # testing things
	
		self.croom.add(t12.player)
		t12.player.geom.center = self.croom.playerstart
	
		inventory.addWeapon(entities.Pistol(False))
		inventory.addWeapon(entities.FireballGun(False))
		inventory.addWeapon(entities.Shotgun(False))
		inventory.changeWeapon(0)
		
	
		self.firstframe = True
		self.last_time = 0
		self.seconds = 0
		self.ctime = 0
	
		self.lastWeaponTextLength = 0
	
		self.activating = False # is the player pressing the activate button?

	def update(self):
		self.ctime = time.time()
		self.seconds = self.ctime - self.last_time
		t12.seconds_passed = self.seconds
		t12.game_time += self.seconds
		self.last_time = time.time()
		if self.firstframe:
			self.seconds = 0
			self.firstframe = False

		self.screen.blit(self.background, (0, 0))


		# process events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					t12.player.attack(t12.dir_left)
				elif event.key == pygame.K_d:
					t12.player.attack(t12.dir_right)
				elif event.key == pygame.K_w:
					t12.player.attack(t12.dir_up)
				elif event.key == pygame.K_s:
					t12.player.attack(t12.dir_down)
				elif event.key == pygame.K_SPACE:
					self.activating = True
				elif event.key == pygame.K_UP:
					if t12.player.grounded:
						t12.player.jump()
				elif event.key == pygame.K_DOWN:
					t12.player.decelerate(0, 5)
				elif event.key == K_LEFT:
					t12.flags["input left"] = True
					t12.flags["input right"] = False
					#t12.player.anim.runSequence("left")
				elif event.key == K_RIGHT:
					t12.flags["input right"] = True
					t12.flags["input left"] = False
					#t12.player.anim.runSequence("right")
				elif event.key == pygame.K_p:
					t12.camy = t12.player.geom.centery - self.screen.get_height()/2
				elif event.key == pygame.K_c:
					t12.player.geom.center = (200, 100)
					t12.player.velx, t12.player.vely = 0, 0
				elif event.key == pygame.K_r:
					t12.player.resurrect()
				elif event.key == K_ESCAPE:
                                        pygame.quit()
                                        sys.exit()
				elif event.key == K_q:
					inventory.previousWeapon()
				elif event.key == K_e:
					inventory.nextWeapon()
				elif K_9 >= event.key >= K_1:
					inventory.changeWeapon(event.key - K_1)
			if event.type == pygame.KEYUP:
				if event.key == K_LEFT and t12.player.velx < 0:
					t12.flags["input left"] = False
					#t12.player.velx = 0
				elif event.key == K_RIGHT and t12.player.velx > 0:
					t12.flags["input right"] = False
					#t12.player.velx = 0
				elif event.key == pygame.K_SPACE or event.key == pygame.K_e:
					self.activating = False

		# apply air friction
		t12.player.decelerate(5000*self.seconds, 0) # this is really high because low decelerations make it hard.

		# make input mac-friendly
		if not pygame.key.get_pressed()[pygame.K_LEFT]:
			t12.flags["input left"] = False
		if not pygame.key.get_pressed()[pygame.K_RIGHT]:
			t12.flags["input right"] = False
		if t12.flags["input left"]: 
			t12.player.left()
		elif t12.flags["input right"]: 
			t12.player.right()
		else:
			t12.player.stopX()


		# update movement/spawn things
		#print "Updating self.croom.all"
		for e in self.croom.all:
			if e.flagForRemoval:
				if e.name != None:
					t12.spam("Removing " + '"' + e.name + '"')
				self.croom.remove(e)
				continue
			e.update(self.seconds)
			if len(e.spawn) > 0:
				for s in e.spawn:
					self.croom.add(s)
				e.spawn = []

				
		# detect collisions
		#print "Detecting Collisions"
		for a in self.croom.geometry:
			for b in self.croom.touch_geom:
				if a is b: continue # this really should never happen
				a.checkCollision(b)

		for a in self.croom.touch_player:
			if a is t12.player: continue # this really should never happen
			a.checkCollision(t12.player)

		for a in self.croom.touch_enemies:
			for b in self.croom.actors:
				if a is b or b is t12.player: continue
				a.checkCollision(b)

		if self.activating:
			for a in self.croom.activators:
				if a is t12.player: continue # this really should never happen
				if a.intersects(t12.player):
					a.activate()

		#print "Finalizing Collisions"
		for e in self.croom.all:
			e.finalizeCollision()

		#print "Appyling Gravity"
		for a in self.croom.actors:
			if not a.grounded:
				a.acy = t12.gravity
			else:
				a.acy = 0

		wid, hig = self.screen.get_size()
		wd = t12.player.geom.centerx - wid/2
		hd = t12.camy
		if t12.player.geom.top - t12.camy < 50:
			hd = t12.player.geom.top - 100
		elif t12.player.geom.bottom - t12.camy > hig - 50:
			hd = t12.player.geom.bottom - hig + 100 

		#print "Translating Graphics"
		# The following rant describes the next two lines of actual code.
		# Both of these are divided by 5 because in my experience the number 5 works pretty well.
		# What the /5 means is that the time remaining until the camera is where it should be
		# has a "fifth-life" of 1/5. This is just like the half-life of unstable particles (except 1/5th instead of 1/2).
		# So at each frame 1/5 of the remaining distance is covered. Because of this it decelerates nicely as it approaches
		# its goal, and eventually the distance is smaller than an integer value and is rounded off. A sequence of distances,
		# over a period of frames, might look like this: 125, 25, 5, 1, 0.2... and 0.2 is rounded to 0 so it stops.
		# It is entirely possible to replace this simple /5 with a slightly more sophisticated approach that would always
		# reach its destination in a predermined time interval. Feel free to implement this if you dislike my magic numbers.
		# Personally, I think it's just fine how it is now.
		xinc = abs(self.artist.offsetx+wd)/5
		yinc = abs(self.artist.offsety+hd)/5

		if self.artist.offsetx < -wd:
			self.artist.offsetx += xinc
		elif self.artist.offsetx > -wd:
			self.artist.offsetx -= xinc

		if self.artist.offsety < -hd:
			self.artist.offsety += yinc
		elif self.artist.offsety > -hd:
			self.artist.offsety -= yinc

		# draw everything
		#print "Drawing Everything"
		for e in self.croom.art_back:
			e.updateArt(self.seconds)
			e.draw(self.artist)
		for e in self.croom.art_mid:
			e.updateArt(self.seconds)
			e.draw(self.artist)
		for e in self.croom.art_front:
			e.updateArt(self.seconds)
			e.draw(self.artist)
		for e in self.croom.art_over:
			e.updateArt(self.seconds)
			e.draw(self.artist)

		#print "Updating Dirty Rects"
		pygame.display.update(self.last_drects)
		pygame.display.update(self.drects)
		#pygame.display.flip() # debug ONLY!
		move(self.drects, self.last_drects, True)

		#print "Drawing Status Text"
		weapon_text = self.font.render("Weapon: " + t12.player.weapon.name, 1, (0, 0, 0))
		health_text = self.font.render("Health: ", 1, (0, 0, 0))
		self.screen.blit(weapon_text, (10, self.screen.get_height()-30))
		pygame.display.update((10, self.screen.get_height()-30, max(self.lastWeaponTextLength, weapon_text.get_width()), weapon_text.get_height()))
		self.screen.fill((0, 0, 0), (10, self.screen.get_height()-30, max(self.lastWeaponTextLength, weapon_text.get_width()), weapon_text.get_height()))
		self.lastWeaponTextLength = weapon_text.get_width()
		healthx, healthy = 10, self.screen.get_height()-30 - weapon_text.get_height() - 5
		self.screen.blit(health_text, (healthx, healthy))

		healthbar = (healthx+health_text.get_width(), healthy, min(100, max(0, int(100. * t12.player.health / t12.player.maxhealth))), health_text.get_height())
		if healthbar[2] > 0: # don't try to draw the bar if it is less than 1, or things may break.
			self.screen.fill((255, 0, 0), healthbar)
		pygame.draw.rect(self.screen, (0, 0, 0), (healthx+health_text.get_width(), healthy, 100, health_text.get_height()), 1)

		pygame.display.update(healthx, healthy, max(self.lastWeaponTextLength, health_text.get_width()+100), health_text.get_height())

	def main(self):
		self.init()
		while 1:
			self.update()
			#print "Ticking"
			self.clock.tick(60)


if __name__ == "__main__":
	Engine().main()
