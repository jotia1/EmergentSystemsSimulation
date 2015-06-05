from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 

import math
import tools

class Wobject(object):
	ORIGIN = (0.0,0.0,0.0)
	DEFAULT_SIZE = 1
	EPSILON = 0.01
	def __init__(self, size=1, pos= (0.0,0.0,0.0)):
		""" Args: size, pos
		"""
		self.pos = pos
		self.size = size
		self.velocity = [0.0, 0.0, 0.0]
		self.eaten = False
		self.id = id(self)
		
	def set_pos(self, new_pos):
		self.pos = new_pos
		
	def get_pos(self):
		return self.pos
		
	def dist_to(self, other):
		return math.sqrt( (self.pos[0] - other.pos[0])**2 + \
				(self.pos[1] - other.pos[1])**2 + \
				(self.pos[2] - other.pos[2])**2 )
				
	def vect_from_to(self, other):
		""" Vector maths says if we do a - b we get vector pointing from b
			to a, so we want a vector point from here to other, so we need
			other - self
		"""
		return [other.pos[i] - self.pos[i] for i in range(len(self.pos))]
	
	def __repr__(self):
		return "Wobject({}, {}, {})".format(self.id, self.pos, self.size)	
		
	def set_eaten(self):
		self.eaten = True
	
	def move(self, env):
		if self.size < self.EPSILON or self.eaten:
			self.remove(env)
			return
		self.pos = tools.add(self.velocity, self.pos)
	
	def step(self, env):
		pass
	
	def draw(self, env):
		raise Exception("Wobjects draw method called. Abstract Class.")