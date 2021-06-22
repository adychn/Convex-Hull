import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __sub__(self, other):
		return [self.x - other.x, self.y - other.y]

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __lt__(self, other):
		if self.x < other.x:
			return True
		elif self.x == other.x:
			if self.y < other.y:
				return True
		return False

	def __repr__(self):
		return f"Point({self.x}, {self.y})"

	def __str__(self):
		return f"Point({self.x}, {self.y})"

class ConvexHull():
	def __init__(self):
		self.points = deque()
		self.pointsSet = set()
		self.hullPoints = []
		self.hullPointsSet = set()

	def __str__(self):
		return f"""
		Current points: {self.points}

		Current hull points: {self.hullPoints}

		"""
		
	def add(self, point):
		'''
		Add a list of points into the object.
		O(1).

		Parameters:
		Point

		Returns:
		None
		'''
		# corner cases
		if not isinstance(point, Point):
			print("Can't add, only Point class is allowed.")
			return

		# skip duplicate points
		if (point.x, point.y) in self.pointsSet:
			return
		
		# main program
		# maintain the leftmost bottom point in the beginning of the deque.
		self.pointsSet.add((point.x, point.y))
		# self.points.append(point) TODO
		if self.points and point.x < self.points[0].x:
			self.points.appendleft(point)
		elif self.points and point.x == self.points[0].x:
			if point.y < self.points[0].y:
				self.points.appendleft(point)
			else:
				self.points.append(point)
		else:
			self.points.append(point)

	def getAll(self):
		'''
		Return a list of all points from the object, deep copied.
		O(n) operation due to deep copy.

		Parameters:
		None

		Returns:
		List[Point]
		'''
		return copy.deepcopy(self.points)

	def getHull(self):
		'''
		Return a list of hull points from the object, deep copied.
		O(h) operation due to deep copy.

		Parameters:
		None

		Returns:
		List[Point]		
		'''
		return copy.deepcopy(self.hullPoints)

	def remove(self, point):
		'''
		Remove a list of points from the ConvexHull object.
		O(n).
		
		Parameters:
		Point

		Returns:
		None
		'''
		if (point.x, point.y) in self.pointsSet:
			self.pointsSet.remove((point.x, point.y))
			self.points.remove(point)
		if (point.x, point.y) in self.hullPointsSet:
			self.hullPointsSet.remove((point.x, point.y))
			self.hullPoints.remove(point)

	def plot(self):
		'''
		Plot all points that was added in to this object, and the convex hull (if any). 
		O(n).
		
		Parameters:
		None

		Returns:
		None
		'''
		x = [p.x for p in self.points]
		y = [p.y for p in self.points]
		plt.plot(x, y, marker='o', color='blue', linestyle='None', ms=2)

		hx = [p.x for p in self.hullPoints]
		hy = [p.y for p in self.hullPoints]
		if hx:
			hx.append(hx[0])
		if hy:
			hy.append(hy[0])
		plt.plot(hx, hy, marker='o', linestyle='-', color='red', ms=3)

		# inHullx = []
		# inHully = []
		# for p in points:
		# 	inHullx.append(p.x)
		# 	inHully.append(p.y)
		# plt.plot(inHullx, inHully, marker='o', linestyle='None', color='green', ms=2)

		plt.xlabel('X')
		plt.ylabel('Y')
		plt.title("Convex Hull")
		plt.show()

	def within(self, point):
		'''
		Check if a given Point object is inside the convex hull.
		O(h).
		
		Parameters:
		Point

		Returns:
		bool
		'''
		if not self.hullPoints:
			return False
		'''
		If the polygon is convex then one can consider the polygon as a "path" from the 
		first vertex. A point is on the interior of this polygons if it is always on the 
		same side of all the line segments making up the path.
		'''
		n = len(self.hullPoints)
		j = n - 1
		x, y = point.x, point.y
		c = False
		for j, i in zip(range(-1, n - 1), range(0, n)):
			p0 = self.hullPoints[j]
			p1 = self.hullPoints[i]
			if x == p1.x and y == p1.y:
				# point is a hull point
				return True 			
			if (p1.y > y) != (p0.y > y):
				# a line is formed by p0 and p1.
				# if diff > 0 then point is to the right of line.
				# if diff == 0 then point is on the line
				# if diff < 0 then point is to the left of line.
				diff = (x - p1.x) * (p0.y - p1.y) - (p0.x -p1.x) * (y - p1.y)
				if diff == 0:
					return True
				if (diff < 0) != (p0.y < p1.y):
					c = not c
		return c

	def hull(self):
		'''
		Gift Wrapping Algorithm (aka Jarvis march). 
		
		O(nh) time complexity, n is the number of points, 
		and h is the number of points on the convex hull. h >> log(n)

		Parameters:
		None

		Returns:
		None

		'''
		# corner cases
		if len(self.points) < 3:
			print("There are less than 3 points currently, no convex hull can be formed.")
			print("Please add more points and try again.")
			print()
			return

		p0 = self.points[0]
		p1 = self.points[1]
		v1 = p1 - p0
		allInOneLine = True
		for i in range(2, len(self.points)):
			v2 = self.points[i] - p0
			crossProduct = np.cross(v1, v2)
			if crossProduct != 0:
				allInOneLine = False
				break
		if allInOneLine:
			print("All points are in a line, no area can be formed with points we currently have.")
			print(self.points)
			print("Please add more points and try again.")
			print()
			return

		# main program
		hullPoints = []
		hullSet = set()
		firstRunFlag = True
		cur_hull_point = first_hull_point = self.points[0]
		nxt_hull_point = self.points[1]

		# Loop until all convex hull points are found.
		while cur_hull_point != first_hull_point or firstRunFlag:
			firstRunFlag = False
			hullPoints.append(cur_hull_point)
			hullSet.add((cur_hull_point.x, cur_hull_point.y))
			'''
			Make nxt_hull_point the most couterclock wise (CCW) point.
			
			Need to run the loop twice to prevent cross product equals to 0 problem (colinear).
			It occurs when the most CCW point (ref_point) vector lies 180 deg at the opposite 
			direction from the nxt_hull_point vector, nxt_hull_point won't update since cross 
			product is 0, and the ref_point isn't checked again in the first loop.

			During the second loop, nxt_hull_point must have moved away from the original point
			that caused cross product with the most CCW point equals to 0. Then in this case,
			we can correctly obtain the negative cross product and moved nxt_hull_point to 
			the most CCW point.
			'''
			for _ in range(2):
				for ref_point in self.points:
					if ref_point == nxt_hull_point or ref_point == cur_hull_point:
						continue
					vref = ref_point - cur_hull_point
					vhull = nxt_hull_point - cur_hull_point
					crossProduct = np.cross(vref, vhull)
					# If crossProduct is negative, it means ref_point is further counterclock wise.
					if crossProduct < 0: 
						nxt_hull_point = ref_point
			# reset nxt_hull_point to any point
			cur_hull_point, nxt_hull_point = nxt_hull_point, cur_hull_point
			# self.plot() # to plot the step by step hull finding graph

		'''
		There may be multiple most CCW hull points that lie in the same line, and the hull may 
		skips some of those points. Due to if the furtherest point is picked as the next hull point
		the closer most CCW points won't be picked.
		'''
		# Make points on hull lines into hull points.
		newHullPoints = []
		n = len(hullPoints)
		for i in range(n):
			j = (i + 1) % n
			p0 = hullPoints[i]
			p1 = hullPoints[j]
			newHullPoints.append(p0)
			for p in self.points:
				if (p.x, p.y) in hullSet:
					continue
				vhull = p1 - p0
				vp = p - p0
				crossProduct = np.cross(vhull, vp)
				if crossProduct == 0:
					newHullPoints.append(p)
					hullSet.add((p.x, p.y))
		self.hullPoints = newHullPoints





