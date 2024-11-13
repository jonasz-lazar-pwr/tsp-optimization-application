// src/tsp_algorithms/ts/TabuSearch.h

#ifndef TABU_SEARCH_H
#define TABU_SEARCH_H

#include "TabuList.h"
#include "Neighbor.h"
#include "NeighborSelectionMethodTS.h"
#include "TenureTypeTS.h"
#include "TabuListLimitMethodTS.h"
#include "InitialSolutionMethodTS.h"
#include <nng/nng.h>


// Class representing the Tabu Search algorithm for the Traveling Salesman Problem (TSP)
class TabuSearch {
public:
    // Constructor with parameters including various options for the Tabu Search algorithm
    TabuSearch(int port, int data_frequency_ms, const std::vector<std::vector<int>>& dist_matrix, int duration_ms,
                InitialSolutionMethodTS initial_solution_method, NeighborSelectionMethodTS neighbor_selection_method,
                int max_neighbors, TabuListLimitMethodTS tabu_list_limit_method, int tabu_list_custom_limit,
                TenureTypeTS tenure_type, int constant_tenure, std::pair<int, int> random_tenure_range);

    // Destructor for the Tabu Search algorithm
    ~TabuSearch();

    // Method to run the Tabu Search algorithm
    void run();

private:
    // --- Data Sending ---
    // Sends the current data (elapsed time and current cost) to the server
    void send_data(const std::chrono::steady_clock::time_point &start_time, std::chrono::steady_clock::time_point &last_send_time);

    // --- Best Solution Saving ---
    // Saves the best solution to a file
    void save_best_solution_to_file();

    // --- Solution Initialization ---
    // Initializes the solution based on the specified type (e.g., Random or Greedy)
    void initialize_solution(InitialSolutionMethodTS initial_solution_method);

    // Initializes a random solution (random permutation of cities)
    void initialize_random_solution();

    // Initializes a greedy solution (nearest neighbor heuristic)
    void initialize_greedy_solution();

    // --- Cost Calculation ---
    // Calculates the cost of a solution (sum of distances between consecutive cities)
    int calculate_cost(const std::vector<int>& solution);

    // --- Neighbor Management ---
    // Generates the neighborhood of a solution, either using Swap or 2-opt moves
    std::vector<Neighbor> generate_neighborhood(const std::vector<int>& current_solution);

    // Generates the neighborhood using Swap moves.
    void generate_swap_neighborhood(const std::vector<int> &current_solution,
                                    std::multimap<int, Neighbor> &sorted_neighborhood);

    // Generates the neighborhood using 2-opt moves.
    void generate_2opt_neighborhood(const std::vector<int> &current_solution,
                                    std::multimap<int, Neighbor> &sorted_neighborhood);

    // Adds a neighbor to the sorted neighborhood map, which is sorted by cost
    void add_neighbor(std::multimap<int, Neighbor>& sorted_neighborhood, const std::vector<int>& new_solution,
                      int neighbor_cost, std::variant<std::pair<int, int>, std::pair<std::pair<int, int>, std::pair<int, int>>> move);

    // --- Tabu Search Logic ---
    // Checks if the algorithm should terminate (based on maximum allowed duration)
    bool should_terminate(const std::chrono::steady_clock::time_point& start_time);

    // Processes a Swap move for a neighbor, updating Tabu List and current solution if valid
    bool process_swap_move(Neighbor& neighbor);

    // Processes a 2-opt move for a neighbor, updating Tabu List and current solution if valid
    bool process_2opt_move(Neighbor& neighbor);

    // Updates the best solution if the current one is better
    void update_best_solution();

    // --- Aspiration Criteria ---
    // Checks if a solution passes the aspiration criteria (e.g., if it's better than the best found solution)
    bool aspiration_criteria(int current_cost);

    // --- Tabu List Limit Management ---
    // Calculates the limit for the Tabu List based on the type (e.g., N, 3N, sqrt(N), or tabu_list_custom_limit)
    int calculate_tabu_list_limit(TabuListLimitMethodTS tabu_list_limit_method, int num_cities, int tabu_list_custom_limit) const;

    // --- NNG Socket ---
    nng_socket sock{};                  // Socket for sendning data to the receiver
    int port{};                         // Port number for the receiver
    int data_frequency;                 // Frequency of sending data to the server in milliseconds

    // --- Member Variables ---
    const int max_duration;             // Maximum allowed duration in milliseconds
    const int max_neighbors;            // Maximum number of neighbors to generate

    // Tabu List object to manage forbidden moves
    TabuList tabu_list;

    // Selected method for type of move
    NeighborSelectionMethodTS neighbor_selection_method;

    // Distance matrix between cities
    const std::vector<std::vector<int>> distances;

    // Current solution and its cost
    std::vector<int> current_solution;
    int current_cost;

    // Best solution found and its cost
    std::vector<int> best_solution;
    int best_cost;
};

#endif // TABU_SEARCH_H
