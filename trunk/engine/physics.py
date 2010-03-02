import math

__a_0 = 0
__a_90 = math.pi/2
__a_180 = math.pi
__a_270 = (3 * math.pi)/2
__a_360 = math.pi * 2

# in range
def __inR(angle, low, high):
	if angle < low:
			return False
	if angle > high:
		return False
	return True

def __wrapAngle(angle):
	while angle < 0:
		angle += __a_360
	while angle >= __a_360:
		angle -= __a_360
	return angle

def __flipHor(angle):
	return __wrapAngle(__a_180 - angle)
def __flipVer(angle):
	return __wrapAngle(__a_360 - angle)

# to left quadrent
def __leftQuad(angle):
	if __inR(angle, __a_90, __a_270):
		return angle
	else:
		return __flipHor(angle)

def __rightQuad(angle):
	if __inR(angle, __a_90, __a_270):
		return __flipHor(angle)	
	else:
		return angle

def __topQuad(angle):
	if __inR(angle, __a_0, __a_180):
		return angle
	else:
		return __flipVer(angle)

def __bottomQuad(angle):
	if __inR(angle, __a_180, __a_360):
		return angle
	else:
		return __flipVer(angle)

def rotatedPointAbsolute(origin, point, angle):
	""" rotatedPointAbsolute( (x,y), (x,y), theta )
 	 Returns a tuple for the coords the point would be at if	
	 it was at the given angle to the origin. In other words,	
	 it tells you where the point would be if the angle
	 was as given and the distance to the origin was the same.  """
	ox, oy, px, py = origin[0], origin[1], point[0], point[1]

	distx, disty = px - ox, py - oy

	distance = math.sqrt(distx**2 + disty**2)

	return (ox + distance * math.cos(angle), oy + distance * math.sin(angle))

def rotatedPointRelative(base_o, base_p, origin, point, angle):
	""" 	 rotatedPointAbsolute( (x,y), (x,y), theta )
		The first two arguments define the base angle. This is useful
		 if you need the location of a point attached to the end of
		another rotated vector.
		 Returns a tuple for the coords of the point after
		 rotating it by the angle (in radians). IE, it rotates
		 the point around the origin by the angle. """
	ox = origin[0]
	oy = origin[1]
	px = point[0]
	py = point[1]

	distx = px - ox
	disty = py - oy

	original_angle = getAngle(base_p[0] - base_o[0], base_p[1] - base_o[1])

	distance = math.sqrt(distx**2 + disty**2)

	new_angle = original_angle + angle
	
	return (ox + distance * math.cos(new_angle), oy + distance * math.sin(new_angle))
	

def getAngle(vectx, vecty):
	""" 	 getAngle(x, y)
		
		 Returns the angle (in radians) of 
		 the vector defined by the x, y coords """
	if vectx == 0:
		if vecty > 0:
			return __a_90
		else:
			return __a_270
	angle = __wrapAngle(math.atan(vecty/vectx))

	if vectx > 0:
		angle = __rightQuad(angle)
	elif vectx < 0:
		angle = __leftQuad(angle)

	if vecty > 0:
		angle = __topQuad(angle)
	elif vecty < 0:
		angle = __bottomQuad(angle)

	return angle


def overLine(p1, p2, p):
	slope = (p2[1]-p1[1])/(p2[0]-p1[0])
	# y = mx + b
	# b = y - mx
	b = p1[1] - slope * p1[0]
	liney = slope * p[0] + b
	return p[1] > liney

def inside_triangle(tri, c):
	p1 = tri[0]
	p2 = tri[1]
	p3 = tri[2]

	# find midpoint
	mid = ((p1[0]+p2[0]+p3[0])/3, (p1[1]+p2[1]+p3[1])/3)
	l1over = overLine(p1, p2, mid)
	l2over = overLine(p1, p3, mid)
	l3over = overLine(p2, p3, mid)
	if (l1over != overLine(p1, p2, c) or l2over != overLine(p1, p3, c) or l3over != overLine(p2, p3, c)):
		return False
	return True

