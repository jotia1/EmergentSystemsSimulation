from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 

import Wobject as wobject
import random
import tools as tools

class Predator(wobject.Wobject):
	def __init__(self, pos, size, speed, colour, lifetime):
		super().__init__( size, pos)
		self.speed = speed
		self.colour = colour
		self.lifetime = lifetime
		self.cur_step = 0
		self.target = None
	
	def move(self, env):
		super().move(env)
		
	def remove(self, env):
		env.remove_predator(self)
		
	def step(self, env):
		self.cur_step += 1
		if self.cur_step > self.lifetime:
			self.set_eaten() # Then this pred has starved to death
		
		if not env.ent_list(self.id): #none left...
			return
			
		if not self.target or not env.lookup_food(self.target.id): # HAS EATEN ENTITY
			self.target = None
		
		if not self.target:  #don't have a target
			ents = env.ent_list(self.id)  # list of tuples
			selection = 0
			while (random.random() > 0.5 and selection < len(ents)-1):
				selection += 1
			nearest_id_dist = ents[selection]
			self.target = env.lookup_food(nearest_id_dist[0])
		
		vect_to = self.vect_from_to(self.target)
		self.velocity = [self.speed * x for x in tools.normalise(vect_to)]
		# if I have eaten a food, let it know
		if self.dist_to(self.target) < self.size:
			self.target.set_eaten()
			self.cur_step = 0
			self.size
		
	def draw(self, env):
		glPushMatrix( )
		glTranslatef( *self.pos)
		glColor3f(*self.colour)
		glutSolidSphere( self.size , 30 , 30 )
		glPopMatrix( )
		
	def __repr__(self):
		return "Predator({}, {}, {}, {})".format(self.id, self.pos, self.size, self.colour)