import random
import numpy as np
import os
import time
import statistics

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

lambda_values = [1, 10, 50, 100] # hospital costs to test with different trade-offs between travel cost and hospital cost

# number of independent runs to average per lambda
runs_per_lambda = 5

# ensure plots directory exists for outputs
os.makedirs("plots", exist_ok=True)

results_csv = os.path.join("plots", "benchmark_results.csv")
with open(results_csv, "w") as f_out:
    f_out.write("lambda,avg_cost,var_cost,avg_hospitals,var_hospitals,avg_time,var_time\n")

for lambda_cost in lambda_values:
    costs = []
    hospitals_built = []
    times = []
    best_overall = None
    best_cost = float('inf')

    for run_idx in range(runs_per_lambda):
        t0 = time.perf_counter()
        solution, cost, iterations = simulated_annealing(distance_matrix, weights, lambda_cost)
        t1 = time.perf_counter()

        runtime = t1 - t0
        hospitals = int(np.sum(solution))

        costs.append(cost)
        hospitals_built.append(hospitals)
        times.append(runtime)

        if cost < best_cost:
            best_cost = cost
            best_overall = solution.copy()

    avg_cost = statistics.mean(costs)
    var_cost = statistics.pvariance(costs)
    avg_hosp = statistics.mean(hospitals_built)
    var_hosp = statistics.pvariance(hospitals_built)
    avg_time = statistics.mean(times)
    var_time = statistics.pvariance(times)

    print("\n-----------------------------")
    print(f"Lambda = {lambda_cost}")
    print("-----------------------------")
    print(f"Runs: {runs_per_lambda}")
    print(f"Avg Hospitals Built: {avg_hosp:.2f}")
    print(f"Avg Cost: {avg_cost:.2f}")
    print(f"Avg Time (s): {avg_time:.4f}")
    print(f"Cost Variance: {var_cost:.4f}")
    print(f"Hospitals Variance: {var_hosp:.4f}")
    print(f"Time Variance: {var_time:.6f}")

    # save best solution visualization for this lambda
    if best_overall is not None:
        plot_solution(
            population_points,
            candidates,
            best_overall,
            filename=os.path.join("plots", f"solution_lambda_{lambda_cost}.png"),
            show=False
        )

    with open(results_csv, "a") as f_out:
        f_out.write(f"{lambda_cost},{avg_cost:.6f},{var_cost:.6f},{avg_hosp:.6f},{var_hosp:.6f},{avg_time:.6f},{var_time:.6f}\n")


# --- Parameter tuning for cooling rate (alpha) on the same dataset ---
alpha_values = [0.90, 0.95, 0.99]
# choose a lambda value for tuning (use the first lambda tested)
tuning_lambda = lambda_values[0] if len(lambda_values) > 0 else 1

print("\n=== Simulated Annealing Cooling Rate Tuning ===")
print(f"Using lambda = {tuning_lambda} and same dataset for all runs")
for alpha in alpha_values:
    t0 = time.perf_counter()
    solution, cost, iterations = simulated_annealing(distance_matrix, weights, tuning_lambda, cooling_rate=alpha)
    t1 = time.perf_counter()
    runtime = t1 - t0

    hospitals = int(np.sum(solution))
    print("\n-----------------------------")
    print(f"alpha = {alpha}")
    print("-----------------------------")
    print(f"Final Cost: {cost:.2f}")
    print(f"Hospitals Built: {hospitals}")
    print(f"Iterations: {iterations}")
    print(f"Runtime (s): {runtime:.4f}")