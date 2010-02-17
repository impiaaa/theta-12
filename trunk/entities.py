import graphwrap, physics, math

class Entity:
	def __init__(self, poly, anim):
		self.geom = poly # RotPoly
		self.anim = anim # AnimSprite
		self.velx, self.vely = 0, 0
		
	def draw(self, artist):
		if self.anim == None:
			artist.drawLines(self.geom.getLines())

	def update(self, time):
		self.anim.update(time)

	def willIntersect(self, poly, time):
		vangle = physics.getAngle(self.velx, self.vely)
		mag = math.sqrt(self.velx**2 + self.vely**2)
		him = physics.rotatedPoints(self.geom.getCenter(), poly, -vangle)

#   __   _  _A...............__   _  _				^
#  /  \_/ \/ \				/  \_/ \/ \				|
#  |          \				|          \	(-1, 1) | (1, 1)	
#  \       ___/	   SMEAR	\       ___/	<-------+------->	
#   |     |  				|     |		   (-1, -1) | (1, -1)
#   \     \__				\     \__				|
#    \_______\B..............\_______\				V
# 


	def getMotionSmear(self, time):
		pA, pB = None, None # see above ascii art for what points a and b are

		vangle = physics.getAngle(self.velx, self.vely)
		mag = math.sqrt(self.velx**2 + self.vely**2)
		me1 = physics.rotatedPoints(self.geom.getCenter(), self.geom.getPoints(), -vangle) # -vangle rotates to horizontal -->
		me2 = []
		for m in me1:
			me2.append((m[0]+mag*time, m[1]))


		# top-right point
		for i in range(len(me1)):
			p = me1[i]
			if pA == None or (p[0] > me1[pA][0] and p[1] > me1[pA][1]):
				pA = i

		# bottom-right point
		for i in range(len(me1)):
			p = me1[i]
			if pB == None or (p[0] > me1[pB][0] and p[1] < me1[pB][1]):
				pB = i

		smear = []

		start = pB
		if me1[pB-1][0] < me1[pB][0]:
			direction = -1
		else:
			direction = 1

		poly = me1
	 	i = start

		print "me1 len: " + str(len(me1)) + ", a: " + str(pA) + ", b: " + str(pB) + ", i: " + str(i)
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

		return physics.rotatedPoints(self.geom.getCenter(), smear, vangle)
		
		
