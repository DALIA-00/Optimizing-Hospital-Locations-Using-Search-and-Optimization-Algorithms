import math
import random
import unittest

import numpy as np

from cost_function import build_distance_matrix, evaluate
from simulated_annealing import (
    generate_neighbor,
    random_solution,
    simulated_annealing,
)


class TestSimulatedAnnealing(unittest.TestCase):

    def test_build_distance_matrix_normal_case(self):
        population_points = [
            (0, 0),
            (3, 4),
        ]
        candidate_locations = [
            (0, 0),
            (6, 8),
        ]

        distances = build_distance_matrix(
            population_points,
            candidate_locations
        )

        expected = np.array(
            [
                [0, 10],
                [5, 5],
            ],
            dtype=float
        )

        np.testing.assert_array_equal(distances, expected)

    def test_evaluate_known_two_hospital_case(self):
        distance_matrix = np.array(
            [
                [0, 10],
                [10, 0],
            ],
            dtype=float
        )
        weights = np.array([1, 1])

        self.assertEqual(
            evaluate(np.array([1, 0]), distance_matrix, weights, 1),
            11.0
        )
        self.assertEqual(
            evaluate(np.array([0, 1]), distance_matrix, weights, 1),
            11.0
        )
        self.assertEqual(
            evaluate(np.array([1, 1]), distance_matrix, weights, 1),
            2.0
        )
        self.assertTrue(
            math.isinf(
                evaluate(np.array([0, 0]), distance_matrix, weights, 1)
            )
        )

    def test_evaluate_weighted_normal_case(self):
        distance_matrix = np.array(
            [
                [2, 6, 8],
                [5, 1, 4],
                [7, 3, 2],
            ],
            dtype=float
        )
        weights = np.array([3, 2, 1])
        solution = np.array([1, 1, 0])

        cost = evaluate(
            solution,
            distance_matrix,
            weights,
            lambda_cost=5
        )

        self.assertEqual(cost, 21.0)

    def test_random_solution_never_empty_for_small_problem(self):
        random.seed(1)

        solution = random_solution(5)

        self.assertEqual(solution.tolist(), [0, 0, 0, 0, 1])
        self.assertEqual(np.sum(solution), 1)

    def test_random_solution_normal_problem_selects_10_to_20_percent(self):
        random.seed(3)

        solution = random_solution(100)
        selected_count = np.sum(solution)

        self.assertEqual(len(solution), 100)
        self.assertGreaterEqual(selected_count, 10)
        self.assertLessEqual(selected_count, 20)

    def test_random_solution_rejects_zero_candidates(self):
        with self.assertRaises(ValueError):
            random_solution(0)

    def test_generate_neighbor_does_not_remove_last_hospital(self):
        random.seed(1)

        neighbor = generate_neighbor(np.array([1, 0, 0]))

        self.assertEqual(neighbor.tolist(), [1, 0, 0])

    def test_single_candidate_edge_case(self):
        distance_matrix = np.array(
            [
                [0],
                [5],
            ],
            dtype=float
        )
        weights = np.array([2, 3])

        random.seed(5)
        np.random.seed(5)

        solution, cost, iterations = simulated_annealing(
            distance_matrix,
            weights,
            lambda_cost=7,
            initial_temperature=10,
            cooling_rate=0.5,
            minimum_temperature=1
        )

        self.assertEqual(solution.tolist(), [1])
        self.assertEqual(cost, 22.0)
        self.assertEqual(iterations, 4)

    def test_simulated_annealing_finds_known_best_solution(self):
        distance_matrix = np.array(
            [
                [0, 10],
                [10, 0],
            ],
            dtype=float
        )
        weights = np.array([1, 1])

        random.seed(2)
        np.random.seed(2)

        solution, cost, iterations = simulated_annealing(
            distance_matrix,
            weights,
            lambda_cost=1,
            initial_temperature=10,
            cooling_rate=0.5,
            minimum_temperature=1
        )

        self.assertEqual(solution.tolist(), [1, 1])
        self.assertEqual(cost, 2.0)
        self.assertEqual(iterations, 4)


if __name__ == "__main__":
    unittest.main()



# Normal distance matrix test
# Normal weighted cost test
# Normal 100-candidate random initialization test
# Known two-hospital cost case
# Known simulated annealing best-solution case
# Edge case: zero candidates raises ValueError
# Edge case: small problem still selects one hospital
# Edge case: neighbor cannot remove the last hospital
# Edge case: one candidate only