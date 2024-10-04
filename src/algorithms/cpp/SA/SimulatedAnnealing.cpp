#include "SimulatedAnnealing.h"
#include <cmath>
#include <random>
#include <algorithm>
#include <limits>
#include <iostream>
#include <chrono>

// Konstruktor - inicjalizuje algorytm z podanymi parametrami oraz inicjalizuje rozwiązanie
SimulatedAnnealing::SimulatedAnnealing(double final_temp, double duration,
                                       const std::vector<std::vector<double>>& dist_matrix,
                                       const std::string& temp_init_method, const std::string& temp_decay_method,
                                       const std::string& neighbor_method, double alpha, double beta, int steps_per_temp)
    : final_temperature(final_temp), max_duration(duration),
      distances(dist_matrix), temp_decay_method(temp_decay_method), neighbor_method(neighbor_method),
      alpha(alpha), beta(beta), steps_per_temp(steps_per_temp) {
    // Generowanie początkowego rozwiązania
    initialize_random_solution();
    // Ustawienie temperatury początkowej na podstawie wybranej metody
    initialize_temperature(temp_init_method);
}

// Funkcja uruchamiająca algorytm Symulowanego Wyżarzania
double SimulatedAnnealing::run() {
    auto start_time = std::chrono::steady_clock::now();

    while (temperature > final_temperature) {
        auto current_time = std::chrono::steady_clock::now();
        double elapsed_time = std::chrono::duration_cast<std::chrono::seconds>(current_time - start_time).count();
        
        if (elapsed_time >= max_duration) {
            break;
        }

        // Pętla wykonywania określonej liczby kroków przy danej temperaturze
        for (int step = 0; step < steps_per_temp; step++) {
            std::vector<int> new_solution = generate_neighbor(current_solution);
            double new_cost = calculate_cost(new_solution);

            double delta = new_cost - current_cost;
            
            if (delta < 0 || generate_random_double() < std::exp(-delta / temperature)) {
                current_solution = new_solution;
                current_cost = new_cost;
            }
        }

        // Zmniejszenie temperatury po określonej liczbie iteracji
        apply_temperature_decay();
    }
    return current_cost;
}

// Inicjalizacja początkowego rozwiązania (losowa permutacja)
void SimulatedAnnealing::initialize_random_solution() {
    current_solution.resize(distances.size());
    std::iota(current_solution.begin(), current_solution.end(), 0);
    std::shuffle(current_solution.begin(), current_solution.end(), std::mt19937{std::random_device{}()});
    current_cost = calculate_cost(current_solution);
}

// Inicjalizacja temperatury początkowej
void SimulatedAnnealing::initialize_temperature(const std::string& method) {
    if (method == "AVG") {
        temperature = init_temp_avg_distance();
    } else if (method == "MAX") {
        temperature = init_temp_max_distance();
    } else if (method == "SAMPLE") {
        temperature = init_temp_sampling();
    }
}

// Metoda obliczająca koszt (długość trasy) dla danego rozwiązania
double SimulatedAnnealing::calculate_cost(const std::vector<int>& solution) const {
    double cost = 0.0;
    for (size_t i = 0; i < solution.size() - 1; ++i) {
        cost += distances[solution[i]][solution[i + 1]];
    }
    cost += distances[solution.back()][solution.front()];
    return cost;
}

// Generowanie sąsiedniego rozwiązania na podstawie wybranej metody
std::vector<int> SimulatedAnnealing::generate_neighbor(const std::vector<int>& solution) {
    std::vector<int> new_solution = solution;
    int i = generate_random_number(0, solution.size() - 1);
    int j;
    do {
        j = generate_random_number(0, solution.size() - 1);
    } while (i == j);

    if (neighbor_method == "SWAP") {
        std::swap(new_solution[i], new_solution[j]);
    } else if (neighbor_method == "INSERT") {
        int temp = new_solution[i];
        new_solution.erase(new_solution.begin() + i);
        new_solution.insert(new_solution.begin() + j, temp);
    } else if (neighbor_method == "INVERT") {
        if (i > j) std::swap(i, j);
        std::reverse(new_solution.begin() + i, new_solution.begin() + j + 1);
    }

    return new_solution;
}

// Funkcja pomocnicza do generowania losowej liczby całkowitej
int SimulatedAnnealing::generate_random_number(int min, int max) {
    static std::mt19937 gen{std::random_device{}()};
    std::uniform_int_distribution<> dist(min, max);
    return dist(gen);
}

// Funkcja pomocnicza do generowania losowej liczby zmiennoprzecinkowej w zakresie [0, 1)
double SimulatedAnnealing::generate_random_double() {
    static std::mt19937 gen{std::random_device{}()};
    std::uniform_real_distribution<> dist(0.0, 1.0);
    return dist(gen);
}

// Obniżenie temperatury na podstawie wybranej metody
void SimulatedAnnealing::apply_temperature_decay() {
    if (temp_decay_method == "GEO") {
        temperature *= alpha;
    } else if (temp_decay_method == "LOG") {
        // temperature /= std::log(2.0 + current_iteration);
    } else if (temp_decay_method == "LINE") {
        temperature -= beta * temperature;
    }
}

// Obliczenie średniej różnicy odległości dla inicjalizacji temperatury
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

// Obliczenie maksymalnej odległości dla inicjalizacji temperatury
double SimulatedAnnealing::init_temp_max_distance() {
    double max_distance = 0.0;
    for (const auto& row : distances) {
        max_distance = std::max(max_distance, *std::max_element(row.begin(), row.end()));
    }
    return max_distance * 0.5;
}

// Obliczenie temperatury na podstawie losowej próbki różnic kosztów
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

std::vector<int> SimulatedAnnealing::get_current_solution() const {
    return current_solution;
}