import random
import math
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
        lamda: Hospital cost parameter, controls the penalty for adding more hospitals
    
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
# DISTANCE MATRIX: Precomputes distances between all population centers and potential hospital sites
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
# SELECTION: Keeps the best solutions (fittest chromosomes)
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
def mutation(chromosome, mutation_prob=0.05):
    """
    Bit-flip mutation: flips each bit with probability specified by mutation_prob.
    This introduces randomness and helps escape local optima.
    
    Args:
        chromosome: Binary list to mutate
        mutation_prob: Probability of flipping each bit (default: 0.05 = 5%)
    
    Returns:
        Mutated chromosome (0→1 or 1→0 for selected bits)
    """
    chromosome = chromosome[:]  # Create a copy to avoid modifying original
    for i in range(100):
        if random.random() < mutation_prob:  # Apply mutation with given probability
            chromosome[i] ^= 1  # XOR: flip the bit (0→1 or 1→0)
    return chromosome