// src/tsp_algorithms/sa/SimulatedAnnealing.cpp

#include "SimulatedAnnealing.h"
#include <nng/protocol/pair1/pair.h>
#include <random>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>


// --- Constructor ---
/*
 * Initializes the Simulated Annealing algorithm with the given parameters.
 */
SimulatedAnnealing::SimulatedAnnealing(int port, int data_frequency_ms, const std::vector<std::vector<int>>& dist_matrix, int duration_ms,
    InitialTempMethodSA initial_temp_method, InitialSolutionMethodSA initial_solution_method,
    NeighborSelectionMethodSA neighbor_selection_method, int steps_per_temp, double alpha):

    max_duration(duration_ms), data_frequency(data_frequency_ms), alpha(alpha), steps_per_temp(steps_per_temp),
    neighbor_selection_method(neighbor_selection_method), distances(dist_matrix) {

    // Initialize the initial solution based on the specified type.
    initialize_solution(initial_solution_method);
    // Calculate the cost of the initial solution.
    current_cost = calculate_cost(current_solution);
    // Set the current solution as the best one.
    best_solution = current_solution;
    // Set the current cost as the best one.
    best_cost = current_cost;
    // Initialize the temperature based on the specified method.
    initialize_temperature(initial_temp_method);

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
 * Destroys the Simulated Annealing algorithm and closes the NNG socket.
 */
SimulatedAnnealing::~SimulatedAnnealing() {
    nng_close(sock);
}

// --- Main Algorithm Loop ---
/*
 * The main function that runs the Simulated Annealing algorithm.
 * It iterates until the termination condition is met (time).
 */
void SimulatedAnnealing::run() {
    // Start the timer to measure the algorithm's duration.
    auto start_time = std::chrono::steady_clock::now();
    auto last_send_time = start_time;

    // Iteration loop until the termination condition is met.
    while (!should_terminate(start_time)) {

        // Loop for a specified number of steps at the current temperature
        for (int step = 0; step < steps_per_temp; step++) {
            // Generate a new neighbor solution
            std::vector<int> new_solution = generate_neighbor(current_solution);
            int new_cost = calculate_cost(new_solution);

            // Calculate the cost difference between the current and new solutions
            int delta = new_cost - current_cost;

            // Accept the new solution if it is better or with a certain probability
            if (delta < 0 || generate_random_double() < std::exp(-delta / temperature)) {
                current_solution = new_solution;
                current_cost = new_cost;

                // Update the best solution if the new one is better
                update_best_solution();
            }
            // Send the current data, passing start_time and last_send_time by reference
            send_data(start_time, last_send_time);
        }
        // Apply the temperature cooling after a certain number of steps
        apply_temperature_cooling();
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
void SimulatedAnnealing::send_data(const std::chrono::steady_clock::time_point& start_time,
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
void SimulatedAnnealing::save_best_solution_to_file() {
    std::string filename = "data/best_solutions/best_solution_sa.txt";
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
void SimulatedAnnealing::initialize_solution(InitialSolutionMethodSA initial_solution_method) {
    if (initial_solution_method == InitialSolutionMethodSA::RANDOM) {
        initialize_random_solution();
    } else if (initial_solution_method == InitialSolutionMethodSA::GREEDY) {
        initialize_greedy_solution();
    }
}

// --- Random Solution Initialization ---
/*
 * Initializes a random solution (random permutation of cities).
 */
void SimulatedAnnealing::initialize_random_solution() {
    current_solution.resize(distances.size());
    std::iota(current_solution.begin(), current_solution.end(), 0);
    std::shuffle(current_solution.begin(), current_solution.end(), std::mt19937{std::random_device{}()});
}

// --- Greedy Solution Initialization ---
/*
 * Initializes a greedy solution (nearest neighbor heuristic).
 */
void SimulatedAnnealing::initialize_greedy_solution() {
    size_t num_cities = distances.size();
    current_solution.clear();
    current_solution.reserve(num_cities);

    // Start from a random city
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<size_t> dist(0, num_cities - 1);
    size_t current_city = dist(rng);
    current_solution.push_back(current_city);

    std::vector<bool> visited(num_cities, false);
    visited[current_city] = true;

    // Greedy step: choose the closest city
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

// --- Temperature Initialization ---
/*
 * Initializes the temperature based on the selected method.
 */
void SimulatedAnnealing::initialize_temperature(InitialTempMethodSA initial_temp_method) {
    switch (initial_temp_method) {
        case InitialTempMethodSA::AVG:
            temperature = init_temp_avg_distance();
        break;
        case InitialTempMethodSA::MAX:
            temperature = init_temp_max_distance();
        break;
        case InitialTempMethodSA::SAMPLING:
            temperature = init_temp_sampling();
        break;
    }
}

// --- Temperature Initialization Methods ---
/*
 * Initializes the temperature based on the average distance between cities.
 */
double SimulatedAnnealing::init_temp_avg_distance() {
    double total_distance = 0.0;
    int count = 0;
    for (size_t i = 0; i < distances.size(); ++i) {
        for (size_t j = i + 1; j < distances.size(); ++j) {
            total_distance += distances[i][j];
            count++;
        }
    }
    return (total_distance / count) * 0.5;
}

/*
 * Initializes the temperature based on the maximum distance between cities.
 */
double SimulatedAnnealing::init_temp_max_distance() {
    int max_distance = 0;
    for (const auto& row : distances) {
        max_distance = std::max(max_distance, *std::max_element(row.begin(), row.end()));
    }
    return max_distance * 0.5;
}

/*
 * Initializes the temperature based on the sampled cost differences.
 */
double SimulatedAnnealing::init_temp_sampling() {
    std::vector<double> deltas;
    for (int k = 0; k < 100; ++k) {
        std::vector<int> sample = current_solution;
        std::shuffle(sample.begin(), sample.end(), std::mt19937{std::random_device{}()});
        deltas.push_back(std::fabs(calculate_cost(sample) - current_cost));
    }
    double avg_delta = std::accumulate(deltas.begin(), deltas.end(), 0.0) / deltas.size();
    return avg_delta * 0.5;
}

/*
 * Checks if the algorithm should terminate based on the elapsed time or temperature.
 */
bool SimulatedAnnealing::should_terminate(const std::chrono::steady_clock::time_point& start_time) {
    auto current_time = std::chrono::steady_clock::now();
    double elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(current_time - start_time).count();

    // Check if the elapsed time exceeds the maximum duration or if the temperature is below the final temperature
    if (elapsed_time >= max_duration) {
        return true;
    }
    return false;
}

/*
 * Updates the best solution if the current one is better.
 */
void SimulatedAnnealing::update_best_solution() {
    if (current_cost < best_cost) {
        best_solution = current_solution;
        best_cost = current_cost;
    }
}

// --- Cost Calculation ---
/*
 * Calculates the cost of a solution (sum of distances).
 */
int SimulatedAnnealing::calculate_cost(const std::vector<int>& solution) {
    int cost = 0;
    for (size_t i = 0; i < solution.size() - 1; ++i) {
        cost += distances[solution[i]][solution[i + 1]];
    }
    cost += distances[solution.back()][solution.front()];
    return cost;
}

// --- Neighbor Generation ---
/*
 * Generates a neighboring solution based on the selected method (Swap, Insert, Invert)
 */
std::vector<int> SimulatedAnnealing::generate_neighbor(const std::vector<int>& solution) {
    std::vector<int> new_solution = solution;
    int i = generate_random_number(0, solution.size() - 1);
    int j;
    do {
        j = generate_random_number(0, solution.size() - 1);
    } while (i == j);

    switch (neighbor_selection_method) {
        case NeighborSelectionMethodSA::SWAP:
            std::swap(new_solution[i], new_solution[j]);
        break;
        case NeighborSelectionMethodSA::INSERT: {
            int temp = new_solution[i];
            new_solution.erase(new_solution.begin() + i);
            new_solution.insert(new_solution.begin() + j, temp);
            break;
        }
        case NeighborSelectionMethodSA::INVERT:
            if (i > j) std::swap(i, j);
        std::reverse(new_solution.begin() + i, new_solution.begin() + j + 1);
        break;
    }
    return new_solution;
}

// --- Temperature Cooling ---
/*
 * Applies the temperature cooling schedule to decrease the temperature
 */
void SimulatedAnnealing::apply_temperature_cooling() {
    temperature *= alpha;
}

// --- Random Helpers ---
/*
 * Generates a random integer number in the range [min, max].
 */
int SimulatedAnnealing::generate_random_number(int min, int max) {
    static std::mt19937 gen{std::random_device{}()};
    std::uniform_int_distribution<> dist(min, max);
    return dist(gen);
}

/*
 * Generates a random double number in the range [0, 1).
 */
double SimulatedAnnealing::generate_random_double() {
    static std::mt19937 gen{std::random_device{}()};
    std::uniform_real_distribution<> dist(0.0, 1.0);
    return dist(gen);
}
