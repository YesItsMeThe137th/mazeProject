import random
import pygame
import pygame_gui

#source venv/bin/activate
#to leave venv, type deactivate
#ignore squigglies on pygame_gui
class DisjointSet:
	def __init__(self, nodes):
		self.parent = {}
	
		for node in nodes:
			self.parent[node] = node

	def find(self, node):
		if self.parent[node] != node:
			self.parent[node] = self.find(self.parent[node])
		return self.parent[node]

	def union(self, n1, n2):
		r1 = self.find(n1)
		r2 = self.find(n2)
		self.parent[r1] = r2

class Tile:
	def __init__(self, x, y, size):
		self.x = x
		self.y = y
		self.size = size
		self.wx = x * size
		self.wy = y * size
		self.iteration = 0
		self.process = 0

		self.connected = {
			(-1,  0) : False,
			( 1,  0) : False,
			( 0, -1) : False,
			( 0,  1) : False
		}

		self.color = (0, 0, 0)

	def __hash__(self):
		return hash((self.x, self.y))
	
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return NotImplemented
		return self.x == other.x and self.y == other.y

	def __repr__(self):
		return f"({self.x}, {self.y})"
	
	def draw(self, screen):
		for x, y in self.connected:
			if not self.connected[(x, y)]:
				pygame.draw.line(
					screen,
					self.color,
					{
						(-1, 0) : (self.wx            , self.wy),
						( 1, 0) : (self.wx + self.size, self.wy),
						(0, -1) : (self.wx            , self.wy),
						(0,  1) : (self.wx            , self.wy + self.size) 
					}[(x, y)],
					{
						(-1, 0) : (self.wx            , self.wy + self.size),
						( 1, 0) : (self.wx + self.size, self.wy + self.size),
						(0, -1) : (self.wx + self.size, self.wy),
						(0,  1) : (self.wx + self.size, self.wy + self.size)
					}[(x, y)],
					1
				)

class Maze:

	def __init__(self, width, height, size):
		self.width = width
		self.height = height
		self.tile_size = size
		self.grid = [[Tile(x, y, self.tile_size) for x in range(self.width)] for y in range(self.height)]
		self.startTile = self.grid[0][0]
		self.endTile = self.grid[width - 1][height - 1]


	def draw(self, screen):
		for row in self.grid:
			for tile in row:
				tile.draw(screen)


	#THIS IS KRUSKALS
	def generate(self):
		self.grid = [[Tile(x, y, self.tile_size) for x in range(self.width)] for y in range(self.height)]
		self.startTile = self.grid[0][0]
		self.endTile = self.grid[self.width - 1][self.height - 1]
		edges = []
		for y, row in enumerate(self.grid):
			for x, tile in enumerate(row):
				for dx, dy in self.neighbors(x, y):
					edges.append((x, y, dx, dy))
		
		random.shuffle(edges)

		ds = DisjointSet([(x, y) for x in range(self.width) for y in range(self.height)])

		for x, y, dx, dy in edges:
			if ds.find((x, y)) != ds.find((x + dx, y + dy)):
				self.grid[y][x].connected[(dx, dy)] = True				
				self.grid[y + dy][x + dx].connected[(dx * -1, dy * -1)] = True
				ds.union((x, y), (x + dx, y + dy))

	#Utilities
	def neighbors(self, x, y):
		return [(dx, dy) for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
				if 0 <= x + dx < self.width and 0 <= y + dy < self.height
		]

"""
MOST IMPORTANT: DFS, BFS
depth first search (dfs)
	fundamental searching algorithm
	"left hand search algorithm" is a variation of this (1 line of code away in some cases)
	looks like a snake that sometimes grows more heads
	goes to the end of one path and then the next path, etc.
	

breath first search (bfs)
	fundamental searching algorithm
	opposite of dfs
	looks like you're pouring water in a maze
	follows all paths that have been reached at an equal pace
		covers every possible spot at an increasing
	

djikstra's algorithm ("dextra's")
	variation of BFS

dead-end filling
	Only a computer can do this one

"""


