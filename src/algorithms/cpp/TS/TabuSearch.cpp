// src/algorithms/cpp/TS/TabuSearch.cpp

#include "TabuSearch.h"
#include "MoveHashUtils.h"
#include <algorithm>
#include <random>
#include <iostream>
#include <numeric>
#include <chrono>
#include <map>
#include <unordered_set>

// --- Constructor ---
/*
 * Constructor initializes the Tabu Search algorithm with the given parameters.
 * - tenure: the length of time a move stays on the Tabu List.
 * - dist_matrix: distance matrix between cities.
 * - move_type: either SWAP or 2-opt.
 * - duration_ms: the maximum allowed runtime in milliseconds.
 * - random_tenure_range: range for random tenure values (for stochastic TS).
 * - tenure_type: type of tenure (CONSTANT or RANDOM).
 * - limit_type: how to calculate the Tabu List size limit (e.g., N, SQRT(N)).
 * - custom_limit: custom size limit for the Tabu List.
 * - max_neighbors: max number of neighbors to generate.
 * - initial_solution_type: type of initial solution (RANDOM or GREEDY).
 */
TabuSearch::TabuSearch(int tenure, const std::vector<std::vector<int>>& dist_matrix, MoveType move_type, int duration_ms,
                       std::pair<int, int> random_tenure_range, TenureType tenure_type, TabuListLimitType limit_type,
                       int custom_limit, int max_neighbors, InitialSolutionType initial_solution_type):
    tabu_list(tenure, random_tenure_range, tenure_type, calculate_tabu_list_limit(limit_type, dist_matrix.size(), custom_limit)),
    move_type(move_type), distances(dist_matrix), max_duration(duration_ms), max_neighbors(max_neighbors) {

    // Initialize the initial solution based on the specified type.
    initialize_solution(initial_solution_type);
    // Calculate the cost of the initial solution.
    current_cost = calculate_cost(current_solution);
    // Set the initial solution as the best one.
    best_solution = current_solution;
    // Set the initial cost as the best cost.
    best_cost = current_cost;
}

// --- Main Algorithm Loop ---
/*
 * The main function that runs the Tabu Search algorithm.
 * Iterates through neighborhoods, evaluating solutions until termination.
 */
void TabuSearch::run() {
    // Start the timer to measure the algorithm's duration.
    auto start_time = std::chrono::steady_clock::now();

    // Main loop until the algorithm exceeds the maximum duration
    while (!should_terminate(start_time, max_duration)) {
        tabu_list.decrement_tenure(); // Decrease tenures of all tabu moves.

        // Generate a neighborhood of possible moves (Swap or 2-opt).
        std::vector<Neighbor> neighborhood = generate_neighborhood(current_solution);

        // Evaluate each neighbor in the neighborhood.
        for (Neighbor &neighbor : neighborhood) {
            // Process the neighbor based on the move type (Swap or 2-opt).
            if (std::holds_alternative<std::pair<int, int>>(neighbor.move)) {
                if (process_swap_move(neighbor, tabu_list, current_cost, current_solution, best_cost, best_solution)) {
                    break;
                }
            } else if (std::holds_alternative<std::pair<std::pair<int, int>, std::pair<int, int>>>(neighbor.move)) {
                if (process_2opt_move(neighbor, tabu_list, current_cost, current_solution, best_cost, best_solution)) {
                    break;
                }
            }
        }
    }

    std::cout << "Finished with best cost: " << best_cost << std::endl;
}

// --- Solution Initialization ---
/*
 * Initializes the solution based on the specified type (e.g., Random or Greedy).
 */
void TabuSearch::initialize_solution(InitialSolutionType initial_solution_type) {
    if (initial_solution_type == InitialSolutionType::RANDOM) {
        initialize_random_solution();
    } else if (initial_solution_type == InitialSolutionType::GREEDY) {
        initialize_greedy_solution();
    }
}

// --- Random Solution Initialization ---
/*
 * Initializes a random solution (random permutation of cities).
 */
void TabuSearch::initialize_random_solution() {
    current_solution.resize(distances.size());
    std::iota(current_solution.begin(), current_solution.end(), 0);
    std::shuffle(current_solution.begin(), current_solution.end(), std::mt19937{std::random_device{}()});
}

// --- Greedy Solution Initialization ---
/*
 * Initializes a greedy solution (nearest neighbor heuristic).
 */
void TabuSearch::initialize_greedy_solution() {
    size_t num_cities = distances.size();
    current_solution.clear();
    current_solution.reserve(num_cities);

    // Zaczynamy od losowego miasta
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<size_t> dist(0, num_cities - 1);
    size_t current_city = dist(rng);
    current_solution.push_back(current_city);

    std::vector<bool> visited(num_cities, false);
    visited[current_city] = true;

    // Zachłannie wybieramy najbliższe miasto
    for (size_t step = 1; step < num_cities; ++step) {
        int closest_city = -1;
        int min_distance = std::numeric_limits<int>::max();

        for (size_t city = 0; city < num_cities; ++city) {
            if (!visited[city] && distances[current_city][city] < min_distance) {
                closest_city = city;
                min_distance = distances[current_city][city];
            }
        }

        current_solution.push_back(closest_city);
        visited[closest_city] = true;
        current_city = closest_city;
    }
}

