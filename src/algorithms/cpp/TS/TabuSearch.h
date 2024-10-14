// src/algorithms/cpp/TS/TabuSearch.h

#ifndef TABU_SEARCH_H
#define TABU_SEARCH_H

#include "TabuList.h"
#include "Neighbor.h"
#include "MoveType.h"
#include "TenureType.h"
#include "TabuListLimitType.h"
#include "InitialSolutionType.h"
#include <vector>
#include <functional>
#include <map>
#include <variant>


// Class representing the Tabu Search algorithm for the Traveling Salesman Problem (TSP)
class TabuSearch {
public:
    // Constructor with parameters including various options for the Tabu Search algorithm
    TabuSearch(int tenure, const std::vector<std::vector<int>>& dist_matrix, MoveType move_type, int duration_ms,
               std::pair<int, int> random_tenure_range = {0, 0}, TenureType tenure_type = TenureType::CONSTANT,
               TabuListLimitType limit_type = TabuListLimitType::N, int custom_limit = 0, int max_neighbors = 100,
               InitialSolutionType initial_solution_type = InitialSolutionType::RANDOM);

    // Method to run the Tabu Search algorithm
    void run();

private:
    // // --- Neighbor Structure ---
    // // A struct representing a neighbor solution and the move (either Swap or 2-opt) that generated it
    // struct Neighbor {
    //     std::vector<int> solution;  // New solution (path)
    //     std::variant<std::pair<int, int>, std::pair<std::pair<int, int>, std::pair<int, int>>> move;  // Move: Swap or 2-opt
    //     int cost;  // Cost of the neighbor solution
    // };
    //
    // // --- Hashing Functions for Moves ---
    // // Hash function for std::pair, used for Swap moves
    // struct hash_pair {
    //     template <typename T1, typename T2>
    //     std::size_t operator()(const std::pair<T1, T2>& p) const {
    //         auto hash1 = std::hash<T1>{}(p.first);
    //         auto hash2 = std::hash<T2>{}(p.second);
    //         return hash1 ^ hash2;
    //     }
    // };
    //
    // // Hash function for std::tuple, used for 2-opt moves
    // struct hash_tuple {
    //     template <typename T1, typename T2, typename T3, typename T4>
    //     std::size_t operator()(const std::tuple<T1, T2, T3, T4>& t) const {
    //         auto hash1 = std::hash<T1>{}(std::get<0>(t));
    //         auto hash2 = std::hash<T2>{}(std::get<1>(t));
    //         auto hash3 = std::hash<T3>{}(std::get<2>(t));
    //         auto hash4 = std::hash<T4>{}(std::get<3>(t));
    //         return hash1 ^ hash2 ^ hash3 ^ hash4;
    //     }
    // };

    // --- Solution Initialization ---
    // Initializes the solution based on the specified type (e.g., Random or Greedy)
    void initialize_solution(InitialSolutionType initial_solution_type);

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

    void generate_swap_neighborhood(const std::vector<int> &current_solution,
                                    std::multimap<int, Neighbor> &sorted_neighborhood);

    void generate_2opt_neighborhood(const std::vector<int> &current_solution,
                                    std::multimap<int, Neighbor> &sorted_neighborhood);

    // Adds a neighbor to the sorted neighborhood map, which is sorted by cost
    void add_neighbor(std::multimap<int, Neighbor>& sorted_neighborhood, const std::vector<int>& new_solution,
                      int neighbor_cost, std::variant<std::pair<int, int>, std::pair<std::pair<int, int>, std::pair<int, int>>> move);

    // --- Tabu Search Logic ---
    // Checks if the algorithm should terminate (based on maximum allowed duration)
    bool should_terminate(const std::chrono::steady_clock::time_point& start_time, int max_duration);

    // Processes a Swap move for a neighbor, updating Tabu List and current solution if valid
    bool process_swap_move(Neighbor& neighbor, TabuList& tabu_list, int& current_cost, std::vector<int>& current_solution, int& best_cost, std::vector<int>& best_solution);

    // Processes a 2-opt move for a neighbor, updating Tabu List and current solution if valid
    bool process_2opt_move(Neighbor& neighbor, TabuList& tabu_list, int& current_cost, std::vector<int>& current_solution, int& best_cost, std::vector<int>& best_solution);

    // Updates the best solution if the current one is better
    void update_best_solution(const std::vector<int>& current_solution, int current_cost, std::vector<int>& best_solution, int& best_cost);

    // --- Aspiration Criteria ---
    // Checks if a solution passes the aspiration criteria (e.g., if it's better than the best found solution)
    bool aspiration_criteria(int current_cost);

    // --- Tabu List Limit Management ---
    // Calculates the limit for the Tabu List based on the type (e.g., N, 3N, sqrt(N), or custom limit)
    int calculate_tabu_list_limit(TabuListLimitType limit_type, int num_cities, int custom_limit) const;

    // --- Member Variables ---
    TabuList tabu_list;  // Tabu List object to manage forbidden moves

    MoveType move_type;  // Type of move (Swap or 2-opt)

    const std::vector<std::vector<int>> distances;  // Distance matrix between cities

    const int max_duration;  // Maximum allowed duration for the algorithm (in milliseconds)

    const int max_neighbors;  // Maximum number of neighbors to generate in each iteration

    std::vector<int> current_solution;  // The current solution (list of cities)
    int current_cost;  // Cost of the current solution

    std::vector<int> best_solution;  // The best solution found during the search
    int best_cost;  // Cost of the best solution
};

#endif // TABU_SEARCH_H
