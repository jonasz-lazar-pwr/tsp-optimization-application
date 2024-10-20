// src/tsp_algorithms/sa/SimulatedAnnealing.h

#ifndef SIMULATED_ANNEALING_H
#define SIMULATED_ANNEALING_H

#include "InitialSolutionTypeSA.h"
#include "InitialTempType.h"
#include "MoveTypeSA.h"
#include "TempDecayType.h"
#include <vector>
#include <nng/nng.h>


// Class representing the Simulated Annealing algorithm for the Traveling Salesman Problem (TSP)
class SimulatedAnnealing {
public:
    // Constructor for the Simulated Annealing algorithm
    SimulatedAnnealing(int duration_ms, int port, const std::vector<std::vector<int>>& dist_matrix,
                       InitialTempType initial_temp_type, TempDecayType temp_decay_type, double alpha, double beta,
                       int steps_per_temp, MoveTypeSA move_type, InitialSolutionTypeSA initial_solution_type);

    // Destructor for the Simulated Annealing algorithm
    ~SimulatedAnnealing();

    // Method to run the Simulated Annealing algorithm
    void run();

private:
    // --- Data Sending ---
    // Sends the current data (elapsed time and current cost) to the server
    void send_data(const std::chrono::steady_clock::time_point &start_time, std::chrono::steady_clock::time_point &last_send_time);

    // --- Solution Initialization ---
    // Initializes the solution based on the specified type (e.g., Random or Greedy)
    void initialize_solution(InitialSolutionTypeSA initial_solution_type);

    // Initializes a random solution (random permutation of cities)
    void initialize_random_solution();

    // Initializes a greedy solution (nearest neighbor heuristic)
    void initialize_greedy_solution();

    // --- Temperature Initialization ---
    // Initializes the temperature
    void initialize_temperature(InitialTempType initial_temp_type);

    // Initializes the temperature based on the average distance
    double init_temp_avg_distance();

    // Initializes the temperature based on the maximum distance
    double init_temp_max_distance();

    // Initializes temperature based on sampled cost differences
    double init_temp_sampling();

    // Checks if the algorithm should terminate based on time or temperature
    bool should_terminate(const std::chrono::steady_clock::time_point& start_time);

    // Updates the best solution if the current solution is better
    void update_best_solution();

    // --- Cost Calculation ---
    // Calculates the total cost of the solution path
    int calculate_cost(const std::vector<int>& solution);

    // --- Neighbor Generation ---
    // Generates a neighbor solution based on the selected method (Swap, Insert, Invert)
    std::vector<int> generate_neighbor(const std::vector<int>& solution);

    // --- Temperature Decay ---
    // Applies the temperature decay based on the selected method (Geometric, Linear, Logarithmic)
    void apply_temperature_decay();

    // --- Random Number Generation Helpers ---
    // Generates a random integer number in the range [min, max]
    int generate_random_number(int min, int max);

    // Generates a random double number in the range [0, 1)
    double generate_random_double();

    // --- NNG Socket ---
    nng_socket sock{};                  // Socket for sending data to the receiver
    int port{};                         // Port number for the receiver

    // --- Member Variables ---
    double temperature{};               // Current temperature
    const int max_duration;             // Maximum allowed duration in milliseconds
    const double alpha;                 // Parameter for geometric decay
    const double beta;                  // Parameter for linear decay
    const int steps_per_temp;           // Steps to perform at each temperature level

    // Selected method for temperature decay
    const TempDecayType temp_decay_type;

    // Selected method for type of move
    const MoveTypeSA move_type;

    // Distance matrix between cities
    const std::vector<std::vector<int>> distances;

    // Current solution and its cost
    std::vector<int> current_solution;
    int current_cost;

    // Best solution found and its cost
    std::vector<int> best_solution;
    int best_cost;
};

#endif // SIMULATED_ANNEALING_H