// --- Cost Calculation ---
/*
 * Calculates the total cost (distance) for a given solution (tour).
 */
int TabuSearch::calculate_cost(const std::vector<int>& solution) {
    int cost = 0;
    for (size_t i = 0; i < solution.size() - 1; ++i) {
        cost += distances[solution[i]][solution[i + 1]];
    }
    // Add the distance from the last city back to the starting city.
    cost += distances[solution.back()][solution.front()];
    return cost;
}

// --- Neighborhood Generation ---
/*
 * Generates the neighborhood of solutions using either Swap or 2-opt moves.
 */
std::vector<Neighbor> TabuSearch::generate_neighborhood(const std::vector<int>& current_solution) {
    std::multimap<int, Neighbor> sorted_neighborhood; // Sorted neighborhood by cost

    // Generate the neighborhood based on the move type (Swap or 2-opt).
    if (move_type == MoveType::SWAP) {
        generate_swap_neighborhood(current_solution, sorted_neighborhood);
    } else if (move_type == MoveType::OPT_2) {
        generate_2opt_neighborhood(current_solution, sorted_neighborhood);
    }

    // Convert the sorted neighborhood to a vector of neighbors.
    std::vector<Neighbor> neighborhood;
    for (const auto& entry : sorted_neighborhood) {
        neighborhood.push_back(entry.second);
    }
    return neighborhood;
}

// --- Swap Neighborhood Generation ---
/*
 * Generates the neighborhood using Swap moves.
 */
void TabuSearch::generate_swap_neighborhood(const std::vector<int>& current_solution, std::multimap<int, Neighbor>& sorted_neighborhood) {
    std::mt19937 rng(std::random_device{}()); // Random number generator
    std::unordered_set<std::pair<int, int>, hash_pair> added_swap_moves; // Set to track unique swap moves
    std::uniform_int_distribution<size_t> dist(0, current_solution.size() - 1); // Random index selection

    for (int k = 0; k < max_neighbors; ++k) {
        size_t i = dist(rng); // Randomly select the first city
        size_t j = dist(rng); // Randomly select the second city

        // Check that cities are different
        while (i == j) { j = dist(rng); }

        // Ensure that the pair (i, j) is unique
        if (added_swap_moves.find({std::min(i, j), std::max(i, j)}) != added_swap_moves.end()) {
            --k; // Skip this move and generate a new one
            continue;
        }

        std::vector<int> new_solution = current_solution;
        std::swap(new_solution[i], new_solution[j]); // Swap the cities

        int neighbor_cost = calculate_cost(new_solution); // Calculate the cost

        // Add the neighbor to the sorted neighborhood
        add_neighbor(sorted_neighborhood, new_solution, neighbor_cost, std::make_pair(current_solution[i], current_solution[j]));

        // Add the move to the set to avoid duplicates
        added_swap_moves.insert({std::min(i, j), std::max(i, j)});
    }
}

// --- 2-opt Neighborhood Generation ---
/*
 * Generates the neighborhood using 2-opt moves.
 */
void TabuSearch::generate_2opt_neighborhood(const std::vector<int>& current_solution, std::multimap<int, Neighbor>& sorted_neighborhood) {
    std::mt19937 rng(std::random_device{}()); // Random number generator
    std::unordered_set<std::tuple<int, int, int, int>, hash_tuple> added_2opt_moves; // Set to track unique 2-opt moves
    std::uniform_int_distribution<size_t> dist(0, current_solution.size() - 1); // Random index selection

    for (int k = 0; k < max_neighbors; ++k) {
        size_t i = dist(rng); // Randomly select the first edge
        size_t j = dist(rng); // Randomly select the second edge

        // Ensure that the edges are different and not adjacent
        while (i >= j || (j - i) < 2 || (j == current_solution.size() - 1 && i == 0)) {
            i = dist(rng);
            j = dist(rng);
        }

        // Ensure that the pair (i, i+1, j, j+1) is unique
        if (added_2opt_moves.find({i, i + 1, j, (j + 1) % current_solution.size()}) != added_2opt_moves.end()) {
            --k; // Skip this move and generate a new one
            continue;
        }

        std::vector<int> new_solution = current_solution;

        // Reverse the segment between the two edges
        if (j == current_solution.size() - 1) {
            std::reverse(new_solution.begin() + (j + 1) % current_solution.size(), new_solution.begin() + i + 1);
        } else {
            std::reverse(new_solution.begin() + i + 1, new_solution.begin() + (j + 1) % current_solution.size());
        }

        int neighbor_cost = calculate_cost(new_solution); // Calculate the cost

        // Add the neighbor to the sorted neighborhood
        add_neighbor(sorted_neighborhood, new_solution, neighbor_cost,
            std::make_pair(std::make_pair(current_solution[i], current_solution[i + 1]),
                std::make_pair(current_solution[j], current_solution[(j + 1) % current_solution.size()])));

        // Add the move to the set to avoid duplicates
        added_2opt_moves.insert({i, i + 1, j, (j + 1) % current_solution.size()});
    }
}

