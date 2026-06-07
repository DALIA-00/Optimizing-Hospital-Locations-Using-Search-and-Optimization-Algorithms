import numpy as np


def build_distance_matrix(population_points, candidate_locations):
    n = len(population_points)
    m = len(candidate_locations)

    distances = np.zeros((n, m)) # n x m matrix to store distances between population points and candidate locations

    for i, p in enumerate(population_points):
        for j, c in enumerate(candidate_locations):
            distances[i][j] = np.sqrt( (p[0] - c[0])**2 + (p[1] - c[1])**2 ) # distance formula between population point p and candidate location c

    return distances

def evaluate(solution, distance_matrix, weights, lambda_cost):

    selected = np.where(solution == 1)[0] # get the indices of the selected candidate locations (where solution is 1)

    if len(selected) == 0: return float("inf") # if no locations are selected, return infinity as the cost

    nearest_distances = np.min( distance_matrix[:, selected], axis=1 ) # for each population point, find the minimum distance to the selected candidate locations)
    travel_cost = np.sum( nearest_distances * weights ) # total travel cost is the sum of the nearest distances weighted by the population weights)
    hospital_cost = lambda_cost * len(selected) # hospital cost is the number of selected locations multiplied by the cost per hospital (lambda_cost)
    
    return travel_cost + hospital_cost