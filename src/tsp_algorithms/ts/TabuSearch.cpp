// src/tsp_algorithms/ts/TabuSearch.cpp

#include "TabuSearch.h"
#include "NeighborSelectionMethodTS.h"
#include "MoveHashUtils.h"
#include <nng/protocol/pair1/pair.h>
#include <iostream>
#include <chrono>
#include <unordered_set>
#include <fstream>
#include <vector>
#include <string>


// --- Constructor ---
/*
 * Initializes the Tabu Search algorithm with the given parameters.
 */
TabuSearch::TabuSearch(int port, int data_frequency_ms, const std::vector<std::vector<int>>& dist_matrix, int duration_ms,
    InitialSolutionMethodTS initial_solution_method, NeighborSelectionMethodTS neighbor_selection_method,
    int max_neighbors, TabuListLimitMethodTS tabu_list_limit_method, int tabu_list_custom_limit,
    TenureTypeTS tenure_type, int constant_tenure, std::pair<int, int> random_tenure_range):

    max_duration(duration_ms), data_frequency(data_frequency_ms), max_neighbors(max_neighbors),
    tabu_list(constant_tenure, random_tenure_range, tenure_type, calculate_tabu_list_limit(tabu_list_limit_method, dist_matrix.size(), tabu_list_custom_limit)),
    neighbor_selection_method(neighbor_selection_method), distances(dist_matrix) {

    // Initialize the initial solution based on the specified type.
    initialize_solution(initial_solution_method);
    // Calculate the cost of the initial solution.
    current_cost = calculate_cost(current_solution);
    // Set the initial solution as the best one.
    best_solution = current_solution;
    // Set the initial cost as the best cost.
    best_cost = current_cost;

    // NNG socket initialization
    if (nng_pair1_open(&sock) != 0) {
        std::cout << "Failed to open NNG socket." << std::endl;
    }

    // Create the address using the specified port
    std::string address = "tcp://127.0.0.1:" + std::to_string(port);
    if (nng_dial(sock, address.c_str(), NULL, 0) != 0) {
        std::cout << "Failed to connect NNG socket." << std::endl;
    }
}

// --- Destructor ---
/*
 * Destroys the Tabu Search algorithm and closes the NNG socket.
 */
TabuSearch::~TabuSearch() {
    nng_close(sock);
}

// --- Main Algorithm Loop ---
/*
 * The main function that runs the Tabu Search algorithm.
 * Iterates through neighborhoods, evaluating solutions until termination (time).
 */
void TabuSearch::run() {
    // Start the timer to measure the algorithm's duration.
    auto start_time = std::chrono::steady_clock::now();
    auto last_send_time = start_time;

    // Main loop until the algorithm exceeds the maximum duration
    while (!should_terminate(start_time)) {
        // Decrease tenures of all tabu moves.
        tabu_list.decrement_tenure();

        // Generate a neighborhood of possible moves (Swap or 2-opt).
        std::vector<Neighbor> neighborhood = generate_neighborhood(current_solution);

        // Evaluate each neighbor in the neighborhood.
        for (Neighbor &neighbor : neighborhood) {
            // Process the neighbor based on the move type (Swap or 2-opt).
            if (std::holds_alternative<std::pair<int, int>>(neighbor.move)) {
                if (process_swap_move(neighbor)) {

                    // Send the current data, passing start_time and last_send_time by reference
                    send_data(start_time, last_send_time);
                    break;
                }
            } else if (std::holds_alternative<std::pair<std::pair<int, int>, std::pair<int, int>>>(neighbor.move)) {
                if (process_2opt_move(neighbor)) {

                    // Send the current data, passing start_time and last_send_time by reference
                    send_data(start_time, last_send_time);
                    break;
                }
            }
        }
    }
    // Send the final data to indicate the end of the algorithm
    std::string eof_message = "EOF";
    nng_send(sock, const_cast<char*>(eof_message.c_str()), eof_message.size(), 0);

    save_best_solution_to_file();
}

// --- Data Sending ---
/*
 * Sends the current data (elapsed time, current cost and solution).
 */
