import plotting
import random
import Experiments
import ga

# ============================================================================
# PARAMETERS: Initialize problem data with random locations and demand weights
# ============================================================================
# Generate 100 random population center locations (x, y coordinates)
populations = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(100)]
# Generate random population demand weights for each location (1-10 people)
weights = [random.randint(1, 10) for _ in range(100)]
# Generate 100 random potential hospital site locations (x, y coordinates)
freelocations = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(100)]

# ============================================================================
# MAIN PROGRAM: Run experiments and display results
# ============================================================================
print('='*70)
print('Genetic Algorithm for Hospital Location Problem')
print('='*70)

# ============================================================================
# EXPERIMENT 1: Test different lambda (cost weight) parameter values
# ============================================================================
print('-'*25 + 'Lambda Parameter Results' + '-'*25)
# Run experiment 1 with lambda values: 1, 10, 50, 100
summary1, bests1 = Experiments.exp1(populations, weights, freelocations)
# Print detailed per-run results
plotting.print_run_table(summary1, 'lamda')
print('\n\n')

# Print summary statistics (averages and variance)
plotting.print_summary(summary1, 'lamda')
# Visualize hospital locations for each lambda value
plotting.plot_results(populations, freelocations, bests1, [1, 10, 50, 100], 'lamda')
print('\n\n')

# ============================================================================
# EXPERIMENT 2: Test different mutation probability parameter values
# ============================================================================
print('-'*25 + 'Mutation Probability Parameter Results' + '-'*25)
# Run experiment 2 with mutation probabilities: 0.01, 0.05, 0.10, 0.20
summary2, bests2 = Experiments.exp2(populations, weights, freelocations)
# Print detailed per-run results
plotting.print_run_table(summary2, 'mutation_prob')
print('\n\n')

# Print summary statistics (averages and variance)
plotting.print_summary(summary2, 'mutation_prob')
# Visualize hospital locations for each mutation probability value
plotting.plot_results(populations, freelocations, bests2, [0.01, 0.05, 0.10, 0.20], 'mutation_prob')