def absolutize(origin, points):
	""" Converts the relative list of points to an absolute list """
	ps = []
	for p in points:
		ps.append((p[0] + origin[0], p[1] + origin[1]))
	return ps

def relativize(origin, points):
	""" Converts the absolute list of points to a list relative to the origin """
	ps = []
	for p in points:
		ps.append((p[0] - origin[0], p[1] - origin[1]))
	return ps

# is p in the bounds defined by the two points?
def inBounds(dims, p):
	left = min(dims[0][0], dims[1][0])
	right = max(dims[0][0], dims[1][0])
	up = max(dims[0][1], dims[1][1])
	down = min(dims[0][1], dims[1][1])

	x = p[0]
	y = p[1]
	if x < left or x > right or y > up or y < down:
		return False
	return True

def polygonsIntersect(poly1, poly2, threshold=1.5):
	for p in poly1:
		if inPoly(poly2, p):
			return True
	for p in poly2:
		if inPoly(poly1, p):
			return True
	return False

def contains(points, p, threshold=1.5):
	for n in points:
		if abs(n[0]-p[0]) + abs(n[1]-p[1]) < threshold * 2.0:
			return True
	return False

def inPoly(poly1, point, threshold=1.5):
	plist = []
	count = 0
	flip = False
	lastP = poly1[len(poly1)-1]
	for p in poly1:
		seg = (lastP, p)
		poi = pointOfIntersectionRay(seg, point, 0, threshold)
		if poi != None:
			if contains(plist, poi, threshold):
				plist.append(poi)
				count += 1
			else:
				count += 1
				flip = True
		lastP = p
	return count % 2 != 0

def linesIntersect(line1, line2, threshold=1.5):
	return pointOfIntersection(line1, line2, threshold) != None

def pointOfIntersectionRay(seg, raystart, rayslope, threshold=1.5):
	""" Returns the point where the line segment and the ray intersect, within the threshold, or None if they don't. """
	y1dif = seg[1][1] - seg[0][1]
	x1dif = seg[1][0] - seg[0][0]

	if x1dif == 0:
		m1 = None
	else:
		m1 = y1dif/x1dif # rise over run

	m2 = rayslope

	b1, b2 = None, None

	if m1 != None:
		b1 = seg[0][1] - m1*seg[0][0]
	if m2 != None:
		b2 = raystart[1] - m2*raystart[0]

	if m1 == None and m2 == None:
		if abs(line1[0][0] - line2[0][0]) < threshold:
			return (seg[0][0] + seg[1][0] + raystart[0])/3.0
		else:
			return None

	if m1 == None:
		px = (seg[0][0] + seg[1][0])/2.0
	elif m2 == None:
		px = raystart[0]
	elif m1 == m2:
		if abs(b1-b2) < threshold and raystart[0] - threshold <= min(seg[0][0], seg[1][1]):
			return raystart
		else:
			return None
	else:
		px = (b2-b1)/(m1-m2)

	py1, py2 = None, None

	if m1 != None:
		py1 = px*m1+b1
	if m2 != None:
		py2 = px*m2+b2

	if py1 is None:
		py1 = py2
	elif py2 is None:
		py2 = py1

	off = abs( py2 - py1 )

	if off > threshold: # arbitrary threshhold
		return None

	if not inBounds(seg, (px, py1)):
		return None
	if px < raystart[0]-threshold:
		return None
	
	return (px, (py1+py2)/2)

		