void TabuSearch::send_data(const std::chrono::steady_clock::time_point& start_time,
                                   std::chrono::steady_clock::time_point& last_send_time) {
    // Check if it is time to send the data
    auto current_time = std::chrono::steady_clock::now();
    auto elapsed_since_last_send = std::chrono::duration_cast<std::chrono::milliseconds>(current_time - last_send_time).count();

    // Send the data if the elapsed time is greater or equal to the data frequency
    if (elapsed_since_last_send >= data_frequency) {
        auto elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(current_time - start_time).count();
        last_send_time = current_time;

        // Convert the current solution to a string
        std::stringstream solution_stream;
        for (size_t i = 0; i < current_solution.size(); ++i) {
            solution_stream << current_solution[i];
            if (i != current_solution.size() - 1) {
                solution_stream << ",";
            }
        }

        // Send the data through the NNG socket
        std::string message = std::to_string(elapsed_time) + " " + std::to_string(best_cost) + " " + std::to_string(current_cost) + " " + solution_stream.str();
        if (nng_send(sock, const_cast<char*>(message.c_str()), message.size(), 0) != 0) {
            std::cerr << "Error: Failed to send message: " << message << std::endl;
        }
    }
}

// --- Best Solution Saving ---
/*
 * Saves the best solution to a file.
 * Each city is written on a separate line, followed by the "EOF" marker.
 */
void TabuSearch::save_best_solution_to_file() {
    std::string filename = "data/best_solutions/best_solution_ts.txt";
    std::ofstream file(filename);
    if (file.is_open()) {
        for (int city : best_solution) {
            file << city << "\n";
        }
        file << "EOF" << std::endl;  // Znacznik końca trasy
        file.close();
    } else {
        std::cerr << "Error: Could not open file " << filename << " for writing." << std::endl;
    }
}

// --- Solution Initialization ---
/*
 * Initializes the solution based on the specified type (e.g., Random or Greedy).
 */
void TabuSearch::initialize_solution(InitialSolutionMethodTS initial_solution_method) {
    if (initial_solution_method == InitialSolutionMethodTS::RANDOM) {
        initialize_random_solution();
    } else if (initial_solution_method == InitialSolutionMethodTS::GREEDY) {
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
    if (neighbor_selection_method == NeighborSelectionMethodTS::SWAP) {
        generate_swap_neighborhood(current_solution, sorted_neighborhood);
    } else if (neighbor_selection_method == NeighborSelectionMethodTS::OPT_2) {
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
bool TabuSearch::should_terminate(const std::chrono::steady_clock::time_point& start_time) {
    auto current_time = std::chrono::steady_clock::now();
    auto elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(current_time - start_time).count();

    if (elapsed_time >= max_duration) {
        return true;
    }
    return false;
}

// --- Swap Move Processing ---
/*
 * Process a Swap move: checks if it's tabu and if aspiration criteria are met.
 * Updates the current solution and Tabu List if the move is valid.
 */
bool TabuSearch::process_swap_move(Neighbor& neighbor) {
    auto [city1, city2] = std::get<std::pair<int, int>>(neighbor.move);

    // If the move is not tabu or meets aspiration criteria, apply it.
    if (!tabu_list.is_tabu(city1, city2) || aspiration_criteria(neighbor.cost)) {

        current_solution = neighbor.solution;
        current_cost = neighbor.cost;
        tabu_list.add_move(city1, city2);

        // Update the best solution if the new one is better.
        update_best_solution();
        return true; // Found a better solution, break the loop.
    }
    return false; // No better solution found
}

// --- 2-opt Move Processing ---
/*
 * Process a 2-opt move: checks if it's tabu and if aspiration criteria are met.
 * Updates the current solution and Tabu List if the move is valid.
 */
bool TabuSearch::process_2opt_move(Neighbor& neighbor) {
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
        update_best_solution();
        return true; // Found a better solution, break the loop.
    }
    return false; // No better solution found
}

// --- Best Solution Update ---
/*
 * Updates the best solution and best cost if the current solution is better.
 */
void TabuSearch::update_best_solution() {
    if (current_cost < best_cost) {
        best_solution = current_solution;
        best_cost = current_cost;
        // std::cout << "New best solution: " << best_cost << std::endl;
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
int TabuSearch::calculate_tabu_list_limit(TabuListLimitMethodTS tabu_list_limit_method, int num_cities, int tabu_list_custom_limit) const {
    switch (tabu_list_limit_method) {
        case TabuListLimitMethodTS::N:
            return num_cities;
        case TabuListLimitMethodTS::SQRT_N:
            return static_cast<int>(std::ceil(std::sqrt(num_cities)));
        case TabuListLimitMethodTS::THREE_N:
            return 3 * num_cities;
        case TabuListLimitMethodTS::N_SQUARED:
            return num_cities * num_cities;
        case TabuListLimitMethodTS::CUSTOM:
            return tabu_list_custom_limit; // Custom value provided by the user
        default:
            return num_cities; // Default value is number of cities
    }
}
