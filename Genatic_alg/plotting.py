import matplotlib.pyplot as plt
# ============================================================================
# VISUALIZATION: Plot hospital locations for each parameter values
# ============================================================================

def plot_results(populations, freelocations, bests, param_values, param_name):
    """
    Creates a visualization showing hospital and population locations for each parameter value.
    
    Args:
        populations: List of (x, y) coordinates for population centers
        freelocations: List of (x, y) coordinates for potential hospital sites
        bests: List of best solutions (chromosomes) for each parameter
        param_values: List of parameter values tested (e.g., [1, 10, 50, 100])
        param_name: Name of the parameter being tested (e.g., "lambda", "mutation_prob")
    """
    # Create subplots, one for each parameter value
    fig, axes = plt.subplots(1, len(bests), figsize=(5 * len(bests), 5))

    # Plot results for each parameter value
    for l in range(len(bests)): 
        # Extract hospital locations (where chromosome[j] == 1)
        hosp_x = [freelocations[j][0] for j in range(100) if bests[l][j] == 1]
        hosp_y = [freelocations[j][1] for j in range(100) if bests[l][j] == 1]

        # Extract all population locations
        pop_x = [populations[i][0] for i in range(100)]
        pop_y = [populations[i][1] for i in range(100)]

        # Plot populations (blue) and hospitals (red)
        axes[l].scatter(pop_x, pop_y, c='blue', label='populations')
        axes[l].scatter(hosp_x, hosp_y, c='red', label='hospitals')
        axes[l].set_title(f'{param_name}={param_values[l]}, hospitals={sum(bests[l])}')
        axes[l].legend()

    # Adjust spacing and save the figure
    plt.tight_layout()
    plt.savefig(f'{param_name}_plot.png')
    plt.show()

    
def print_run_table(summary, param_name):
    """
    Prints a detailed table showing results for each individual run.
    
    Args:
        summary: Dictionary containing results for each parameter value
        param_name: Name of the parameter being tested
    """
    print('=' * 78)
    print(f"{param_name:>5} | {'Run':>3} | {'Best Cost':>12} | {'Hospitals':>9} | {'Runtime(s)':>10}")
    print('=' * 78)
    
    # Print results for each parameter and its runs
    for param, values in summary.items():
        for r in values['runs']:
            print(f"{param:>5} | {r['run']:>3} | {r['best_cost']:>12.2f} | {r['hospitals']:>9} | {r['runtime']:>10.3f}")
        # Separator line between different parameters
        print('-' * 78)


def print_summary(summary, param_name):
    """
    Prints a summary table showing averaged results across all runs for each parameter.
    
    Args:
        summary: Dictionary containing results for each parameter value
        param_name: Name of the parameter being tested
    """
    print('=' * 78)
    print("     SUMMARY (average over runs)")
    print('=' * 78)
    print(f"{param_name:>5} | {'Avg Cost':>12} | {'Avg Hospitals':>13} | {'Avg Time':>10} | {'Variance':>12}")
    print('-' * 78)
    
    # Print averaged statistics for each parameter value
    for param, values in summary.items():
        print(f"{param:>5} | {values['avg_cost']:12.2f} | {values['avg_hospitals']:13.1f} | {values['avg_runtime']:10.2f} | {values['variance']:12.2f}")