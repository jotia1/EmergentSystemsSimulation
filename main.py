#import OpenGL
#OpenGL.ERROR_LOGGING = False # Turns off debugging log to increase speed
from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import *  

import time # for waiting

# Project imports
from model import *
from math import *
from PIL import Image
import numpy as np

class Controller(object):
	""" A high-level class used to start and control the Computer Graphics
		project.
	"""
	WINDOW_WIDTH = 640
	WINDOW_HEIGHT = 480
	def __init__(self):
		
		glutInit( "" )
		glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH )
		glutInitWindowSize( self.WINDOW_WIDTH, self.WINDOW_HEIGHT )
		glutInitWindowPosition( 0, 0 )
		
		self.hWindow = glutCreateWindow( b"Populations Simulation" )
		
		glutDisplayFunc( self.drawGLScene )
		glutIdleFunc( self.drawGLScene )
		
		glutReshapeFunc( self.resizeGLScene )
		
		glutKeyboardFunc( self.keyPressed )
		
		self.initGL( self.WINDOW_WIDTH, self.WINDOW_HEIGHT )
		
		self.model = Model()
		
		self.camRange = 20
		self.camPhi = 10
		self.camTheta = 0
		self.lightr = self.model.get_option(Model.ENV_SIZE)*2
		#print(self.model.get_option(Model.ENV_SIZE*2))
		self.lighttheta = 0.1
		self.lightz = self.model.get_option(Model.ENV_SIZE)*2
		
		self.print_instructions()
		glutMainLoop( )  #Start everything

	def drawGLScene(self):
		""" Callback when a scene needs drawing
		"""
		# clear the screen and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		glLoadIdentity( )
		
		self.ground_plane()
		self.position_camera()
		self.position_light()
		
		glTranslatef( 0.0, 0.0, 0.0 )  # may need to go further
		
		glPushMatrix( )
		
		self.draw_world_edge( )
		glPushMatrix()
		
		glEnable(GL_LIGHTING)
		self.model.draw( )  # Render the environment
		glDisable(GL_LIGHTING)
		glPopMatrix()
		"""
		# Colour and draw a sphere
		glColor3f(1.0,0.0,0.0)
		glutSolidSphere( 1 , 30 , 30 )
		"""
		
		glPopMatrix( )
		
		glutSwapBuffers( )		
		time.sleep(0.01)
		
	def ground_plane(self):
		glBegin(GL_QUADS);
		glColor3f(0.0,1.0,0.0)
		glVertex4f(-1, -1, 0, 0);
		glVertex4f(-1, 1, 0, 0);
		glVertex4f(1, 1, 0, 0);
		glVertex4f(1, -1, 0, 0);
		glEnd();
	
	def draw_world_edge(self):
		""" Draw whatever is going to be the edge of the environment
		"""
		world_size = self.model.get_option( Model.WORLDSIZE ) # single value, world must be square
		# For now draw a wire box
		glPushMatrix()
		glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
		glColor3f(1.0,0.0,0.0)  # Colour worlds edge red
		
		glutSolidCube( world_size )  #Cube of size world
		glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )  # set back
		
		#Texturing
		glassTex = Image.open( "texture_wood.bmp" )
		
		# create textures
		glassTexID = glGenTextures( 1 )
		gnp = np.array(glassTex)
		
		# just use linear filtering
		glBindTexture( GL_TEXTURE_2D, glassTexID )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
		glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, glassTex.size[0], glassTex.size[1], 0, GL_RGB,
				GL_UNSIGNED_BYTE, gnp.ctypes.data_as(ctypes.POINTER(ctypes.c_short)) )
		
		
		
		glEnable(GL_BLEND);		
		glBindTexture( GL_TEXTURE_2D, glassTexID )
		
		glTranslatef( -0.5, -0.5, 0 )
		
		glBegin( GL_QUADS )
        glTexCoord2f( 0, 0.075 ); glVertex3f( 0, 0, 0 )
        glTexCoord2f( 0.075, 0.075 ); glVertex3f( 0, 0, -0.1 )
        glTexCoord2f( 0.075, 0.925 ); glVertex3f( 0, 1, -0.1 )
        glTexCoord2f( 0, 0.925 ); glVertex3f( 0, 1, 0 )
		glEnd( )
		glDisable(GL_BLEND);
		
		
		
		glPopMatrix()

	def keyPressed(self, key, x, y):
		key = ord(key)
		
		if key == 27:
			self.close_simulation()
		elif key == ord( 'S' ) or key == ord( 's' ):
		    self.camPhi -= 3
		    if self.camPhi < -90:
		        self.camPhi = -90  #Limit  
		elif key == ord( 'W' ) or key == ord( 'w' ):
		    self.camPhi += 3
		    if self.camPhi > 90:
		        self.camPhi = 90   #Limit 
		elif key == ord( 'A' ) or key == ord( 'a' ):
		    self.camTheta -= 3
		    if self.camTheta < 0:
		        self.camTheta += 360   #Modulus
		elif key == ord( 'D' ) or key == ord( 'd' ):
		    self.camTheta += 3
		    if self.camTheta > 360:
		        self.camTheta -= 360   #Modulus
		elif key == ord( 'E' ) or key == ord( 'e' ):
		    self.camRange -= 1
		elif key == ord( 'Q' ) or key == ord( 'q' ):
		    self.camRange += 1
		elif key == ord( 'n' ) or key == ord( 'N' ):
			self.model.queue_ent()
		elif key == ord( 'm' ) or key == ord( 'M' ):
			self.model.queue_pred()
				

	def resizeGLScene(self, width, height):
		""" Callback for when resize is needed
		"""
		# prevent a divide-by-zero error if the window is too small
		if height == 0:
			height = 1
		
		# reset the current viewport and recalculate the perspective transformation
		# for the projection matrix
		glViewport( 0, 0, width, height )
		glMatrixMode( GL_PROJECTION )
		glLoadIdentity( )
		gluPerspective( 45.0, float( width )/float( height ), 0.1, 100.0 )
		
		# return to the modelview matrix mode
		glMatrixMode( GL_MODELVIEW )
	
	def position_camera(self):
		#--**Camera Code**--------------------------------------------------
		r_xz = self.camRange*cos(self.camPhi*pi/180)
		x = r_xz*sin(self.camTheta*pi/180)
		y = self.camRange*sin(self.camPhi*pi/180)
		z = r_xz*cos(self.camTheta*pi/180)
		
		gluLookAt(x,y,z,    # Eye point
			0,0,0,    # Center of view
			0,1,0,    # 'Up vector'
		)
	
	def initGL(self, nWidth, nHeight):
		# use black when clearing the colour buffers -- this will give us a black
		# background for the window
		glClearColor( 1.0, 1.0, 1.0, 0.0 )
		# enable the depth buffer to be cleared
		glClearDepth( 1.0 )
		# set which type of depth test to use
		glDepthFunc( GL_LESS )
		# enable depth testing
		glEnable( GL_DEPTH_TEST )
		# enable smooth colour shading
		glShadeModel( GL_SMOOTH )
		glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
		# enable lighting of materials
		glEnable(GL_COLOR_MATERIAL)
		
		self.resizeGLScene( nWidth, nHeight )

	def position_light(self):
		glPushMatrix() #Push Stack matrix down by one
		#Make Sphere Yellow
		glColor3f(1.0,1.0,0.0)
		x = self.lightr * sin(self.lighttheta)
		y = self.lightr * cos(self.lighttheta)
		z = self.lightz
		self.lighttheta += 0.003
		
		glLightfv( GL_LIGHT0, GL_DIFFUSE, GLfloat_3(1,1,1) )
		glLightfv( GL_LIGHT0, GL_AMBIENT, GLfloat_3(0,0,0) )
		glLightfv( GL_LIGHT0, GL_SPECULAR, GLfloat_3(1,1,1) )
		glLightfv( GL_LIGHT0, GL_POSITION, GLfloat_4(x,y,z,1) )
		glEnable( GL_LIGHT0)
		
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		
		#Position Sphere
		glTranslatef( x, y, z)
		
		#Generate Sphere
		glutSolidSphere( 0.125 , 30 , 30 )
		
		glPopMatrix()

	def close_simulation(self):
		""" Method for ending the simulation
		"""
		if self.hWindow:
			glutDestroyWindow( self.hWindow )
		sys.exit( )
		
	def print_instructions(self):
		print("Controls\n\n\
			Esc - Exit the program\n\
			A-D - Camera: Rotate around object (theta)\n\
			W-S - Camera: Rotate around object (phi)\n\
			Q-E - Camera: Zoom\n\
			N - Add another Entity\n\
			M - Add another Predator\n\
			")

if __name__ == "__main__":
	Controller();