class MazeSolver():
	def __init__(self, maze):
		self.winningPath = []
		self.size = maze.tile_size
		self.timeSinceSolve = 0
		self.stack = [(0, 0, 0, 0)]
		self.visited = {}
		self.solved = False
		self.totalIterations = 1
		self.maze = maze
		#self.visited = []
		
		#self.winningPath = self.DFS((0, 0, 0, 0), maze)
	"""
	Do a check to see if this is the end tile
	If not, check only the connected tiles at (-1, 0), (0, -1), (1, 0), (0, 1) but not the tile that was just passed in
	With each tile checked, pass in the movement required to get here (ie, (-1, 0), (-1, 0), (0, -1), (1, 0), (0, 1))
	When we reach the final tile, we append the movement we just made and return. 
		Then we repeat this process for each step in the recursive algorithm so far.
	"""
	"""def DFS(self, coords, maze):
		# coords goes myX myY pX pY
		# This is for checking if it is the end tile
		winning = []
		# print(self.foundWin)
		if(maze.grid[coords[0]][coords[1]] == maze.endTile): # maybe not exist?
			print("Found Win")
			winning = coords
		else:
			#print("a")
		
			#print("b")
			viable = self.getValidNeighbors(maze, coords)
			#print(viable)
			# add in a check to see if there is an edge between the two sides
			for item in viable:
				#print("c")
				if (item[0] >= 0 and item[1] >= 0):
					if (item[0] < len(maze.grid) + 1 and item[1] < len(maze.grid[0]) + 1):
						newCoords = (item[0], item[1], coords[0], coords[1])
						print(newCoords)
						self.DFS(newCoords, maze)
						if maze.endTile in self.visited:
							return winning
						#print(coords[0], coords[1])
		return winning"""


	def DFS(self, maze):
		while self.stack:
			x, y, px, py = self.stack.pop(len(self.stack) - 1)
			self.visited[(x, y)] = (px, py)
			maze.grid[y][x].process = self.totalIterations
			if (maze.grid[y][x] == maze.endTile):
				# set stack to nothing
				self.stack = []
				# calculate path (with function)
				self.winningPath = self.calcPath(x, y)
				# return nothing
				self.timeSinceSolve = 0
				self.solved = True
				return
			viable = self.getValidNeighbors(maze, x, y)
			for x2, y2 in viable:
				self.stack.append((x2, y2, x, y))
			self.totalIterations += 1
	

	def BFS(self, maze):
		while self.stack:
			x, y, px, py = self.stack.pop(0)
			
			self.visited[(x, y)] = (px, py)
			maze.grid[y][x].process = self.totalIterations
			if (maze.grid[y][x] == maze.endTile):
				# set stack to nothing
				self.stack = []
				# calculate path (with function)
				self.winningPath = self.calcPath( x, y)
				# return nothing
				self.timeSinceSolve = 0
				self.solved = True
				return
			viable = self.getValidNeighbors(maze, x, y)
			for x2, y2 in viable:
				self.stack.append((x2, y2, x, y))
			self.totalIterations += 1

	def calcLikelihood(self, node):
		manhattan = self.getManhattan(self.maze, node[0], node[1])
		iteration = self.maze.grid[node[1]][node[0]].iteration
		iteration = 0
		heuristic = manhattan + iteration
		print(iteration, manhattan)

		# iteration rises over the course of the project, 
		
		return heuristic

	def getNextPoint(self):
		# sort the list based on manhatten distance
		# pop out the first thing and return it from the distorted list 
		
		# key=lambda node : abs(maze.endTile.x - node[0]) + abs(maze.endTile.y - node[1])
		self.stack.sort(key=self.calcLikelihood)
		return self.stack.pop(0)

	def getManhattan(self, maze, x, y):
		xd = abs(maze.endTile.x - x)
		yd = abs(maze.endTile.y - y)
		return xd + yd

	def djikstras(self, maze):
		while self.stack:
			x, y, px, py = self.getNextPoint()
			self.visited[(x, y)] = (px, py)
			print(self.totalIterations)
			maze.grid[y][x].process = self.totalIterations
			self.totalIterations += 1
			if (maze.grid[y][x] == maze.endTile):
				# set stack to nothing
				self.stack = []
				# calculate path (with function)
				self.winningPath = self.calcPath(x, y)
				# return nothing
				self.timeSinceSolve = 0
				self.solved = True
				return
			viable = self.getValidNeighbors(maze, x, y)
			for x2, y2 in viable:
				maze.grid[y2][x2].iteration = maze.grid[y][x].iteration + 1
				self.stack.append((x2, y2, x, y))
			
	def deadEnd_init(self):
		queue = []
		print("Point A Reached")
		for row in self.maze.grid:
			for tile in row:
				connections = 0
				for item in (self.getGood(tile)):
					if tile.connected[item]:
						connections += 1
				if connections < 2:
					queue.insert(0, tile)
		print("Point B Reached")
		for x in range(len(queue) - 1, -1, -1):
			if queue[x] == self.maze.startTile or queue[x] == self.maze.endTile:
				queue.pop(x)
		print("Point C Reached")
		return queue

	def deadEndFill(self):
		# assumption: True means that there is no wall
		queue = self.deadEnd_init()
		# print(type(queue[0]))
		# print(queue[0])
		self.timeSinceSolve = 0
		while queue:
			item = queue.pop()
			self.maze.grid[item.y][item.x].process = self.totalIterations
			self.totalIterations += 1
			self.visited[(item.x, item.y)] = (item.x, item.y)
			connections = 0
			for tile in (self.getGood(item)):
				if item.connected[tile]:
					print(tile)
					newTile = self.maze.grid[tile[0]][tile[1]]
					for otherTile in (self.getGood(newTile)):
						if newTile.connected[otherTile]:
							print(otherTile)
							if (newTile.connected[otherTile]):
								connections += 1
							if connections < 2:
								queue.insert(0, tile)
					# find connected tiles and just check whether or not they are already dead ends
		#print(queue)
		# while queue:
		# 	tile = queue.pop(0)
		# 	for item in (self.getGood(tile)): # this needs fixing right here
		# 		if tile.connected[item]:
		# 			newTile = self.maze.grid[tile.x + item[0]][tile.y + item[1]]
		# 			newTile.connected[(item[0] * -1, item[1] * -1)] = False

		# 			connections = 0
		# 			for newItem in ((0,1), (0,-1), (1,0), (-1, 0)):
		# 				if newTile.connected[newItem]:
		# 					connections += 1
		# 			if connections < 2:
		# 				queue.append(newTile)
		self.solved = True
			
	def getGood(self, tile):
		possible = [(0,1), (0,-1), (1,0), (-1, 0)]
		for i in range(len(possible) - 1, -1, -1):
			if possible[i][0] + tile.x > self.maze.width:
				possible.pop(i)
			elif possible[i][0] + tile.x < 0:
				possible.pop(i)					
			elif possible[i][1] + tile.y > self.maze.height:
				possible.pop(i)
			elif possible[i][1] + tile.y < 0:
				possible.pop(i)

		return possible

		"""
		Pre set up a list/set
		
		
		"""


		"""
		We put all of our tiles in one big set
		We do the same here, but
		We loop through the set
		
		
		"""
		
		
		
		
		#Create boolean FoundSolution = True
		#for loop to check each row, each tile in each row
		# for each tile, if tiles has less than 2 connections
		#  wall off the current tile and signify on the tile's connected piece that that wall is now a wall
		#  FoundSolution = False
		#if FoundSolution:
		# this.solved = True



	'''
	Excluding the start and the end, we find all dead ends
		A dead end is defined as a cell with three surrounding walls	
	Fill in all identified dead cells
		You can say that there is a wall there...
	Once that's done, this whole thing loops.
	
	'''

	def djikstras_iter(self, maze):
		if self.stack:
			x, y, px, py = self.getNextPoint() # this is the line where we access the current iteration
			self.visited[(x, y)] = (px, py)
			maze.grid[y][x].process = self.totalIterations
			self.totalIterations += 1
			if (maze.grid[y][x] == maze.endTile):
				# set stack to nothing
				self.stack = []
				# calculate path (with function)
				self.winningPath = self.calcPath(x, y)
				# return nothing
				self.timeSinceSolve = 0
				self.solved = True
				return
			viable = self.getValidNeighbors(maze, x, y)
			for x2, y2 in viable:
				maze.grid[y2][x2].iteration = maze.grid[y][x].iteration + 1 # this is the line where we set the current iteration
				self.stack.append((x2, y2, x, y))

	def DFS_iter(self, maze):
		if self.stack:
			x, y, px, py = self.stack.pop(len(self.stack) - 1)
			self.visited[(x, y)] = (px, py)
			maze.grid[y][x].process = self.totalIterations
			if (maze.grid[y][x] == maze.endTile):
				# set stack to nothing
				self.stack = []
				# calculate path (with function)
				self.winningPath = self.calcPath(x, y)
				# return nothing
				self.timeSinceSolve = 0
				self.solved = True
				return
			viable = self.getValidNeighbors(maze, x, y)
			for x2, y2 in viable:
				self.stack.append((x2, y2, x, y))
			self.totalIterations += 1
	

	def BFS_iter(self, maze):
		if self.stack:
			x, y, px, py = self.stack.pop(0)
			
			self.visited[(x, y)] = (px, py)
			maze.grid[y][x].process = self.totalIterations
			if (maze.grid[y][x] == maze.endTile):
				# set stack to nothing
				self.stack = []
				# calculate path (with function)
				self.winningPath = self.calcPath(x, y)
				# return nothing
				self.timeSinceSolve = 0
				self.solved = True
				return
			viable = self.getValidNeighbors(maze, x, y)
			for x2, y2 in viable:
				self.stack.append((x2, y2, x, y))
			self.totalIterations += 1



	def calcPath(self,  x, y):
		path = []
		while self.visited[(x, y)] != (x, y):
			path.append((x, y))
			x, y = self.visited[x, y]
		path.append((x, y))
		path.reverse()
		return path



	def getValidNeighbors(self, maze, x, y):
		valid = [(-1, 0), (0, -1), (1, 0), (0, 1)]
		answer = []
		for dx, dy in valid:
			if maze.grid[y][x].connected[(dx, dy)]:
				new = (dx + x, dy + y)
				if new not in self.visited:
					answer.append(new)
		return answer


	def draw_path(self, maze_surface, toggle):
		if toggle:
			color = (20, 255, 20)
		else:
			color = (100, 255, 100)

		for x, y in self.winningPath:
			rect = pygame.rect.Rect(x * self.size + self.size / 6, y * self.size + self.size / 6, self.size - self.size / 3, self.size - self.size / 3)
			pygame.draw.rect(maze_surface, color, rect, int(self.size / 3))

	def draw_other(self, maze_surface, maze):
		# print(self.visited)
		for x, y in self.visited.keys():
			color = self.getColor(maze.grid[y][x])
			# print(color)
			rect = pygame.rect.Rect(x * self.size + self.size / 6, y * self.size + self.size / 6, self.size - self.size / 3, self.size - self.size / 3)
			pygame.draw.rect(maze_surface, color, rect, int(self.size / 3))
			# WHAT WE WANT:
			# How late in the process this tile was reached with a color gradient
			# 2-color gradient moving inbetween Original and End colors
	
	def getColor(self, tile):
		iter = tile.process
		color1 = (56, 9, 107)
		color2 = (255, 20, 20)
		percent = iter / self.totalIterations
		# print(iter, " ", self.totalIterations)
		r = color2[0] + ((color1[0]-color2[0]) * percent)
		g = color2[1] + ((color1[1]-color2[1]) * percent)
		b = color2[2] + ((color1[2]-color2[2]) * percent)
		#print (percent, (r, g, b))
		return (r, g, b)


