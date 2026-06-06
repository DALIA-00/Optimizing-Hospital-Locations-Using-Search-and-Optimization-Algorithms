import random
import math
import statistics
import time
import matplotlib.pyplot as plt
def cost_function(chromosome, weights,distances, lamda):
    total_travel = 0
    hospital_cost = sum(chromosome)
    for i in range(100):
        min_dist = float('inf')
        for j in range(100):
            if chromosome[j] == 1:
                d = distances[i][j]
                if d < min_dist:
                    min_dist = d
        total_travel += weights[i] * min_dist
    return total_travel + hospital_cost * lamda
def distance_function(populations,freelocations):
    distance_matrix = [[0]*100 for _ in range(100)] #2d array
    for i in range(100):    #population
        for j in range(100):    #freelocation
            x1, y1 = populations[i]
            x2, y2 = freelocations[j]
            distance_matrix[i][j]= math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance_matrix

def selection(chromosomes, costs):
    select_pairs = [(costs[i], chromosomes[i]) for i in range(200)]
    select_pairs.sort()
    best_100 = select_pairs[:100]
    return best_100

def crossover(parent1, parent2):
    point = random.randint(1, 99)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return [child1, child2]

def mutation(chromosome):
    chromosome = chromosome[:]
    for i in range(100):
        if random.random() < 0.05:
            chromosome[i] ^= 1
    return chromosome

populations = [(random.uniform(0,100), random.uniform(0,100)) for _ in range(100)]
weights = [random.randint(1,10) for _ in range(100)]
freelocations = [(random.uniform(0,100), random.uniform(0,100)) for _ in range(100)]
distances = distance_function(populations,freelocations)
summary = {}
print('='*78)
print(f"{'λ':>5} | {'Run':>3} | {'Best Cost':>12} | {'Number of Hospitals':>9} | {'runtime(s)':>10}")
print('='*78)
bests=[]
for lamda in [1, 10, 50, 100]:
    
    cost = 0
    hospitalnumbers = 0
    avg_run_time = 0
    costs_list=[]
    for run in range(1, 6):
        chromosomes = [[random.randint(0,1) for _ in range(100)] for _ in range(200)]
        best_sol = (float('inf'), None)
        start=time.time()
        for gen in range(100):
            totalcost = [cost_function(chromosomes[g], weights,distances,lamda) for g in range(200)]
            best_100 = selection(chromosomes, totalcost)
            new_children = []
            for j in range(0, 100, 2):
                c1, c2 = crossover(best_100[j][1], best_100[j+1][1])
                new_children.append(c1)
                new_children.append(c2)
            new_generation = [pair[1] for pair in best_100] + new_children
            chromosomes = [mutation(new_generation[k]) for k in range(200)]

            if best_100[0][0] < best_sol[0]:
                best_sol = (best_100[0][0], best_100[0][1])
        end = time.time()
        runtime = end - start
        
        best_cost, best_chr = best_sol
        cost += best_cost
        costs_list.append(best_cost)
        hospitalnumbers += sum(best_chr)
        avg_run_time += runtime
        print(f"{lamda:>5} | {run:>3} | {best_cost:>12.2f} | {sum(best_chr):>9} | {runtime:>10.3f}")
    bests.append(best_chr)  #just only one chromosome per lamda
    print('-'*78)
    summary[lamda] = {"avg_cost": cost / 5, "avg_hospitals": hospitalnumbers / 5 , "avg_runtime":avg_run_time /5, "variance":statistics.variance(costs_list)}
    
print('='*78)
print("     SUMMARY (average over runs)")
print('='*78)
print(f"{'λ':>5} | {'Avg Cost':>12} | {'Avg Hospitals':>13} | {'avg time':>10} | {'variance':>12}")
print('-'*78)
for lam, values in summary.items():
    print(f"{lam:>5} | {values['avg_cost']:12.2f} | {values['avg_hospitals']:13.1f} | {values['avg_runtime']:10.2f} | {values['variance']:12.2f}")
""""
for l in range (4):
    hosp_x = [freelocations[j][0] for j in range (100) if bests[l][j] == 1]
    hosp_y = [freelocations[j][1] for j in range (100) if bests[l][j]==1]
    pop_x = [populations[i][0] for i in range(100)]
    pop_y = [populations[i][1] for i in range(100)]

    plt.scatter(pop_x, pop_y, c='blue', label='populations')
    plt.scatter(hosp_x, hosp_y, c='red', label='hospitals')
    plt.legend()
    plt.show()
    #fig, axes = plt.subplots(1, 4, figsize=(20, 5))

for l in range(4):
    # your hosp_x, hosp_y, pop_x, pop_y code here
    axes[l].scatter(pop_x, pop_y, c='blue', label='populations')
    axes[l].scatter(hosp_x, hosp_y, c='red', label='hospitals')
    axes[l].set_title(f'λ={[1,10,50,100][l]}, hospitals={sum(bests[l])}')
plt.show()
"""
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
for l in range(4):
    hosp_x = [freelocations[j][0] for j in range(100) if bests[l][j] == 1]
    hosp_y = [freelocations[j][1] for j in range(100) if bests[l][j] == 1]
    pop_x = [populations[i][0] for i in range(100)]
    pop_y = [populations[i][1] for i in range(100)]
    axes[l].scatter(pop_x, pop_y, c='blue', label='populations')
    axes[l].scatter(hosp_x, hosp_y, c='red', label='hospitals')
    axes[l].set_title(f'λ={[1,10,50,100][l]}, hospitals={sum(bests[l])}')
plt.show()