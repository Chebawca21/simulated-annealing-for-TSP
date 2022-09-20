from simulated_annealing import *

import numpy as np

sa = SimulatedAnnealing()

def kmeans(k, adjencyMatrix, maxN=100):
    dim = len(adjencyMatrix)
    # initial centroids
    newCentroids = np.random.choice(dim, k, replace=False)
    centroids = np.full_like(newCentroids, -1)

    N = 0
    while not np.array_equal(centroids, newCentroids):
        centroids = newCentroids.copy()
        newCentroids = np.full_like(centroids, -1)

        # assigning points to correct clusters
        clusters = np.empty((k, 1)).tolist()
        for i in range(k):
            clusters[i] = []
        
        for point in range(dim):
            if not np.isin(point, centroids):
                minDistance = float('inf')
                minCentroids = []
                for centroid in centroids:
                    if adjencyMatrix[centroid][point] < minDistance:
                        minDistance = adjencyMatrix[centroid][point]
                        minCentroids = [centroid]
                    elif adjencyMatrix[centroid][point] == minDistance:
                        minCentroids.append(centroid)
                index = np.where(centroids == np.random.choice(minCentroids))[0][0]
                clusters[index].append(point)
        
        # recalculating centroids
        n = 0
        for cluster in clusters:
            minSumDistances = float('inf')
            minPoints = []
            for point in cluster:
                sumDistances = 0
                for i in range(dim):
                    if not point == i:
                        sumDistances = sumDistances + adjencyMatrix[point][i]

                if sumDistances < minSumDistances:
                    minSumDistances = sumDistances
                    minPoints = [point]
                elif sumDistances == minSumDistances:
                    minPoints.append(point)
            
            if len(minPoints) == 0:
                newCentroids[n] = centroids[n]
            else:
                newCentroids[n] = np.random.choice(minPoints)
            
            n = n + 1
        
        N = N + 1
        if N >= maxN:
            break

    return clusters

print(kmeans(3, sa.adjencyMatrix))