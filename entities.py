import graphwrap, physics, math

class Entity:
	def __init__(self, poly, anim):
		self.geom = poly # RotPoly
		self.anim = anim # AnimSprite
		self.velx, self.vely = 0, 0
		self.move_allowed = True # flag set to false if collision is imminent
		
	def draw(self, artist):
		if self.anim is None:
			artist.drawLines(self.geom.getLines()) # this is throwing an exception in graphwrap.Artist for some reason

		br = self.boundingRect()
		artist.addDirtyRect(br)

	def updateArt(self, time):
		if self.anim is not None:
			self.anim.update(time)

	def update(self, time):
		self.geom.centerx += self.velx * time
		self.geom.centery += self.vely * time

	def left(self):
		return self.geom.left()
	def right(self):
		return self.geom.right()
	def top(self):
		return self.geom.top()
	def bottom(self):
		return self.geom.bottom()
	def boundingRect(self):
		return self.geom.boundingRect()

	def smearsIntersect(self, other_entity, time):
		smear1 = physics.RotPoly((0, 0), self.getMotionSmear(time), 0)
		smear2 = physics.RotPoly((0, 0), other_entity.getMotionSmear(time), 0)
		return smear1.intersects(smear2)

	def willIntersect(self, poly, time):
		vangle = physics.getAngle(self.velx, self.vely)
		mag = math.sqrt(self.velx**2 + self.vely**2)
		him = physics.rotatedPoints(self.geom.getCenter(), poly, -vangle)

#   __   _  _A...............__   _  _				^
#  /  \_/ \/ \				/  \_/ \/ \				|
#  |          \				|          \	(-1, 1) | (1, 1)	
#  \       ___/	   SMEAR	\       ___/	<-------+------->	
#   |     |  				 |     |	   (-1, -1) | (1, -1)
#   \     \__				 \     \__				|
#    \_______\B.............. \_______\				V
# 


	def getMotionSmear(self, time):
		""" The motion smear is the polygon that would be created if this entity's motion path were smeared out over time. """
		pA, pB = None, None # see above ascii art for what points a and b are

		vangle = physics.getAngle(self.velx, self.vely)
		mag = math.sqrt(self.velx**2 + self.vely**2)
		me1 = physics.rotatedPoints(self.geom.getCenter(),
				self.geom.getPoints(), -vangle, False) # -vangle rotates to horizontal -->


		me2 = []
		for m in me1:
			me2.append((m[0]+mag*time, m[1]))


		# top-right point
		for i in range(len(me1)):
			p = me1[i]
			if pA is None or p[1] < me1[pA][1] or (p[1] == me1[pA][1] and p[0] > me1[pA][0]):
				pA = i

		# bottom-right point
		for i in range(len(me1)):
			p = me1[i]
			if pB is None or p[1] > me1[pB][1] or (p[1] == me1[pB][1] and p[0] > me1[pB][0]):
				pB = i

		smear = []

		start = pB
		if me1[pB-1][0] < me1[pB][0]:
			direction = -1
		else:
			direction = 1

		poly = me1
	 	i = start

		# debugging stuff
		#print "me1 len: " + str(len(me1)) + ", a: " + str(pA) + ", b: " + str(pB) + ", i: " + str(i)
		#print "dir=" + str(direction)
		
		# constructing the smear poly
		while True:
			# made into a new tuple just in case they're mutable for some reason
			smear.append((poly[i][0], poly[i][1]))

			if i == pA and poly == me1:
				poly = me2
			elif i == pB and poly == me2:
				break
			else:
				i += direction

			if i >= len(me1):
				i = 0
			elif i < 0:
				i = len(me1)-1

		return physics.rotatedPoints(self.geom.getCenter(), smear, vangle)
		
		
