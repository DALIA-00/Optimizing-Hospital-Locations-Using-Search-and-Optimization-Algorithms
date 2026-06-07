import random
import math
import statistics
import time
import matplotlib.pyplot as plt

# ============================================================================
# COST FUNCTION: Evaluates the fitness of a solution (chromosome)
# ============================================================================
def cost_function(chromosome, weights, distances, lamda):
    """
    Calculates the total cost of a hospital placement solution.
    
    Args:
        chromosome: Binary list where 1 = hospital location, 0 = no hospital
        weights: Population demand at each location
        distances: Precomputed distance matrix between all locations
        lamda:hospital cost, Controls how much we add more hospitals
    
    Returns:
        Total cost = travel cost + (number of hospitals * λ)
    """
    total_travel = 0
    hospital_cost = sum(chromosome)  # Count number of hospitals in solution
    
    # For each population center, find nearest hospital and calculate the travel cost
    for i in range(100):
        min_dist = float('inf')
        # Find the closest hospital to this population center
        for j in range(100):
            if chromosome[j] == 1:  # j is a hospital location
                d = distances[i][j]
                if d < min_dist:
                    min_dist = d
        total_travel += weights[i] * min_dist  # Weight travel by population demand
    
    return total_travel + hospital_cost * lamda


# ============================================================================================
# DISTANCE MATRIX: Precomputes distances between all hsoptials free locations and populations
# ============================================================================================
def distance_function(populations, freelocations):
    """
    Creates a 2D distance matrix using Euclidean distance formula.
    
    Args:
        populations: List of (x, y) coordinates for population centers (100 points)
        freelocations: List of (x, y) coordinates for potential hospital sites (100 points)
    
    Returns:
        100x100 matrix where matrix[i][j] = distance from population i to site j
    """
    distance_matrix = [[0] * 100 for _ in range(100)]  # 2D array initialization
    
    for i in range(100):  # For each population center
        for j in range(100):  # For each potential hospital location
            x1, y1 = populations[i]
            x2, y2 = freelocations[j]
            # Calculate Euclidean distance
            distance_matrix[i][j] = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return distance_matrix


# ============================================================================
# SELECTION: Keeps the best solutions (fittest chromosome)
# ============================================================================
def selection(chromosomes, costs):
    """
    Selects the top 100 best solutions based on fitness (lowest cost).
    
    Args:
        chromosomes: List of 200 solutions (binary strings of length 100)
        costs: List of 200 corresponding fitness values
    
    Returns:
        List of top 100 (cost, chromosome) tuples sorted by cost (best first)
    """
    # Pair each solution with its cost
    select_pairs = [(costs[i], chromosomes[i]) for i in range(200)]
    # Sort by cost (ascending - lower is better)
    select_pairs.sort()
    # Keep only the best 100 solutions
    best_100 = select_pairs[:100]
    return best_100


# ============================================================================
# CROSSOVER: Creates new solutions by combining parents
# ============================================================================
def crossover(parent1, parent2):
    """
    Single-point crossover: combines two parent solutions at a random point.
    
    Args:
        parent1: First parent chromosome (binary list)
        parent2: Second parent chromosome (binary list)
    
    Returns:
        Two children chromosomes created by swapping genetic material at crossover point
    """
    point = random.randint(1, 99)  # Random crossover point between 1 and 99
    # Child 1: first part of parent1 + second part of parent2
    child1 = parent1[:point] + parent2[point:]
    # Child 2: first part of parent2 + second part of parent1
    child2 = parent2[:point] + parent1[point:]
    return [child1, child2]


# ============================================================================
# MUTATION: Randomly modifies solutions to maintain genetic diversity
# ============================================================================
def mutation(chromosome):
    """
    Bit-flip mutation: flips each bit with 5% probability.
    This introduces randomness and helps escape local optima.
    
    Args:
        chromosome: Binary list to mutate
    
    Returns:
        Mutated chromosome (0→1 or 1→0 for selected bits)
    """
    chromosome = chromosome[:]  # Create a copy to avoid modifying original
    for i in range(100):
        if random.random() < 0.05:  # 5% mutation probability per bit
            chromosome[i] ^= 1  # XOR: flip the bit (0→1 or 1→0)
    return chromosome


# ============================================================================
# MAIN GENETIC ALGORITHM EXECUTION
# ============================================================================

# Initialize problem data: random locations and demand weights
populations = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(100)]
weights = [random.randint(1, 10) for _ in range(100)]
freelocations = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(100)]

# Precompute all distances (avoids recalculation during evolution)
distances = distance_function(populations, freelocations)

# Dictionary to store summary statistics for each λ value
summary = {}

