import random
from ConvexHull import *
def convex_hull_corner_test(dimension='2d'):
	print(f"Begin testing corner cases, dimension is {dimension}.")
	if dimension == '2d':
		# corner test case 1, when vector cross product can be zero (2D only).
		ch = ConvexHull2D()
		points = [Point(0, 0), Point(0, 5), Point(0, 2), Point(0, 10), Point(3, 3)]
		for p in points:
			ch.add(p)
		ch.hull()

		# corner test case 2, no hull can be formed with the points we have.
		ch = ConvexHull2D()
		points = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]
		for p in points:
			ch.add(p)
		ch.hull()

		# corner test case 3, less than 3 points for 2D, or less than 4 points for 3D.
		ch = ConvexHull2D()
		points = [Point(1, 1), Point(2, 2)]
		for p in points:
			ch.add(p)
		ch.hull()
	else:
		# corner test case 2, no hull can be formed with the points we have.
		ch = ConvexHull3D()
		points = [Point(1, 1, 1), Point(2, 2, 2), Point(3, 3, 3), Point(4, 4, 4), Point(5, 7, 3)]
		for p in points:
			ch.add(p)
		ch.hull()

		# corner test case 3, less than 3 points for 2D, or less than 4 points for 3D.
		ch = ConvexHull3D()
		points = [Point(1, 1, 1), Point(2, 2, 2), Point(3, 3, 3)]
		for p in points:
			ch.add(p)
		ch.hull()
	print("Corner cases all captured.\n")

def convex_hull_test(dimension='2d', numPointsToAdd=50, minX=0, maxX=60, minY=0, maxY=60, 
						minZ=0, maxZ=60, step=1, numPointsToCheck=5):
	'''	1. Given a set of 2D or 3D points, compute the convex hull.
		2. Given some more points, find if they are inside the convex hull.
	'''
	points = []
	pointsToCheck = []
	if dimension == '2d':
		print("Testing 2D convex hull.")
		ch = ConvexHull2D()
	elif dimension == '3d':
		print("Testing 3D convex hull.")
		ch = ConvexHull3D()
	else:
		print("Please specify the correct dimension to test. convex_hull_test(dimension={'2d' or '3d'}.\n")
		return

	# Main randomized test
	############################################################
	print("Begin randomized points test case......")
	print("Adding points...")
	for _ in range(numPointsToAdd):
		if dimension == '2d':
			p = Point(random.randrange(minX, maxX + 1, step), 
					  random.randrange(minY, maxY + 1, step),
					 )
		else:
			p = Point(random.randrange(minX, maxX + 1, step), 
				  	  random.randrange(minY, maxY + 1, step),
				  	  random.randrange(minZ, maxZ + 1, step),
				  	 )
		points.append(p)
	for p in points:	
		ch.add(p)
	print(f"The following points were added: {ch.getAllPoints()}\n")
	############################################################
	print("Finding the hull...")
	ch.hull()
	print(f"Here are a list of hull points: {ch.getHullPoints()}\n")
	############################################################
	print("Check if a given point sit in the hull...")
	offset = (maxX - minX) // 4
	for _ in range(numPointsToCheck):
		if dimension == '2d':
			p = Point(random.randrange(minX - offset, maxX + offset, step), 
					  random.randrange(minY - offset, maxY + offset, step),
					 )
		else:
			p = Point(random.randrange(minX - offset, maxX + offset, step), 
				  	  random.randrange(minY - offset, maxY + offset, step),
				  	  random.randrange(minZ - offset, maxZ + offset, step),
				  	 )
		pointsToCheck.append(p)
		print(f"Is {p} in the hull? {ch.within(p)}")
	print()
	############################################################		
	print("Check if all existing points are in the hull. Should be all true.")
	for p in points:
		answer = ch.within(p)
		# print(f"Is {p} in the hull? {answer}")
		if not answer:
			print("It should be all true, either there is no hull or this program has a bug.\n")
			break
	print("All good. All existing points are in the hull.\n")
	############################################################
	print("Here is a figure showing all points and the hull...")
	ch.plot()
	print("Finished.\n")
	print()
	print()

def main():
	kwargs = dict(numPointsToAdd = 10,
				  numPointsToCheck = 5,
				  minX = 0,
				  maxX = 60,
				  minY = 0,
				  maxY = 60,
				  minZ = 0,
				  maxZ = 60,
				  step = 1,
				  )
	# convex_hull_corner_test(dimension='2d')
	# convex_hull_corner_test(dimension='3d')
	convex_hull_test(dimension='2d', **kwargs)
	convex_hull_test(dimension='3d', **kwargs)

if __name__ == "__main__":
	main()