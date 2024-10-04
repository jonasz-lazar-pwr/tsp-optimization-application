# src/tests/test_simulated_annealing.py

import compiled_binaries.SimulatedAnnealing as SA

# Przyklad użycia
dist_matrix = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
sa = SA.SimulatedAnnealing(final_temp=0.1, duration=60.0, dist_matrix=dist_matrix,
                           temp_init_method='AVG', temp_decay_method='GEO', neighbor_method='SWAP',
                           alpha=0.95, beta=0.1, steps_per_temp=100)

final_cost = sa.run()
print("Final Cost:", final_cost)
print("Current Solution:", sa.current_solution)
print("Current Cost:", sa.current_cost)