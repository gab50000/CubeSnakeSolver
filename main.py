#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import ipdb

start_cfg = "ddrddrdrrrdrrdrrdrrdrdrdrdrddrrdrdrdrrdddrdrdddrddrdrdrdrdrdddr"
COUNTER = 0

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
        global COUNTER
	#find out length of new segment:
	direction = directionlist[-1]
	length = 0
	
	if len(cfg) == 0:
		return False
	x = cfg[0]
	while cfg[0] == x:
		length += 1
		cfg = cfg[1:]
		if len(cfg) == 0:
			break
		
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
	
        if COUNTER % 100 == 0:
            print "sum {:2d}, counter: {:10d}".format(cube.sum(), COUNTER), "\r",
        COUNTER += 1
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
			newcube = np.copy(cube)
			arr = np.zeros(3, int)
			arr[newdir] = i
			newlist.append(arr)
			if continue_cube(newcube, new_startpoint, newlist, cfg) == True:
				return True
	return False
			#~ dirs.append(arr)

		
	
def make_cube(cfg):
	directionlist = []
	directionlist.append(np.array([1,0,0]))
	
	#find startconfig
	for x in xrange(4):
		for y in xrange(4):
			for z in xrange(4):
				if x+2 < 4:
					cube = np.zeros((4,4,4), int)
					startpoint = np.array((x,y,z), int)
					print "startpoint", startpoint
					
					for i in xrange(3):
						cube[startpoint[0]+i, startpoint[1], startpoint[2]] = 1
					direction = directionlist[-1]
					new_startpoint = startpoint + (2,0,0)
					cfg = cfg[2:]

					newdirs = np.where(direction == 0)[0]
					
					for newdir in newdirs:
						for i in [-1, 1]:
							newlist = list(directionlist)
							arr = np.zeros(3, int)
							arr[newdir] = i
							newlist.append(arr)
							newcube = np.copy(cube)
							print "testing", arr
							if continue_cube(newcube, new_startpoint, newlist, cfg) == True:
								print "startpoint for solution", startpoint
								break
		
def find_hinges(cfg):
	pass

def main(*args):
	make_cube(start_cfg)

if __name__ == '__main__':
	main()
