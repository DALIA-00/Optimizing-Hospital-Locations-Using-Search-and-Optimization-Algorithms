import ga
import time
import statistics
import random


# Experiment 1: Tests different lambda values (cost weight parameters)
def exp1(populations, weights, freelocations):
    bests = []
    summary = {}
    distances = ga.distance_function(populations, freelocations)

    # Test with different lambda values
    for lamda in [1, 10, 50, 100]:
        cost = 0
        hospitalnumbers = 0
        avg_run_time = 0
        costs_list = []
        run_results = []  # stores per-run data for the table

        # Run 5 iterations for each lambda
        for run in range(1, 6):
            # Initialize population with random binary chromosomes
            chromosomes = [[random.randint(0, 1) for _ in range(100)] for _ in range(200)]
            best_sol = (float('inf'), None)

            start = time.time()

            # Run genetic algorithm for 100 generations
            for gen in range(100):
                # Calculate cost for each chromosome
                totalcost = [ga.cost_function(chromosomes[g], weights, distances, lamda) for g in range(200)]
                # Select top 100 individuals
                best_100 = ga.selection(chromosomes, totalcost)

                # Create new offspring through crossover
                new_children = []
                for j in range(0, 100, 2):
                    c1, c2 = ga.crossover(best_100[j][1], best_100[j + 1][1])
                    new_children.append(c1)
                    new_children.append(c2)

                # Combine selected individuals with offspring
                new_generation = [pair[1] for pair in best_100] + new_children
                # Apply mutation to create new population
                chromosomes = [ga.mutation(new_generation[k]) for k in range(200)]

                # Track the best solution found
                if best_100[0][0] < best_sol[0]:
                    best_sol = (best_100[0][0], best_100[0][1])

            end = time.time()
            runtime = end - start

            # Collect results from this run
            best_cost, best_chr = best_sol
            cost += best_cost
            costs_list.append(best_cost)
            hospitalnumbers += sum(best_chr)
            avg_run_time += runtime

            # Store per-run result for the table
            run_results.append({
                "run": run,
                "best_cost": best_cost,
                "hospitals": sum(best_chr),
                "runtime": runtime
            })

        bests.append(best_chr)

        # Calculate averages and statistics for this lambda
        summary[lamda] = {
            "avg_cost": cost / 5,
            "avg_hospitals": hospitalnumbers / 5,
            "avg_runtime": avg_run_time / 5,
            "variance": statistics.variance(costs_list),
            "runs": run_results  # per-run data attached here
        }

    return summary, bests


# Experiment 2: Tests different mutation probabilities
def exp2(populations, weights, freelocations):
    bests = []
    summary = {}
    distances = ga.distance_function(populations, freelocations)
    lamda = 10  # fixed lambda value for this experiment

    # Test with different mutation probabilities
    for mutation_prob in [0.01, 0.05, 0.10, 0.20]:
        cost = 0
        hospitalnumbers = 0
        avg_run_time = 0
        costs_list = []
        run_results = []

        # Run 5 iterations for each mutation probability
        for run in range(1, 6):
            # Initialize population with random binary chromosomes
            chromosomes = [[random.randint(0, 1) for _ in range(100)] for _ in range(200)]
            best_sol = (float('inf'), None)

            start = time.time()

            # Run genetic algorithm for 100 generations
            for gen in range(100):
                # Calculate cost for each chromosome
                totalcost = [ga.cost_function(chromosomes[g], weights, distances, lamda) for g in range(200)]
                # Select top 100 individuals
                best_100 = ga.selection(chromosomes, totalcost)

                # Create new offspring through crossover
                new_children = []
                for j in range(0, 100, 2):
                    c1, c2 = ga.crossover(best_100[j][1], best_100[j + 1][1])
                    new_children.append(c1)
                    new_children.append(c2)

                # Combine selected individuals with offspring
                new_generation = [pair[1] for pair in best_100] + new_children
                # Apply mutation with variable probability
                chromosomes = [ga.mutation(new_generation[k], mutation_prob) for k in range(200)]

                # Track the best solution found
                if best_100[0][0] < best_sol[0]:
                    best_sol = (best_100[0][0], best_100[0][1])

            end = time.time()
            runtime = end - start

            # Collect results from this run
            best_cost, best_chr = best_sol
            cost += best_cost
            costs_list.append(best_cost)
            hospitalnumbers += sum(best_chr)
            avg_run_time += runtime

            # Store per-run result for the table
            run_results.append({
                "run": run,
                "best_cost": best_cost,
                "hospitals": sum(best_chr),
                "runtime": runtime
            })

        bests.append(best_chr)

        # Calculate averages and statistics for this mutation probability
        summary[mutation_prob] = {
            "avg_cost": cost / 5,
            "avg_hospitals": hospitalnumbers / 5,
            "avg_runtime": avg_run_time / 5,
            "variance": statistics.variance(costs_list),
            "runs": run_results
        }

    return summary, bests