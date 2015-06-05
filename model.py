#
# This file is part of a submission for credit in the course COSC3000 run
# At the University of Queensland. Written by Joshua Arnold 2015.
#

import json
import random
from entity import *
from food import *
from predator import *

from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 

class Model(object):
	ENV_SIZE = "ENV_SIZE"
	NUMFOODS = "NUMFOODS"
	NUMENTITIES = "NUMENTITIES"
	NUMPREDATORS = "NUMPREDATORS"
	ENTITYSIZE = "ENTITYSIZE"
	ENTITYSPEED = "ENTITYSPEED"
	FOODSIZE = "FOODSIZE"
	WORLDSIZE = "WORLDSIZE"
	COLOURFOOD = "COLOURFOOD"
	LIGHTPOSITION = "LIGHTPOSITION"
	BORNRATE = "BORNRATE"
	PREDATORSPEED = "PREDATORSPEED"
	PREDATORSIZE ="PREDATORSIZE"
	COLOURPREDATOR = "COLOURPREDATOR"
	PREDATORLIFETIME = "PREDATORLIFETIME"
	def __init__(self):
		#self.wobjects = []
		self.entities = []
		self.foods = []
		self.predators = []
		self.config = {}
		self.dist_pred_ent = {}
		self.dist_ent_food = {}
		self.all_wobs = {}
		self.load_config()  # will raise exception killing program on fail
		self.create_life()
		self.calc_env()
		self.preds_to_add = 0
		self.ents_to_add = 0
	
	def draw(self):
		# First calculate all,
		for wob in self.get_wobjects():
			wob.step(self)
		for wob in self.get_wobjects():
			wob.move(self)
			wob.draw(self)
		self.draw_waiting()
		self.calc_env()
		
		
	def draw_waiting(self):
		while self.preds_to_add > 0:
			self.add_rand_pred()
			self.preds_to_add -= 1
		while self.ents_to_add > 0:
			self.add_rand_ent()
			self.ents_to_add -= 1
		
	def calc_env(self):
		""" Calculate all of the feautres of the environment including
			distances between wobjects
		"""
		self.dist_ent_food = self.calc_dist_ent_food()
		self.dist_pred_ent = self.calc_dist_pred_ent() #TODO function
		if len(self.foods) < self.get_option(Model.NUMFOODS):
			self.spawn_foods()
		
	def lookup_food(self, food_id):
		return self.all_wobs.get(food_id, None)	
		
	def add_predator(self, pred):
		self.predators.append(pred)
		self.all_wobs[pred.id] = pred
	
	def remove_predator(self, pred):
		self.predators.remove(pred)
		del self.all_wobs[pred.id]
	
	def add_entity(self, ent):
		self.entities.append(ent)
		self.all_wobs[ent.id] = ent
		
	def add_food(self, food):
		self.foods.append(food)
		self.all_wobs[food.id] = food 
		
	def remove_entity(self, ent):
		self.entities.remove(ent)
		del self.all_wobs[ent.id]
		
	def remove_food(self, food):
		self.foods.remove(food)
		del self.all_wobs[food.id]
		
	def queue_pred(self):
		self.preds_to_add += 1
		
	def queue_ent(self):
		self.ents_to_add += 1
		
	def add_rand_pred(self):
		pred = Predator( self.random_position(), \
						self.config[self.PREDATORSIZE], \
						self.config[self.PREDATORSPEED], \
						self.config[self.COLOURPREDATOR], \
						self.config[self.PREDATORLIFETIME])
		self.add_predator(pred)
		
	def add_rand_ent(self):
		ent = Entity(self.random_position(), \
					self.config[self.ENTITYSIZE], \
					self.config[self.ENTITYSPEED])
		self.add_entity(ent)
		
	def create_life(self):
		""" Add the entities in the configure object to the wobjects list
		"""
		# Add entities
		for i in range(self.config[self.NUMENTITIES]):
			self.add_rand_ent()
			
		for i in range(self.config[self.NUMFOODS]):
			fob = Food( self.random_position(), \
						self.config[self.FOODSIZE], \
						self.config[self.COLOURFOOD])
			self.add_food(fob)
			
		for i in range(self.config[self.NUMPREDATORS]):
			self.add_rand_pred();
	
	def chance_born_entity(self):
		""" An entity has eaten food, give it a chance to produce another
		"""
		if random.random() < self.get_option(Model.BORNRATE):
			self.add_entity(Entity(self.random_position(), \
						self.config[self.ENTITYSIZE], \
						self.config[self.ENTITYSPEED]))
	
	def ent_list(self, pred_id):
		""" Get a list of entities in order of closest to pred_id
		"""
		return self.dist_pred_ent.get(pred_id, None)
		
	def nearest_ent(self, pred_id):
		if self.ent_list:
			return self.ent_list(pred_id)[0]
		return None
	
	def food_list(self, ent_id):
		""" return a list of the food in sorted order of distance for ent_id
			List is sorted with closest first
		"""
		return self.dist_ent_food.get(ent_id, None)
		
	def nearest_food(self, ent_id):
		if self.food_list:
			return self.food_list(ent_id)[0]	
		return None													
	
	def random_position(self):
		env_size = self.config[self.ENV_SIZE]
		return tuple([(random.random() * env_size) - env_size/2 for x in range(3)])
		
	def calc_dist_ent_food(self):
		result = {}
		for ent in self.entities:
			result[ent.id] = []
			for food in self.foods:
				result[ent.id].append((food.id, ent.dist_to(food)))
			result[ent.id].sort(key=lambda tup: tup[1])
		return result
		
	def calc_dist_pred_ent(self):
		result = {}
		for pred in self.predators:
			result[pred.id] = []
			for ent in self.entities:
				result[pred.id].append((ent.id, pred.dist_to(ent)))
			result[pred.id].sort(key=lambda tup: tup[1])
		return result
			
	
	def load_config(self):
		""" Responsible for reading in configurations from a config file and 
			creating the associated environment
		"""
		# Don't error handle
		self.config = json.load(open('config.json'))
		
	def get_option(self, key):
		return self.config.get(key, None)
	
	def get_env_radius(self):
		return self.get_option(self.ENV_SIZE)/2
		
	def get_wobjects(self):
		return self.entities + self.foods + self.predators

	def add_wobject(self, new_wobject):
		raise Exception("deprecated")
		self.wobjects.append(new_wobject)
		
	def spawn_foods(self):
		""" continue to spawn food at random locations until number of foods
			equals the number loaded in at config time
		"""
		while len(self.foods) < self.get_option(Model.NUMFOODS):
			fob = Food( self.random_position(), \
						self.config[self.FOODSIZE], \
						self.config[self.COLOURFOOD])
			self.add_food(fob)
			

def _test_all():
	""" Test various parts of the model to ensure it is problem free
	"""
	pass

if __name__ == "__main__":
	_test_all();