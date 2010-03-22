import pygame
from pygame.locals import *

class AnimSprite:
	def __init__(self):
		# define self.sequences as a dictionary of AnimSequence's
		# self.sequences will contains entries like "walk left" and "jump right" and "attack up"
		# define self.current_sequence
		print "NOT IMPLEMENTED YET"

	def update(self, time):
		if self.current_sequence is not None:
			self.current_image = self.current_sequence.updateImage(self, secs_passed)

	def runSequence(seq_id):
		# set self.current_sequence to the sequence associated with the given id
		# ...

		update(self, 0) # update the current image

	def getImage(self):
		return self.current_image


class AnimSequence:
	def __init__(self, images, time):
		""" images are the individual frames, time is
			 the duration of the entire sequence in seconds """
		self.images = images
		self.__current_image_index = 0
		self.duration = time
		self.__time_ellapsed = 0
		self.loops = 0 # number of loops completed so far
	

	def currentImage(self):
		return self.image[__current_image_index]

	def nextImage(self):
		i = self.__current_image_index + 1
		if i >= len(self.images):
			i = 0
			loops += 1
		self.__current_image_index = i
		return self.images[i]

	def updateImage(self, secs_passed):
		self.__time_ellapsed += secs_passed
		frame_length = self.duration/len(self.images)

		if __time_ellapsed >= frame_length:
			__time_ellapsed -= frame_length
			self.nextImage()

		return self.currentImage()

	def restart(self):
		self.__current_image_index = 0
		self.loops = 0


def _findRect(points):
	""" Finds the rect that bounds all the given points """
	lx, ly, gx, gy = None, None, None, None
	for p in points:
		x, y = p[0], p[1]
		if lx is None or x < lx:
			lx = x
		if gx is None or x > gx:
			gx = x
		if ly is None or y < ly:
			ly = y
		if gy is None or y > gy:
			gy = y
	return (lx, ly, gx-lx, gy-ly)

class Artist:
	""" Set the color and stroke with the color (eg (0, 255, 10) ) and stroke (eg 3) attributes. """
	def __init__(self, screen, dimensions, dirty_rects):
		self.screen = screen
		self.width = dimensions[0]
		self.height = dimensions[1]
		self.color = (0, 0, 0)
		self.stroke = 1
		self.dirty_rects = dirty_rects
		self.offsetx, self.offsety = 0, 0

	def addDirtyRect(self, rect):
		dr = (rect[0]-3 + self.offsetx, rect[1]-3 + self.offsety, rect[2]+6, rect[3]+6)

		# This is here because we don't need to repaint things that are off-screen.
		if dr[0] + dr[2] < 0 or dr[1] + dr[3] < 0 or dr[0] > self.width or dr[1] > self.height:
			return
		self.dirty_rects.append(dr)


	def drawLine(self, line):
		""" line in the form ((x1, y1), (x2, y2), (x3, y3), (x4, y4)) """

		#print "stuff: " + str(line[0]) + ", " + str(line[1])
		pygame.draw.line(self.screen, self.color, (line[0][0]+self.offsetx, line[0][1]+self.offsety),
				(line[1][0]+self.offsetx, line[1][1]+self.offsety), self.stroke)

	def drawRect(self, upper_left, dimensions):
		""" draws rectangle; upper_left in (x, y), dimensions in (width, height) """
		pygame.draw.rect(self.screen, self.color, (upper_left[0]+self.offsetx, upper_left[1] + self.offsety,
			 dimensions[0], dimensions[1]), self.stroke)

	def drawOval(self, upper_left, dimensions):
		""" Draws the oval with given upper-left corner and dimensions """
		pygame.draw.ellipse(self.screen, self.color, (upper_left[0]+self.offsetx, upper_left[1]+self.offsety, 
				dimensions[0], dimensions[1]), self.stroke)

	def drawPolyPoints(self, points):
		lp = points[-1]
		for p in points:
			self.drawLine((lp, p))
			lp = p

	def drawLines(self, lines):
		""" Draws the list of lines """
		for l in lines:
			self.drawLine(l)

	def drawImage(self, image, x, y, width, height):
		# ...
		print "NOT IMPLEMENTED YET"
