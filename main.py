#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import ipdb

start_cfg = "ddrddrdrrrdrrdrrdrrdrdrdrdrddrrdrdrdrrdddrdrdddrddrdrdrdrdrdddr"

#~ def make_vector(cfg):
	#~ vectors = []
	#~ while len(cfg) > 0:
		#~ vec = [0,0,0]
		#~ direction = cfg[0]
		#~ while cfg[0] == direction:
			#~ if direction == 1:
				#~ vec[0] -= 1
			#~ elif direction == "r":
				#~ vec[0] += 1
			#~ elif 
		#~ 

def make_matrix(cfg):
	matrix = np.zeros((64, 64), int)
	matrix[0,0] = 1
	
	i, j = 0, 0
	
	for direction in start_cfg:
		if direction == "l":
			i += 1
		elif direction == "r":
			j += 1
		
		matrix[i,j] = 1
	
	return matrix

def continue_cube(cube, start_point, directionlist, cfg):	
	#find out length of new segment:
	direction = directionlist[-1]
	length = 0
	x = cfg[0]
	while cfg[0] == x:
		length += 1
		cfg = cfg[1:]
		
	for i in xrange(1, length+1):
		#~ ipdb.set_trace()
		new_point = start_point + i*direction
		if (new_point > 3).any() or (new_point < 0).any():
			#~ print "not possible"
			#~ print directionlist
			return False
		else:
			#~ ipdb.set_trace()
			if cube[new_point[0], new_point[1], new_point[2]] == 0:
				cube[new_point[0], new_point[1], new_point[2]] = 1
			else:
				#~ print "not possible"
				#~ print directionlist
				return False
	
	if (cube == 1).all():
		print "Found solution"
		for d in directionlist:
			print d
		return True
				
	new_startpoint = start_point + length*direction

	newdirs = np.where(direction == 0)[0]
	
	for newdir in newdirs:
		for i in [-1, 1]:
			newlist = list(directionlist)
			arr = np.zeros(3, int)
			arr[newdir] = i
			newlist.append(arr)
			if continue_cube(cube, new_startpoint, newlist, cfg) == True:
				break
			#~ dirs.append(arr)
		
	
def make_cube(cfg):
	directionlist = []
	directionlist.append(np.array([1,0,0]))
	cube = np.zeros((4,4,4), int)
	
	cube[0:3,0,0] = 1
	direction = directionlist[-1]
	new_startpoint = np.array([2,0,0])
	cfg = cfg[2:]

	newdirs = np.where(direction == 0)[0]
	
	for newdir in newdirs:
		for i in [-1, 1]:
			newlist = list(directionlist)
			arr = np.zeros(3, int)
			arr[newdir] = i
			newlist.append(arr)
			print "testing", arr
			if continue_cube(cube, new_startpoint, newlist, cfg) == True:
				break
	
		
	
def find_hinges(cfg):
	pass

def main(*args):
	make_cube(start_cfg)

if __name__ == '__main__':
	main()