def main():

	#Setup
	screen_width  = 1440
	screen_height = 870

	pygame.init()

	screen = pygame.display.set_mode([screen_width, screen_height])
	
	#UI
	ui_manager = pygame_gui.UIManager((200, 800))
	generate_button = pygame_gui.elements.UIButton(
		relative_rect=pygame.Rect((40, 50), (120, 50)),
		text="Generate",
		manager=ui_manager
	)
	toggle = pygame_gui.elements.UIDropDownMenu(
		options_list = ["BFS", "DFS", "Djikstra's", "Dead-End Fill"],
		expansion_height_limit = 1000,
		starting_option = "Dead-End Fill",
		relative_rect=pygame.Rect((40, 110), (120, 50)),
		manager=ui_manager
	)
	iter_toggle = pygame_gui.elements.UIButton(
		relative_rect=pygame.Rect((40, 170), (120, 50)),
		text="Pop the Hood",
		manager=ui_manager
	)

	#Maze
	maze_surface = pygame.Surface((870, 870), pygame.SRCALPHA)
	w = 24
	l = 24




	maze = Maze(w, l, 860 / w)
	maze.generate()
	mazeSolver = MazeSolver(maze)
	# winning = mazeSolver.BFS(maze)
	print(mazeSolver.winningPath)
	#Clock
	clock = pygame.time.Clock()

	# coords = [1, 1, 1, 0]
	# viable = mazeSolver.getValidNeighbors(maze, coords)
	# print(viable)
	#Event Loop
	running = True
	iterMode = False
	mode = "BFS" #Dead-End Fill
	# True: DFS
	# False: BFS
	while running:
		delta_time = clock.tick(240)/1000.0
		mazeSolver.timeSinceSolve += delta_time
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame_gui.UI_BUTTON_PRESSED:
				if event.ui_element == generate_button:
					maze.generate()
					mazeSolver = MazeSolver(maze)
				if event.ui_element == iter_toggle:
					iterMode = not iterMode
					maze.solved = False
					mazeSolver = MazeSolver(maze)
			if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
				if event.ui_element == toggle:
					mode = event.text 
					if not iterMode:
						mazeSolver = MazeSolver(maze)
			ui_manager.process_events(event)
		
		'''
		Change DBFS toggle
		
		'''




		if iterMode:
			if mode == "DFS":
				mazeSolver.DFS_iter(maze)
				mazeSolver.draw_other(maze_surface, maze)
				# print("DFS_iter!")
				# print(mazeSolver.stack)
			elif mode == "Djikstra's":
				mazeSolver.djikstras_iter(maze)
				mazeSolver.draw_other(maze_surface, maze)
			
			else: 
				mazeSolver.BFS_iter(maze)
				mazeSolver.draw_other(maze_surface, maze)
				# print("BFS_iter!")
		else: 
			if mode == "BFS":
				if not mazeSolver.solved:
					mazeSolver.BFS(maze)
			elif mode == "Djikstra's":
				if not mazeSolver.solved:
					mazeSolver.djikstras(maze)
			elif mode == "Dead-End Fill":
				if not mazeSolver.solved:
					print("DeadEnd")
					mazeSolver.deadEndFill()
			else: 
				if not mazeSolver.solved:
					mazeSolver.DFS(maze)
			

		

		ui_manager.update(delta_time)

		screen.fill(pygame.Color("white"))
		maze_surface.fill(pygame.Color("white"))
		maze.draw(maze_surface)
		# print(mazeSolver.visited)
		mazeSolver.draw_other(maze_surface, maze)
		mazeSolver.draw_path(maze_surface, mode)

		ui_manager.draw_ui(screen)
		screen.blit(maze_surface, (200, 0))
		pygame.display.flip()
			