// --- Add Neighbor ---
/*
 * Helper function to add a neighbor to the sorted neighborhood.
 */
void TabuSearch::add_neighbor(std::multimap<int, Neighbor>& sorted_neighborhood,
                              const std::vector<int>& new_solution, int neighbor_cost,
                              std::variant<std::pair<int, int>, std::pair<std::pair<int, int>, std::pair<int, int>>> move) {
    // Create a new Neighbor object and insert it into the sorted neighborhood.
    Neighbor neighbor = { new_solution, move, neighbor_cost };
    sorted_neighborhood.insert({neighbor_cost, neighbor});
}

// --- Termination Condition ---
/*
 * Checks if the algorithm should terminate based on elapsed time.
 */
bool TabuSearch::should_terminate(const std::chrono::steady_clock::time_point& start_time, int max_duration) {
    auto current_time = std::chrono::steady_clock::now();
    auto elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(current_time - start_time).count();

    if (elapsed_time >= max_duration) {
        std::cout << "Elapsed time: " << elapsed_time << " ms, stopping the algorithm." << std::endl;
        return true;
    }
    return false;
}

// --- Swap Move Processing ---
/*
 * Process a Swap move: checks if it's tabu and if aspiration criteria are met.
 * Updates the current solution and Tabu List if the move is valid.
 */
bool TabuSearch::process_swap_move(Neighbor& neighbor, TabuList& tabu_list, int& current_cost, std::vector<int>& current_solution, int& best_cost, std::vector<int>& best_solution) {
    auto [city1, city2] = std::get<std::pair<int, int>>(neighbor.move);

    // If the move is not tabu or meets aspiration criteria, apply it.
    if (!tabu_list.is_tabu(city1, city2) || aspiration_criteria(neighbor.cost)) {

        current_solution = neighbor.solution;
        current_cost = neighbor.cost;
        tabu_list.add_move(city1, city2);

        // Update the best solution if the new one is better.
        update_best_solution(current_solution, current_cost, best_solution, best_cost);
        return true; // Found a better solution, break the loop.
    }
    return false; // No better solution found
}

// --- 2-opt Move Processing ---
/*
 * Process a 2-opt move: checks if it's tabu and if aspiration criteria are met.
 * Updates the current solution and Tabu List if the move is valid.
 */
bool TabuSearch::process_2opt_move(Neighbor& neighbor, TabuList& tabu_list, int& current_cost, std::vector<int>& current_solution, int& best_cost, std::vector<int>& best_solution) {
    auto [edge1, edge2] = std::get<std::pair<std::pair<int, int>, std::pair<int, int>>>(neighbor.move);

    bool edge1_is_tabu = tabu_list.is_tabu(edge1.first, edge1.second);
    bool edge2_is_tabu = tabu_list.is_tabu(edge2.first, edge2.second);

    // Apply the move if at least one of the edges is not tabu or aspiration criteria are met.
    if ((!edge1_is_tabu || !edge2_is_tabu) || aspiration_criteria(neighbor.cost)) {

        current_solution = neighbor.solution;
        current_cost = neighbor.cost;

        if (!edge1_is_tabu) {
            tabu_list.add_move(edge1.first, edge1.second);
        }
        if (!edge2_is_tabu) {
            tabu_list.add_move(edge2.first, edge2.second);
        }

        // Update the best solution if the new one is better.
        update_best_solution(current_solution, current_cost, best_solution, best_cost);
        return true; // Found a better solution, break the loop.
    }
    return false; // No better solution found
}

// --- Best Solution Update ---
/*
 * Updates the best solution and best cost if the current solution is better.
 */
void TabuSearch::update_best_solution(const std::vector<int>& current_solution, int current_cost, std::vector<int>& best_solution, int& best_cost) {
    if (current_cost < best_cost) {
        best_solution = current_solution;
        best_cost = current_cost;
        std::cout << "New best solution: " << best_cost << std::endl;
    }
}

// --- Aspiration Criteria ---
/*
 * Aspiration criteria check: determines if a move should be accepted based on the current cost.
 */
bool TabuSearch::aspiration_criteria(int current_cost) {
    return current_cost < best_cost;
}

// --- Tabu List Limit Calculation ---
/*
 * Calculates the Tabu List size limit based on the specified limit type.
 */
int TabuSearch::calculate_tabu_list_limit(TabuListLimitType limit_type, int num_cities, int custom_limit) const {
    switch (limit_type) {
        case TabuListLimitType::N:
            return num_cities;
        case TabuListLimitType::SQRT_N:
            return static_cast<int>(std::ceil(std::sqrt(num_cities)));
        case TabuListLimitType::THREE_N:
            return 3 * num_cities;
        case TabuListLimitType::N_SQUARED:
            return num_cities * num_cities;
        case TabuListLimitType::CUSTOM:
            return custom_limit; // Custom value provided by the user
        default:
            return num_cities; // Default value is number of cities
    }
}
