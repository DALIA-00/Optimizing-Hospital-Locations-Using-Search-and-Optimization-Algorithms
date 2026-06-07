import random
import numpy as np
import os

from data_generator import generate_problem
from cost_function import build_distance_matrix
from simulated_annealing import simulated_annealing
from visualization import plot_solution

random.seed(42)
np.random.seed(42)

population_points, weights, candidates = ( generate_problem() )

# ensure plots directory exists (to store visualizations of the solutions for different lambda values)
#create one if it doesn't exist
os.makedirs("plots", exist_ok=True)

distance_matrix = build_distance_matrix( population_points, candidates )

lambda_values = [1, 10, 50, 100]

for lambda_cost in lambda_values:
    solution, cost, iterations = ( simulated_annealing( distance_matrix, weights, lambda_cost  ))

    hospitals = np.sum(solution)

    print("\n-----------------------------")
    print(f"Lambda = {lambda_cost}")
    print("-----------------------------")
    print(f"Hospitals Built: {hospitals}")
    print(f"Final Cost: {cost:.2f}")
    print(f"Iterations: {iterations}")

    plot_solution(
        population_points,
        candidates,
        solution,
        filename=os.path.join(
            "plots",
            f"solution_lambda_{lambda_cost}.png"
        ),
        show=False
    )