main()

# import pygame
# from pygame.locals import *
# import settings
# import random


# class DisjoinSet():
#     def __init__(self, nodes):
#         self.map = {}






# class Tile:
#     def __init__(self, maxSet, x, y):
#         self.connections = {
#             'up' : False,
#             'left' : False,
#             'down' : False,
#             'right' : False
#         }
#         self.set = maxSet
#         self.x = x
#         self.y = y
    
#     def __hash__(self):
#         return hash((self.x, self.y))

#     def __eq__(self, other):
#         if not isinstance(other, type(self)):
#             return NotImplemented # means False basically
#         return self.x == other.x and self.y == other.y
    
#     def __str__(self):
#         return f"({self.x}, {self.y})"


# '''

# '''


# #BUILDTILES STUFF:
#     #set.union lets us join the second set into the first set 
#         #for each node in our map
#         # create a set
#         # add to a list of sets
# #KRUSKALS STUFF
# # while we have more than 1 set
#     # pull out our first set
#     #pick random node from that set
#     #pick random side from that node
#      #that exists in a different set
#     #update the connection
#     #join them set.union
#     #add back to list.
# class Maze:
#     def __init__(self):
#         self.maxSet = 0
#         self.tiles, self.tileSet = self.build_tiles() # self.tiles for now is a 2d list that just has all the tiles
#         # for x in range(settings.width):
#         #     for y in range(settings.height):
#         #         print(self.tiles[x][y].set)
#         # for row in self.tiles:
#         #     print(row)
#         # print()
#         # for tile in self.tileSet:
#         #     print(tile)
        
        
#         # the plan is to have it so that the connections get broken down and when they are broken down
#         # they are lumped into a "set". The "set" is numbered at whatever the "maxSet" is currently set to.
#         # When we break down the walls between two 0 sets, we increase self.maxSet by 1.
#         # When we break down the walls between any two other sets, we do nothing
#         # We do not break down walls of two of the same set. 
#         # Keep on doing this until only one set remains


