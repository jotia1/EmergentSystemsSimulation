import math

def normalise(vect):
	mag = math.sqrt(sum([vect[i]**2 for i in range(len(vect))]))
	return [v/mag for v in vect]
	
def add(vect1, vect2):
	if len(vect1) != len(vect2):
		raise Exception("Different Length vectors")
	return [vect1[i] + vect2[i] for i in range(len(vect1))]