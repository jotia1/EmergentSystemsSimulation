import Wobject as wobject
from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 
import tools as tools
import random

class Entity(wobject.Wobject):
	DEFAULT_SIZE = 1
	DEFAULT_SPEED = 0.1
	DEFAULT_POS = (0.0, 0.0, 0.0)
	DEFAULT_COLOUR = [0.1, 0.3, 0.7]
	def __init__(self, pos=(0.0, 0.0, 0.0), size=1, \
				speed=0.1):
		""" Args: pos, size, speed
		"""
		super().__init__(size, pos)
		self.size = size
		self.speed = speed
		self.colour = self.DEFAULT_COLOUR
		self.target = None
	
	def step(self, env):
		#nearest_id_dist = env.nearest_food(self.id) # comes back as (id, dist)
		# select food to hunt from pdf?
		if not self.target or not env.lookup_food(self.target.id): # has been eaten
			self.target = None
		
		if not self.target:  #don't have a target
			foods = env.food_list(self.id)  # list of tuples
			selection = 0
			while (random.random() > 0.5 and selection < len(foods)-1):
				selection += 1
			nearest_id_dist = foods[selection]
			self.target = env.lookup_food(nearest_id_dist[0])
		
		vect_to = self.vect_from_to(self.target)
		self.velocity = [self.speed * x for x in tools.normalise(vect_to)]
		# if I have eaten a food, let it know
		if self.dist_to(self.target) < self.target.get_size():
			self.target.set_eaten()
			env.chance_born_entity()
	
	def move(self, env):
		super().move(env)
	
	def remove(self, env):
		env.remove_entity(self)
	
	def draw(self, env):
		glPushMatrix( )
		glTranslatef( *self.pos)
		glColor3f(*self.colour)
		glutSolidSphere( self.size , 30 , 30 )
		glPopMatrix( )
	
	def set_size(self, new_size):
		self.size = new_size
		
	def get_size(self):
		return self.size
		
	def set_speed(self, new_speed):
		self.speed = new_speed
	
	def get_speed(self):
		return self.speed
		
	def __repr__(self):
		return "Entity({}, {}, {}, {})".format(self.id, self.pos, self.size, self.speed)
	
def _test_all():
	""" Test various parts of the Entity to ensure it is problem free
	"""
	pass

if __name__ == "__main__":
	_test_all();