#         # 1. Separate every node into different sets
#         # 2. Whenever "knock over wall" join the two sets
#         # 3. eventually, only one set remains

#     def find_set(self, tile_sets, current_tile):
#         for s in tile_sets:
#             if current_tile in s:
#                 #print("Found the tile!")
#                 return s

#     def get_other_coord(self, x, y, side):
#         return {
#             "left"  : (x - 1, y),  "up" : (x, y - 1),
#             "right" : (x + 1, y),"down" : (x, y + 1)
#         }[side]

#     def getOtherSide(side):
#         return {
#             'up' : 'down',
#             'left' : 'right',
#             'down' : 'up',
#             'right' : 'left'
#         }[side]
        
#     def Kruskal(self):
#         edges = []
#         for y in settings.height:
#             for x in settings.width:
#                 if y > 0:
#                     edges.append((x, y, "up"))
#                 if x > 0:
#                     edges.append((x, y, "left"))
#         random.shuffle(edges)

#         for x, y, dir in edges:
#             x, y, dir




#     # def Kruskal(self):
    
#         # while (len(self.tileSet) > 1):
#         #     # randomSet1 = random.randint(0, len(self.tileSet) - 1) # put  a lot of prints in and find it  
#         #     # while self.tileSet[randomSet1] == None:
#         #     #     randomSet1 = random.randint(0, len(self.tileSet))
#         #     # randomTile1 = random.randint(0, len(self.tileSet[randomSet1]) - 1)
            