def pointOfIntersection(line1, line2, threshold=1.5):
	""" Returns the point where line1 and line2 intersect (within the threshold, default 1.5). Returns None
		if these line segments do not intersect. """
	y1dif = line1[1][1] - line1[0][1]
	x1dif = line1[1][0] - line1[0][0]

	y2dif = line2[1][1] - line2[0][1]
	x2dif = line2[1][0] - line2[0][0]

	if x1dif == 0:
		m1 = None
	else:
		m1 = y1dif/x1dif # rise over run
	if x2dif == 0:
		m2 = None
	else:
		m2 = y2dif/x2dif # same for line 2

	b1, b2 = None, None

	if m1 != None:
		b1 = line1[0][1] - m1*line1[0][0] # b = y - mx
	if m2 != None:
		b2 = line2[0][1] - m2*line2[0][0]

	if m1 == None and m2 == None:
		if abs(line1[0][0] - line2[0][0]) < threshold:
			return ((line1[0][0]+line2[0][0])/2.0, (line1[0][1] + line1[1][1] + line2[0][1] + line2[1][1])/4.0)
		else:
			return None

	if m1 == None:
		px = (line1[0][0] + line1[1][0])/2
	elif m2 == None:
		px = (line2[0][0] + line2[1][0])/2
	elif m1 == m2:
		al = min(line1[0][0], line1[1][0])
		ar = max(line1[0][0], line1[1][0])
		bl = min(line2[0][0], line2[1][0])
		br = max(line2[0][0], line2[1][0])
		if al - threshold < br and al + threshold > bl:
			return True
		if ar - threshold < br and ar + threshold > bl:
			return True
		return False
	else:
		px = (b2-b1)/(m1-m2)

	py1, py2 = None, None

	if m1 != None:
		py1 = px*m1+b1
	if m2 != None:
		py2 = px*m2+b2

	if py1 == None:
		py1 = py2
	elif py2 == None:
		py2 = py1

	off = abs( py2 - py1 )

	if off > threshold: # arbitrary threshhold
		return None

	if not inBounds(line1, (px, py1)):
		return None
	if not inBounds(line2, (px, py2)):
		return None
	
	return (px, (py1+py2)/2)


def rotatedPoints(center, points, angle, absolute=False):
	""" returns a new list of points rotated around the given center by angle """
	ps = points
	nps = []
	for p in ps:
		if absolute:
			nps.append(rotatedPointAbsolute(center, p, angle))
		else:
			nps.append(rotatedPointRelative(center, p, center, p, angle))
	return nps


def createPoly(points):
	# set center to average ...
	# relativize points ...
	# init RotPoly ...
	# return RotPoly ...
	return None

class RotPoly:
	def __init__(self, center, points, rotation):
		self.__pointmatrix = []
		self.angle = rotation
		self.centerx = center[0]
		self.centery = center[1]
		for p in points:
			self.__pointmatrix.append(p)

	def getPoints(self):
		cent = (self.centerx, self.centery)
		ap = absolutize(cent, self.__pointmatrix)
		ps = []
		for p in ap:
			ps.append(rotatedPointRelative(cent, p, cent, p, self.angle))
		return ps

	def intersects(self, other):
		""" other should be another RotPoly instance """
		if polygonsIntersect(self.getPoints(), other.getPoints()):
			return True
		mylines = self.getLines()
		hislines = other.getLines()
		for m in mylines:
			for h in hislines:
				if linesIntersect(m, h):
					return True
		return False

	def getLines(self):
		lines = []
		points = self.getPoints()
		lp = points[len(points)-1]
		for p in points:
			lines.append((lp, p))
			lp = p
		return lines

	def getCenter(self):
		return (self.centerx, self.centery)

	def left(self):
		l = None
		ps = self.getPoints()
		for p in ps:
			if p[0] < l or l is None:
				l = p[0]
		return l

	def right(self):
		l = None
		ps = self.getPoints()
		for p in ps:
			if p[0] > l or l is None:
				l = p[0]
		return l

	def top(self):
		l = None
		ps = self.getPoints()
		for p in ps:
			if p[1] < l or l is None:
				l = p[1]
		return l


	def bottom(self):
		l = None
		ps = self.getPoints()
		for p in ps:
			if p[1] > l or l is None:
				l = p[1]
		return l

	def boundingRect(self):
		l = self.left()
		r = self.right()
		t = self.top()
		b = self.bottom()
		return (l, t, r-l, b-t)

class RotRect(RotPoly):

	def __init__(self, x, y, width, height, rotation):
		RotPoly.__init__(self, (x + width/2.0, y + height/2.0),
			 ( (-width/2.0, height/2.0), 
				(width/2.0, height/2.0), 
				(width/2.0, -height/2.0),
				(-width/2.0, -height/2.0) ), rotation)

	def moveCenterTo(self,x,y):
		self.centerx = x
		self.centery = y
