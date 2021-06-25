import copy
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class Point():
	def __init__(self, x, y, z=0):
		self.x = x
		self.y = y
		self.z = z

	def __sub__(self, other):
		return [self.x - other.x, self.y - other.y, self.z - other.z]

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z

	def __lt__(self, other):
		if self.x < other.x:
			return True
		elif self.x == other.x:
			if self.y < other.y:
				return True
			elif self.y == other.y and self.z and other.z:
				if self.z < other.z:
					return True
		return False

	def __repr__(self):
		return f"Point({self.x}, {self.y}, {self.z})"

	def __str__(self):
		return f"Point({self.x}, {self.y}, {self.z})"

class ConvexHull2D():
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
	def getAllPoints(self):
		'''
		Return a list of all points from the object, deep copied. O(n) operation due to deep copy.

		Parameters:
		None

		Returns:
		List[Point]
		'''
		return copy.deepcopy(self.points)

	def getHullPoints(self):
		'''
		Return a list of hull points from the object, deep copied. O(h) operation due to deep copy.

		Parameters:
		None

		Returns:
		List[Point]		
		'''
		return copy.deepcopy(self.hullPoints)

	def add(self, point):
		'''
		Add a list of points into the object. O(1).

		Parameters:
		point: Point(x, y, z=0)

		Returns:
		None
		'''
		# corner cases
		if not isinstance(point, Point):
			print("Can't add, only Point class is allowed.")
			return

		# duplicate point
		if (point.x, point.y, point.z) in self.pointsSet:
			return

		self.pointsSet.add((point.x, point.y, point.z))
		if not self.points:
			self.points.append(point)	
		elif point < self.points[0]: # maintain the leftmost bottom point in the beginning
			self.points.appendleft(point)
		else:
			self.points.append(point)

	def remove(self, point):
		'''
		Remove a list of points from the ConvexHull object. O(n).
		
		Parameters:
		point: Point(x, y, z=0)

		Returns:
		None
		'''
		if (point.x, point.y, point.z) in self.pointsSet:
			self.pointsSet.remove((point.x, point.y, point.z))
			self.points.remove(point)
		if (point.x, point.y, point.z) in self.hullPointsSet:
			self.hullPointsSet.remove((point.x, point.y, point.z))
			self.hullPoints.remove(point)

	def plot(self):
		'''
		Plot all points that was added in to this object, and the convex hull (if any).
		
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

		plt.xlabel('X')
		plt.ylabel('Y')
		plt.title("2D Convex Hull")
		plt.show()

	def within(self, point):
		'''
		Check if a given Point object is inside the convex hull.
		O(h), h is the number of points on the convex hull
		
		Parameters:
		Point

		Returns:
		bool
		'''
		if not self.hullPoints:
			return False
		'''
		Walk the edge of the convex hull polygon.
		A point is in this polygon if it is always on the same side 
		of all the line segments making up the path.
		'''
		c = False
		n = len(self.hullPoints)
		for j, i in zip(range(-1, n - 1), range(0, n)):
			p0 = self.hullPoints[j]
			p1 = self.hullPoints[i]
			if point == p1: 
				# point is a hull point
				return True 			
			if (p1.y > point.y) ^ (p0.y > point.y):
				# point.y lies between [p0.y, p1.y]
				crossProduct = np.cross(point - p0, p1 - p0)
				if crossProduct[2] == 0:
					return True
				if (crossProduct[2] > 0) ^ (p0.y > p1.y):
					c = not c
		return c

	def hull(self):
		'''
		Gift Wrapping Algorithm (aka Jarvis march). 
		O(nh) time complexity, n is the number of points, 
		and h is the number of points on the convex hull.

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
			if crossProduct.any():
				allInOneLine = False
				break
		if allInOneLine:
			print("All points lie in a line, no area can be formed.")
			print("Please add more points and try again.")
			print()
			return

		# main program
		'''
		Loop until all convex hull points are found.
		Make nextHullPoint the most couterclock wise (CCW) point.
		
		Need to run the loop twice to prevent cross product equals to 0 problem (colinear).
		It occurs when the most CCW point (ref_point) vector lies 180 deg at the opposite 
		direction from the nextHullPoint vector, nextHullPoint won't update since cross 
		product is 0, and the ref_point isn't checked again in the first loop.

		During the second loop, nextHullPoint must have moved away from the original point
		that caused cross product with the most CCW point equals to 0. Then in this case,
		we can correctly obtain the negative cross product and moved nextHullPoint to 
		the most CCW point.
		'''
		hullPoints = []
		hullSet = set()
		firstRunFlag = True
		curHullPoint = firstHullPoint = self.points[0]
		nextHullPoint = self.points[1]
		while curHullPoint != firstHullPoint or firstRunFlag:
			firstRunFlag = False
			hullPoints.append(curHullPoint)
			hullSet.add((curHullPoint.x, curHullPoint.y))
			for _ in range(2):
				for point in self.points:
					if point == nextHullPoint or point == curHullPoint:
						continue
					crossProduct = np.cross(point - curHullPoint, nextHullPoint - curHullPoint)
					# If crossProduct is negative, it means point is further counterclock wise.
					if crossProduct[2] < 0: 
						nextHullPoint = point
			# reset nextHullPoint to any point
			curHullPoint, nextHullPoint = nextHullPoint, curHullPoint
			# self.plot() # to plot the step by step hull finding graph

		'''
		Make points on hull lines into hull points.

		There may be multiple most CCW hull points that lie in the same line, and the hull may 
		skips some of those points. Due to if the furtherest point is picked as the next hull point
		the closer most CCW points won't be picked.
		'''
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
				if crossProduct[2] == 0:
					newHullPoints.append(p)
					hullSet.add((p.x, p.y))
		self.hullPoints = newHullPoints