#         #     idx = random.randint(0, len(self.tileSet) - 1)
#         #     set_one = self.tileSet.pop(idx)
#         #     tile_one = random.choice(list(set_one))

#         #     side = random.choice(["left", "right", "up", "down"])
#         #     coord = self.get_other_coord(tile_one.x, tile_one.y, side)
#         #     set_two = self.find_set(self.tileSet, self.tiles[coord[1]][coord[0]])
#         #     tile_one.connections[side] = True
#         #     self.tiles[coord[1]][coord[0]].connections[Maze.getOtherSide(side)] = True
#         #     # print(side, Maze.getOtherSide(side))
#         #     # for s in set_one:
#     #         #     print(s)
#     #         # for s in set_two:
#     #         #     print(s)
#     #         # print()
#     #         set_two.update(set_one)
#     #         # for s in set_two:
#     #         #     print(s)
            
#     #         # find and get set the other tile belongs to
#     #          # can likely go to the 2d board for this
#     #         # print(self.tiles[coord[1]][coord[0]])
#     #         # print(tile_one)
#     #         # print(self.tiles[tile_one.y][tile_one.x
            
            
#     #         exit()
#     #         # print("Len tileSet: ", len(self.tileSet))
#     #         # print("Len set in tileSet: ", len(self.tileSet[randomSet1]))
#     #         # randomWall1 = [
#     #         #     'up',
#     #         #     'down',
#     #         #     'left',
#     #         #     'right'
#     #         # ]
#     #         # random.shuffle(randomWall1)
#     #         # for choice in randomWall1:
#     #         #     if (not self.tileSet[randomSet1][randomTile1].x == 0 and 
#     #         #         not self.tileSet[randomSet1][randomTile1].y == 0 and
#     #         #         not self.tileSet[randomSet1][randomTile1].x == settings.width - 1 and
#     #         #         not self.tileSet[randomSet1][randomTile1].y == settings.height - 1):
                    
