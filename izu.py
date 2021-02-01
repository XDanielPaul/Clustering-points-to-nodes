import math
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext, ROUND_HALF_UP

round_context = getcontext()
round_context.rounding = ROUND_HALF_UP

# PYTHON SUCKS AT ROUNDING (round(1.125) == 1.12), SO THIS FUNCTION ROUND`S CORRECTLY (c_round(1.125) == 1.13)


def c_round(x, digits, precision=5):
    tmp = round(Decimal(x), precision)
    return float(tmp.__round__(digits))

# CLASS FOR POINT


class Point:

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.coordinates = coordinates

    def len(self, node):
        # EUCLIDIAN LENGTH OF TWO 3D POINTS
        return math.sqrt((node.x-self.x)**2 + (node.y-self.y)**2 + (node.z-self.z)**2)

    def __repr__(self):
        return str(self.coordinates)


class Computing:

    def __init__(self, pts, nds, iterations):
        # POINTS
        self.points = [Point(point) for point in pts]
        # NODES/CENTROIDS
        self.nodes = [Point(point) for point in nds]
        # STARTING CENTROIDS
        self.clusters = [[Point([-3, -1, -3])],
                         [Point([-3, 0, 0])], [Point([-1, 1, -4])]]
        print("Starting with", repr(self.nodes))
        self.compute(iterations)

    # APPENDS POINTS
    def append_points_to_clusters(self):
        for point in self.points:
            results = []
            for node in self.nodes:
                results.append(Point.len(point, node))
            # APPENDS POINT TO A CLUSTER WITH CENTROID TO WHICH THE POINT HAS THE SMALLEST EUKLIDIAN DISTANCE
            self.clusters[results.index(min(results))].append(point)

    def calculate_new_centroids(self, iterations):
        new_centroids = []
        # CALCULATES NEW CENTROIDS WITH MEAN OF COORDINATES OF POINTS WHICH BELONG TO SPECIFIC CLUSTER
        for cluster in self.clusters:
            x = y = z = 0
            for point in cluster[1:]:
                x += point.x
                y += point.y
                z += point.z
            if (len(cluster) != 1):
                # NEW CENTOROID IS BEING CALCULATED
                new_centroids.append(Point([c_round(
                    x/(len(cluster)-1), 2), c_round(y/(len(cluster)-1), 2), c_round(z/(len(cluster)-1), 2)]))
            # CLUSTER IS EMPTY - OLD CENTROID REMAINS AS THE NEW ONE
            else:
                new_centroids.append(cluster[0])

        # PLOTS 3D GRAPH AFTER PROCESSING ALL ITERATIONS
        if (self.i == iterations):
            self.plot()

        print("Iteration", self.i)
        print("Cluster 1:", self.clusters[0])
        print("Cluster 2:", self.clusters[1])
        print("Cluster 3:", self.clusters[2])
        print("New centroids:", repr(new_centroids), "\n")
        self.clusters = [[new] for new in new_centroids]
        self.nodes = new_centroids

    # WHILE LOOP FOR COMPUTING
    def compute(self, iterations):
        self.i = 1
        while (self.i != iterations+1):
            self.append_points_to_clusters()
            self.calculate_new_centroids(iterations)
            self.i += 1

    # PLOTTING THE GRAPH
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter3D([item.x for item in self.clusters[0]], [item.y for item in self.clusters[0]], [
                     item.z for item in self.clusters[0]],  color="r")
        ax.scatter3D([item.x for item in self.clusters[1]], [item.y for item in self.clusters[1]], [
                     item.z for item in self.clusters[1]],  color="b")
        ax.scatter3D([item.x for item in self.clusters[2]], [item.y for item in self.clusters[2]], [
                     item.z for item in self.clusters[2]],  color="g")
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()


# INPUT POINTS
pts = [[0, 1, 4], [-1, 1, 3], [-1, -1, 3], [1, 0, 4], [4, 0, 0], [5, 1, 1],
       [5, -1, -1], [6, 0, 0], [1, 4, 0], [2, 3, 1], [0, 4, 2], [-1, 5, 1]]
#pts = [[7,1,4], [-1,6,3], [-1,-4,3], [5,0,4], [4,-6,0], [5,-4,1], [5,-2,-1], [6,2,-7], [1,4,7], [2,3,1], [0,4,-2], [-1,5,11]]
# NODES
nds = [[-3, -1, -3], [-3, 0, 4], [-1, 1, -4]]

# INPUT = NUMBER OF ITERATIONS
Computing(pts, nds, int(input()))
