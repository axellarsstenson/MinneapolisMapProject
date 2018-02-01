import turtle
import queue as Q
from random import *
import sys as sys
import ast

draw_map = True

if draw_map == True:
	window = turtle.Screen()
	window.bgcolor("darkgrey")
	window.title("Navigating Minneapolis")
	pathpen = turtle.Turtle()
	turtle.setworldcoordinates(0000, 1000, 3000, 10000)
	pathpen.color("blue")
	pathpen.pensize(1) 
	pathpen.shape("blank")
	pathpen.speed(0)
	pathpen.clearstamps()

# Define class Path()
class Path:
	def __init__(self):
		self.f_value = 0
		self.g_value = 0
		self.h_value = 0
		self.distance = 0
		self.start_node = (0, 0)
		self.end_node = (0, 0)
		self.path = []

# Define calculate_heuristic() function
def calculate_heuristic(end_node, goal_node) :

	# Returns absolute distance to goal_node from end_node
	h = ((end_node[0] - goal_node[0]) ** 2 + (end_node[1] - goal_node[1]) ** 2) ** (1/2)
	#print (h)
	return h

# Define calculate_distance() function
def calculate_distance(start_node, end_node):

	# Returns absolute distance to between start_node and end_node
	return ((start_node[0] - end_node[0]) ** 2 + (start_node[1] - end_node[1]) ** 2) ** (1/2)


def a_star_search(pathList, start_path, goal_path):
	
	pq = Q.PriorityQueue()
	close = set()
  
	start_path.g_value = 0
	start_path.f_value = start_path.h_value
	pq.put((start_path.f_value, random(), start_path))
  
	while not pq.empty():
		temp = pq.get()
		top = temp[2]
		if is_goal(goal_path, top):
			top.path.append(top)
			print ("DONE?")
			return top.path
		close.add(top)
		for next in find_succ(pathList, top):
			skip = 0
			for i in close:
				if (next.start_node == i.start_node):
					skip = 1
			if skip == 0:
				next.g_value = top.g_value + top.distance
				next.f_value = next.g_value + next.h_value
				for i in top.path:
					next.path.append(i)
				next.path.append(top)
				pq.put((next.f_value, random(), next))

	return ["Nothing"]

def bfs_search(graph, start, goal):
	q = Q.Queue()
	q.put(start)

	while not q.empty():
		temp = q.get()
		successors = find_succ(graph, temp) 
		for s in successors:
			for t in temp.path:
				if (s.start_node == t.start_node):
					successors.remove(s)
					break

		for next in successors:
			if (next.end_node == goal.start_node):
				next.path.append(next)
				return next.path
			else:
				next.path = temp.path
				next.path.append(next)
				q.put(next)
	return []


def	find_succ(pathList, top_path):
	succ_list = []
	for i in pathList:
		if (top_path.end_node == i.start_node):
			succ_list.append(i)
	return succ_list
	
	
def is_goal(goal_path, test_path):
	if (test_path.end_node == goal_path.start_node):
		return True
	else:
		return False
	
			
def main():
 
	# Init pathList
	pathList = [] 
	
	if (len(sys.argv) <= 1):
	
		with open("map_data.txt") as f:
		
			# Get start and end nodes from user
			start_node = tuple(int(x) for x in input("Enter start: x y: ").split())
			goal_node = tuple(int(x) for x in input("Enter goal: x y: ").split())

			# Max int
			start_distance = 999999999
			goal_distance = 999999999
		
			# For function finds closest nodes to entered location
			for line in f:
		
				# Iterate through f to find candidates
				n_way, x1, y1, x2, y2 = line.split(" ")
				temp_start = (int(x1), int(y1))
				temp_goal = (int(x2), int(y2))
				temp_start_distance = calculate_distance(start_node, temp_start)
				temp_goal_distance = calculate_distance(goal_node, temp_goal)
			
				# Check if distance is less than distance of best candidate
				if (temp_start_distance < start_distance) :
					candidate_start = (int(x1), int(y1))
					start_distance = temp_start_distance
				if (temp_goal_distance < goal_distance) :
					candidate_goal = (int(x2), int(y2))
					goal_distance = temp_goal_distance
				
			# Assign new start and goals to use for search
			start_node = candidate_start
			goal_node = candidate_goal
			print ("Start Node: ", start_node[0], start_node[1]) 
			print ("Goal Node: ", goal_node[0], goal_node[1])
	
	else:
			start_node = (ast.literal_eval(sys.argv[1]), ast.literal_eval(sys.argv[2]))
			goal_node = (ast.literal_eval(sys.argv[3]), ast.literal_eval(sys.argv[4]))
		
		
	hey = 0
	while (hey < 1):
		search_choice = int(input("Please enter 1 for A* search, or 2 for BFS: "))
		print(search_choice)
		if ((search_choice == 1) or (search_choice == 2)):
			hey = 1
			break
		print("Please enter only 1 or 2")	
		
	if search_choice == 1:
		print("You selected A*")
	else: 
		print("You selected BFS")
		
	with open("map_data.txt") as f:
		
		for line in f:
		
			# UI - don't draw while finding start point
			if draw_map == True:
				pathpen.penup()
		
  			# Strip () chars and break up data into chunks     
			# print (line)
			n_way, x1, y1, x2, y2 = line.split(" ")

			if draw_map == True:
				pathpen.goto(int(x1), int(y1))
				pathpen.pendown()
				pathpen.goto(int(x2), int(y2))

			# create x -> y Path
			path1Way = Path()
			path1Way.start_node = (int(x1), int(y1))
			path1Way.end_node = (int(x2), int(y2))
			path1Way.distance = calculate_distance(path1Way.start_node, path1Way.end_node)
			path1Way.h_value = calculate_heuristic(path1Way.end_node, goal_node)

			pathList.append(path1Way)
			
			# create y -> x Path
			if int(n_way) == 2:
				# print (n_way, x2, y2, x1, y1, '\n')
				path2Way = Path()
				path2Way.start_node = (int(x2), int(y2))
				path2Way.end_node = (int(x1), int(y1))
				path2Way.distance = calculate_distance(path2Way.start_node, path2Way.end_node)
				path2Way.h_value = calculate_heuristic(path2Way.end_node, goal_node)

				pathList.append(path2Way)


	if draw_map == True:
		pathpen.penup()
		pathpen.goto(int(start_node[0]), int(start_node[1]))
		pathpen.pensize(7)
		pathpen.pendown()
		pathpen.color("lightgreen")
		pathpen.forward(25)
		pathpen.forward(-25)
		pathpen.penup()
		pathpen.goto(int(goal_node[0]), int(goal_node[1]))
		pathpen.color("red")
		pathpen.pendown()
		pathpen.forward(25)
		pathpen.forward(-25)
		pathpen.penup()
		pathpen.pensize(3)
		pathpen.color("yellow")

		
	start_path = Path()
	start_path.end_node = start_node
	
	goal_path = Path()
	goal_path.start_node = goal_node
	
	if search_choice == 1:
		goal_from_search = a_star_search(pathList, start_path, goal_path)
	else :
		goal_from_search = bfs_search(pathList, start_path, goal_path)


	for route in goal_from_search:
		if draw_map == True:
			pathpen.pencolor("yellow")
			pathpen.penup()
			pathpen.goto(int(route.start_node[0]), int(route.start_node[1]))
			pathpen.pendown()
			pathpen.goto(int(route.end_node[0]), int(route.end_node[1]))

		print (route.start_node[0], route.start_node[1], route.end_node[0], route.end_node[1])

if __name__ == "__main__":
    main()
			
			
			
			
			
			
			
			
			
			
			
			
			
			