def main():
	'''	1. Given a set of 2D points, compute the convex hull.
       	2. Given some more points, find if they are inside the convex hull.
    '''
	# points = [Point(0, 0), Point(0, 10), Point(0, 20), Point(0, 30),
	# 		  Point(50, 0), Point(50, 10), Point(50, 20), Point(50, 30),
	# 		  Point(10, 50), Point(20, 50), Point(30, 50), Point(40, 50),
	# 		  Point(10, 0), Point(20, 0), Point(30, 0), Point(40, 0),]
	points = []
	pointsToCheck = []
	numPointsToAdd = 100
	minX, maxX = 0, 60
	minY, maxY = 0, 60
	step = 1
	numPointsToCheck = 5
	ch = ConvexHull()

	# corner test case 1 - when vector cross product can be zero.
	# points = [Point(0, 0), Point(0, 5), Point(0, 2), Point(0, 10), Point(3, 3)]
	# for p in points:
	# 	ch.add(p)

	# corner test case 2 - all points in a line.
	# points = [Point(0, 0), Point(0, 2), Point(0, 5), Point(0, 10)]
	# points = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]
	# for p in points: 
	# 	ch.add(p)
	
	# Main randomized test
	print("Begin randomized points test case......\n")
	print("Add points.\n")
	for _ in range(numPointsToAdd):
		p = Point(random.randint(0, 100), random.randint(0, 100))
		points.append(p)
	for p in points:
		ch.add(p)

	print("Find the hull.\n")
	ch.hull()

	print("Check if a given point sit in the hull.")
	for _ in range(numPointsToCheck):
		p = Point(random.randrange(minX, maxX+1, step), random.randrange(minY, minY+1, step))
		pointsToCheck.append(p)
		print(f"Is {p} in the hull? {ch.within(p)}")
	print()
			
	print("Check if all existing points are in the hull. Should be all true.")
	for p in points:
		answer = ch.within(p)
		print(f"Is {p} in the hull? {answer}")
		if not answer:
			print("It should be all true, either there is no hull or this program has a bug.\n")
			break

	ch.plot()

if __name__ == "__main__":
	main()
