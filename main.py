from ConvexHull import *

def main():
	ch = ConvexHull()

	# corner test case 1
	# to detect the problem of when cross product is zero.
	# ch.add([Point(0, 0), Point(0, 2), Point(0, 5), Point(0, 10), Point(3, 3)])

	# corner test case 2
	# points can't form an area
	# ch.add([Point(0, 0), Point(0, 2), Point(0, 5), Point(0, 10)])
	# ch.add([Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)])

	# randomized points test case
	p = []
	for _ in range(100):
		p.append(Point(random.randint(0, 50), random.randint(0, 50)))
	
	ch.addPoints(p)

	ch.findConvexHull()
	# print(ch)
	ch.plot()


if __name__ == "__main__":
	main()