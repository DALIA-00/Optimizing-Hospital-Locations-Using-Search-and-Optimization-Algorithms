import numpy as np
import random
import math

from cost_function import evaluate

def random_solution(num_candidates):

    if num_candidates <= 0:
        raise ValueError("num_candidates must be positive")

    solution = np.zeros( num_candidates, dtype=int)

    # Start with about 10-20% of candidate hospitals selected.
    # For small test cases, keep at least one hospital selected.
    min_selected = max(1, math.ceil(0.10 * num_candidates))
    max_selected = max( min_selected, math.floor(0.20 * num_candidates))

    k = random.randint(min_selected, max_selected) # number of hospitals to select randomly between 10-20% of total candidates
    selected = random.sample(range(num_candidates), k) # randomly select k unique indices from the range of candidate locations
    solution[selected] = 1 # set the selected indices in the solution array to 1 (indicating those candidate locations are selected as hospitals)

    return solution


def generate_neighbor(solution):
    neighbor = solution.copy()

    idx = random.randint( 0, len(solution) - 1) # randomly select an index in the solution array
    neighbor[idx] = 1 - neighbor[idx] # flip the value at the selected index (if it was 0, it becomes 1; if it was 1, it becomes 0)

    # Do not allow a solution with zero hospitals.
    if np.sum(neighbor) == 0:
        neighbor[idx] = 1

    return neighbor


def simulated_annealing(
    distance_matrix,
    weights,
    lambda_cost,
    initial_temperature=1000,
    cooling_rate=0.95,
    minimum_temperature=1
):

    current_solution = random_solution(distance_matrix.shape[1]) 
    # generate a random initial solution with the same number of candidate locations as columns in the distance matrix

    current_cost = evaluate(
        current_solution,
        distance_matrix,
        weights,
        lambda_cost
    )

    best_solution = current_solution.copy()
    best_cost = current_cost

    T = initial_temperature
    iteration = 0

    while T > minimum_temperature:

        neighbor = generate_neighbor(current_solution) # generate a neighboring solution by flipping one random bit in the current solution

        neighbor_cost = evaluate( neighbor, distance_matrix, weights, lambda_cost ) # evaluate the cost of the neighboring solution

        delta = (neighbor_cost - current_cost) # calculate the change in cost between the neighbor and current solution

        if delta < 0:
            current_solution = neighbor
            current_cost = neighbor_cost
        else:
            probability = math.exp( -delta / T ) # calculate the probability of accepting a worse solution based on the cost difference and current temperature

            if random.random() < probability:
                current_solution = neighbor
                current_cost = neighbor_cost

        if current_cost < best_cost:
            best_solution = current_solution.copy()
            best_cost = current_cost

        T *= cooling_rate
        iteration += 1

    return ( best_solution, best_cost, iteration)