#     #         #         if not self.tileSet[randomSet1][randomTile1].connections[choice]: # Low chance of breaking
#     #         #              # kinda sus code
#     #         #             x = self.tileSet[randomSet1][randomTile1].x
#             #             y = self.tileSet[randomSet1][randomTile1].y
#             #             if (choice == 'up'):
#             #                 y -= 1
#             #             elif (choice == 'down'):
#             #                 y += 1
#             #             elif (choice == 'left'):
#             #                 x -= 1
#             #             elif (choice == 'right'):
#             #                 x += 1

#             #             self.tiles[y][x].connections[choice] = True
#             #             set2 = self.tiles[y][x].set
#             #             self.tileSet[randomSet1][randomTile1].connections[choice] = True
#             #             for i in self.tileSet[set2]:
#             #                 i.set = self.tileSet[randomSet1][randomTile1].set
#             #             self.tileSet[randomSet1].extend(self.tileSet[set2])
#             #             self.tileSet[set2] = None
                        
                        



#             #         # join the two sets and break connection
                
#             #     # when we create the sets originally, we write / record into the tile
#             #     # the index of the set it belongs to
            
#             #     # right after we pick the tile that we want to break a wall from, which we have just done,
#             #     # we can go to the adjacent tile that we have picked using self.tiles
                
#             #     #---------

#             #     # From here, what we can do, now that we have all the information (the board, the adjacent)
#             #     # We can go to the new tile, and we can do the connections. We can break the connections
#             #     # from both sides, and then we have the tile set for the current and the new one
#             #     # because the other tile set for both is stored inside the tile that we got

#             #     # Once we know that, we know which two sets to store together

#             # if self.checkBreakable():
#             #     pass


#         # Math for left wall
        
#         # Math for upper wall
#         # Math for right wall
#         # Math for down wall

#     def checkBreakable(self):
#         return True

#     def build_tiles(self):
#         allTiles = []
#         tileSet = []
#         for y in range(settings.height):
#             tiles = []
#             for x in range(settings.width):
#                 newTile = Tile(self.maxSet, x, y)
#                 tiles.append(newTile)
#                 tileSet.append(set([newTile])) # we want this to be a list for our logic later on
#                 self.maxSet += 1          # both of these reference the same object in memory
#             allTiles.append(tiles)
#         return allTiles, tileSet

#     def draw_board(self, screen):
#         xOff, yOff = 100, 100
#         for x in range(settings.width):
#             for y in range(settings.height):
#                 #Left
#                 if (not self.tiles[x][y].connections['left']):
#                     pygame.draw.line(
#                         screen,
#                         (255, 255, 255),
#                         (x * settings.gridSize + xOff, y * settings.gridSize + yOff),
#                         (x * settings.gridSize + yOff, (y + 1) * settings.gridSize + yOff),
#                         1
#                     )
#                 #Upper
#                 if (not self.tiles[x][y].connections['up']):
#                     pygame.draw.line(
#                         screen,
#                         (255, 255, 255),
#                         (x * settings.gridSize + xOff, y * settings.gridSize + yOff),
#                         ((x+1) * settings.gridSize + yOff, y * settings.gridSize + yOff),
#                         1
#                     )
#                 #Right
#                 if (not self.tiles[x][y].connections['right']):
#                     pygame.draw.line(
#                         screen,
#                         (255, 255, 255),
#                         ((x+1) * settings.gridSize + xOff, y * settings.gridSize + yOff),
#                         ((x+1) * settings.gridSize + yOff, (y + 1) * settings.gridSize + yOff),
#                         1
#                     )
#                 # Lower
#                 if (not self.tiles[x][y].connections['down']):
#                     pygame.draw.line(
#                         screen,
#                         (255, 255, 255),
#                         (x * settings.gridSize + xOff, (y + 1) * settings.gridSize + yOff),
#                         ((x + 1) * settings.gridSize + yOff, (y + 1) * settings.gridSize + yOff),
#                         1
#                     )