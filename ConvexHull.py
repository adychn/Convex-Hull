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
		
	def addPoints(self, points):
		'''
		Add a list of points into the object.
		O(1 * points to add).

		Parameters:
		List[Point]

		Returns:
		None
		'''
		for point in points:
			# can only accept Point object
			if not isinstance(point, Point):
				print("Can't add, only Point class is allowed.")
				return

			# skip duplicate points
			if (point.x, point.y) in self.pointsSet:
				continue
			
			# maintain the leftmost bottom point in the beginning of the deque.
			self.pointsSet.add((point.x, point.y))
			if self.points and point.x < self.points[0].x:
				self.points.appendleft(point)
			elif self.points and point.x == self.points[0].x:
				if point.y < self.points[0].y:
					self.points.appendleft(point)
				else:
					self.points.append(point)
			else:
				self.points.append(point)

	def getPoints(self):
		'''
		Return a list of all points from the object, deep copied.
		O(n) operation due to deep copy.

		Parameters:
		None

		Returns:
		List[Point]
		'''
		return copy.deepcopy(self.points)

	def getHullPoints(self):
		'''
		Return a list of hull points from the object, deep copied.
		O(h) operation due to deep copy.

		Parameters:
		None

		Returns:
		List[Point]		
		'''
		return copy.deepcopy(self.hullPoints)

	def removePoints(self, points):
		'''
		Remove a list of points into the ConvexHull object.
		O(n * points to remove).
		
		Parameters:
		List[Point]

		Returns:
		None
		'''
		for p in points:
			if p in self.pointsSet:
				self.pointsSet.remove(p)
				self.points.remove(p)
			if p in self.hullPointsSet:
				self.hullPointsSet.remove(p)
				self.hullPoints.remove(p)

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
		plt.plot(x, y, marker='o', linestyle='None', ms=2)

		hx = [p.x for p in self.hullPoints]
		hy = [p.y for p in self.hullPoints]
		if hx:
			hx.append(hx[0])
		if hy:
			hy.append(hy[0])
		plt.plot(hx, hy, marker='o', linestyle='-', color='red', ms=3)

		print(self)
		plt.xlabel('X')
		plt.ylabel('Y')
		plt.title("Convex Hull")
		plt.show()

	def isInHull(self, point):
		'''
		Check if a given Point object is inside the convex hull.
		O(1).
		
		Parameters:
		Point

		Returns:
		bool
		'''
		if not self.hullPoints:
			return False

		vref = self.hullPoints[1] - self.hullPoints[0]
		vcheck = point - self.hullPoints[0]




	def findConvexHull(self):
		'''
		Gift Wrapping Algorithm (aka Jarvis march). 
		
		O(nh) time complexity, n is the number of points, 
		and h is the number of points on the convex hull.

		Parameters:
		None

		Returns:
		None

		'''
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

		self.hullPoints = []
		firstRunFlag = True
		cur_hull_point = first_hull_point = self.points[0]
		nxt_hull_point = self.points[1]

		# Loop until all convex hull points are found.
		while cur_hull_point != first_hull_point or firstRunFlag:
			firstRunFlag = False
			self.hullPoints.append(cur_hull_point)

			'''
			Make nxt_hull_point the most couterclock wise (CCW) point.
			
			There may be multiple CCW points that lies in the same line, and the hull may skips 
			some of those points. It is fine, it doesn't affect the correctness of the hull.

			Need to run the loop twice to prevent cross product equals to 0 problem.
			It occurs when the most CCW point (ref_point) vector lies 180 deg at the opposite 
			direction from the nxt_hull_point vector, nxt_hull_point won't update since cross 
			product is 0, and the ref_point isn't checked again in the first loop.

			During the second loop, nxt_hull_point must have moved away from the original point
			that causes vector cross product with the most CCW equals to 0. Then in this case,
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

			cur_hull_point = nxt_hull_point
			nxt_hull_point = first_hull_point # reset nxt_hull_point to any point
			# self.plot() # to plot the step by step hull finding graph


