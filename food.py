
from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 
import Wobject as wobject

class Food(wobject.Wobject):
	DEFAULT_SIZE = 1
	DEFAULT_POS = (0.0, 0.0, 0.0)
	DEFAULT_COLOUR = [0.5, 0.5, 0.5]
	def __init__(self, pos=(0.0, 0.0, 0.0), size=1, colour=[0.5, 0.5, 0.5]):
		""" Args: pos, size
		"""
		super().__init__(size, pos)
		self.size = size
		self.colour = colour
		
	def draw(self, env):
		glPushMatrix( )
		glTranslatef( *self.pos)
		glColor3f(*self.colour)
		glutSolidSphere( self.size , 30 , 30 )
		glPopMatrix( )
	
	def step(self, env):
		super().step(env)
	
	def move(self, env):
		super().move(env)
		
	def remove(self, env):
		env.remove_food(self)
				
	def set_size(self, new_size):
		self.size = new_size
		
	def get_size(self):
		return self.size
		
	def __repr__(self):
		return "Food({}, {}, {}, {})".format(self.id, self.pos, self.size, self.colour)
		
	
def _test_all():
	""" Test various parts of the Entity to ensure it is problem free
	"""
	pass

if __name__ == "__main__":
	_test_all();