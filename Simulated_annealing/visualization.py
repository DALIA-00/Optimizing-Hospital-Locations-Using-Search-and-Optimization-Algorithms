import matplotlib.pyplot as plt
import numpy as np
import os


def plot_solution( population_points, candidate_locations, solution , filename=None, show=True):
    population_points = np.array(population_points)
    candidate_locations = np.array(candidate_locations)
    selected = candidate_locations[solution == 1]

    plt.figure(figsize=(8, 8))

    plt.scatter(
        population_points[:, 0],
        population_points[:, 1],
        label="Population")

    plt.scatter(
        candidate_locations[:, 0],
        candidate_locations[:, 1],
        alpha=0.3,
        label="Candidates")

    plt.scatter(
        selected[:, 0],
        selected[:, 1],
        s=150,
        marker="s",
        label="Hospitals"
    )

    plt.legend()

    plt.title("Hospital Location Optimization")

    if filename:
        dirname = os.path.dirname(filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        plt.savefig(filename, bbox_inches="tight")
        plt.close()
    else:
        if show:
            plt.show()
        plt.close()