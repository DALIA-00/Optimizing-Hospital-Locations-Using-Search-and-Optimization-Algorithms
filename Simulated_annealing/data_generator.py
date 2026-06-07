import random

# Generate random problem instance with population points, weights, and candidate locations for purpose of testing the simulated annealing algorithm. 
#The function takes parameters to specify the number of population points, candidate locations, and the coordinate range for generating random points.

def generate_problem(n_population=100, n_candidates=100, coord_min=0, coord_max=100):
    population_points = [
        (
            random.uniform(coord_min, coord_max),
            random.uniform(coord_min, coord_max)
        )
        for _ in range(n_population)
    ] # generate random coordinates for population points within the specified range

    weights = [
        random.randint(1, 10)
        for _ in range(n_population)
    ] # generate random weights for each population point

    candidate_locations = [
        (
            random.uniform(coord_min, coord_max),
            random.uniform(coord_min, coord_max)
        )
        for _ in range(n_candidates)
    ] # generate random coordinates for candidate locations within the specified range

    return population_points, weights, candidate_locations