# Print header for results table
print('='*78)
print(f"{'λ':>5} | {'Run':>3} | {'Best Cost':>12} | {'Number of Hospitals':>9} | {'runtime(s)':>10}")
print('='*78)

bests = []  # Store best solution found for each λ value

# ============================================================================
# EXPERIMENT LOOP: Test different λ values 
# ============================================================================
for lamda in [1, 10, 50, 100]:
    cost = 0
    hospitalnumbers = 0
    avg_run_time = 0
    costs_list = []
    
    # Run 5 independent experiments for each λ value
    for run in range(1, 6):
        # Initialize population: 200 random binary chromosomes (each bit = hospital/no hospital)
        chromosomes = [[random.randint(0, 1) for _ in range(100)] for _ in range(200)]
        best_sol = (float('inf'), None)  # Track best solution found so far
        
        # Time the genetic algorithm execution
        start = time.time()
        
        # ====================================================================
        # EVOLUTION: Run genetic algorithm for 100 generations
        # ====================================================================
        for gen in range(100):
            # Step 1: EVALUATION - Calculate fitness for all chromosomes
            totalcost = [cost_function(chromosomes[g], weights, distances, lamda) for g in range(200)]
            
            # Step 2: SELECTION - Keep the best 100 solutions (elitism)
            best_100 = selection(chromosomes, totalcost)
            
            # Step 3: CROSSOVER - Create 100 new offspring from best 100 parents
            new_children = []
            for j in range(0, 100, 2):  # Pair up parents sequentially
                c1, c2 = crossover(best_100[j][1], best_100[j + 1][1])
                new_children.append(c1)
                new_children.append(c2)
            
            # Step 4: CREATE NEW GENERATION - Combine best solutions with new offspring
            new_generation = [pair[1] for pair in best_100] + new_children
            
            # Step 5: MUTATION - Apply mutation to introduce genetic diversity
            chromosomes = [mutation(new_generation[k]) for k in range(200)]
            
            # Step 6: ELITISM - Track the best solution found in this generation
            if best_100[0][0] < best_sol[0]:
                best_sol = (best_100[0][0], best_100[0][1])
        
        end = time.time()
        runtime = end - start
        
        # Extract final best solution and its statistics
        best_cost, best_chr = best_sol
        cost += best_cost
        costs_list.append(best_cost)
        hospitalnumbers += sum(best_chr)  # Count hospitals in best solution
        avg_run_time += runtime
        
        # Print results for this run
        print(f"{lamda:>5} | {run:>3} | {best_cost:>12.2f} | {sum(best_chr):>9} | {runtime:>10.3f}")
    
    bests.append(best_chr)  # Store best solution found for this λ value
    print('-' * 78)
    
    # Calculate and store average statistics for this λ value
    summary[lamda] = {
        "avg_cost": cost / 5,                          # Average cost across 5 runs
        "avg_hospitals": hospitalnumbers / 5,          # Average number of hospitals
        "avg_runtime": avg_run_time / 5,              # Average execution time
        "variance": statistics.variance(costs_list)    # Variance of costs
    }

# ============================================================================
# RESULTS SUMMARY
# ============================================================================
print('=' * 78)
print("     SUMMARY (average over runs)")
print('=' * 78)
print(f"{'λ':>5} | {'Avg Cost':>12} | {'Avg Hospitals':>13} | {'avg time':>10} | {'variance':>12}")
print('-' * 78)

for lam, values in summary.items():
    print(f"{lam:>5} | {values['avg_cost']:12.2f} | {values['avg_hospitals']:13.1f} | {values['avg_runtime']:10.2f} | {values['variance']:12.2f}")

print([sum(b) for b in bests])  # Print hospital counts for each λ

# ============================================================================
# VISUALIZATION: Plot hospital locations for each λ value
# ============================================================================
fig, axes = plt.subplots(1, 4, figsize=(20, 5))

for l in range(4):
    # Extract hospital locations (where chromosome[j] == 1)
    hosp_x = [freelocations[j][0] for j in range(100) if bests[l][j] == 1]
    hosp_y = [freelocations[j][1] for j in range(100) if bests[l][j] == 1]
    
    # Extract all population locations
    pop_x = [populations[i][0] for i in range(100)]
    pop_y = [populations[i][1] for i in range(100)]
    
    # Plot populations (blue) and hospitals (red)
    axes[l].scatter(pop_x, pop_y, c='blue', label='populations')
    axes[l].scatter(hosp_x, hosp_y, c='red', label='hospitals')
    axes[l].set_title(f'λ={[1, 10, 50, 100][l]}, hospitals={sum(bests[l])}')

plt.show()