class ConvexHull3D(ConvexHull2D):
	def plot(self):
		'''
		Plot all points that was added in to this object, and the convex hull (if any).
		
		Parameters:
		None

		Returns:
		None
		'''

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		x = [p.x for p in self.points]
		y = [p.y for p in self.points]
		z = [p.z for p in self.points]
		ax.scatter(x, y, zs=z, marker='o', s=2)

		hx = [p.x for p in self.hullPoints]
		hy = [p.y for p in self.hullPoints]
		hz = [p.z for p in self.hullPoints]
		if hx:
			hx.append(hx[0])
		if hy:
			hy.append(hy[0])
		if hz:
			hz.append(hz[0])
		ax.plot(hx, hy, zs=hz, marker='o', linestyle='dotted', color='red', ms=2)

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		ax.set_title("3D Convex Hull")
		plt.show()

	def within(self, point):
		'''
		Check if a given Point object is inside the convex hull. O(F), where F is number of faces.
		
		Parameters:
		point: Point(x, y, z)

		Returns:
		bool
		'''
		if not self.hullPoints:
			return False

		'''
		The point needs to lie to the right all faces.
		Why so simple? Because when we add faces to our convex hull, all points lie 
		to the right of faces, since that's how we orient hull faces in self.hull().
		'''
		pos, neg = 0, 0
		for face in self.faces:
			a, b, c = face
			if point == a or point == b or point == c:
				return True
			q = np.cross(b - a, c - a) # q is an ortho vector points into the hull
			sign = np.dot(point - a, q)
			if sign > 0: # lie to the right of the face
				pass
			elif sign == 0: # lie in the face plane
				return True
			else: # lie to the left of the face
				return False
		return True

	def __allInOnePlane(self):
		# create an equation plane and check against all points.
		n = len(self.points)
		for i in range(0, n - 2):
			for j in range(1, n - 1):
				for k in range(2, n):
					x1, y1, z1 = self.points[i].x, self.points[i].y, self.points[i].z
					x2, y2, z2 = self.points[j].x, self.points[j].y, self.points[j].z
					x3, y3, z3 = self.points[k].x, self.points[k].y, self.points[k].z
					a1 = x2 - x1
					b1 = y2 - y1
					c1 = z2 - z1
					a2 = x3 - x1
					b2 = y3 - y1
					c2 = z3 - z1
					a = b1 * c2 - b2 * c1
					b = a2 * c1 - a1 * c2
					c = a1 * b2 - b1 * a2
					d = -a * x1 - b * y1 - c * z1
					for p in self.points:
						if (a*p.x + b*p.y + c*p.z + d) != 0:
							return False
		return True

	def hull(self):
		'''
		Brute Force Algorithm. O(n^4)

		Parameters:
		None

		Returns:
		None

		'''
		# corner case
		n = len(self.points)
		if n < 4:
			print("There are less than 4 points currently, no convex hull can be formed.")
			print("Please add more points and try again.")
			print()
			return

		# corner case
		if self.__allInOnePlane():
			print("All points lie in a plane, no hull can be formed.")
			print("Please add more points and try again.")
			print()
			return

		# main program
		'''
		Choose three points from a combination of existing points to form a plane.
		If all other remaining points are to the one side of the plane, 
		then these three points are convex hull points. 
		Repeat for all combinations.
		'''
		self.faces = []
		for i in range(0, n - 2):
			for j in range(i + 1, n - 1):
				for k in range(j + 1, n):
					a, b, c = self.points[i], self.points[j], self.points[k]
					q = np.cross(b - a, c - a)

					pos, zero, neg = 0, 0, 0
					for p in self.points:
						if p == a or p == b or p == c:
							continue
						sign = np.dot(p - a, q)
						if sign > 0:
							pos += 1
						elif sign == 0:
							zero += 1
						else:
							neg += 1
					if bool(pos) ^ bool(neg):
						# make sure all faces are oriented correctly, so the cross product of 
						# (vector_a_to_b, vector_a_to_c) always points toward inside the hull. 
						if bool(pos):
							order = [a, b, c]
						else:
							order = [a, c, b]
						self.hullPoints.extend(order)
						self.faces.append(order)
						self.hullPointsSet.add((a.x, a.y, a.z))
						self.hullPointsSet.add((b.x, b.y, b.z))
						self.hullPointsSet.add((c.x, c.y, c.z))
						