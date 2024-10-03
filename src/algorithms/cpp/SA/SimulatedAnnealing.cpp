// src/algorithms/cpp/SA/SimulatedAnnealing.cpp

#include "SimulatedAnnealing.h"
#include <iostream>
#include <vector>
#include <cmath>  // std::exp
#include <cstdlib>  // std::rand, std::srand
#include <ctime>  // std::time

SimulatedAnnealing::SimulatedAnnealing(double temp, int iter, const std::vector<std::vector<double>>& dist_matrix)
    : temperature(temp), max_iterations(iter), distances(dist_matrix) {
    std::srand(static_cast<unsigned int>(std::time(nullptr)));  // seed for randomness

    // Initialize current_solution as a sequence of cities 0, 1, 2, ..., n-1
    int num_cities = distances.size();
    current_solution.resize(num_cities);

    for (int i = 0; i < num_cities; ++i) {
        current_solution[i] = i;
    }

    // Optionally print the initial solution for debugging
    std::cout << "Initial solution: ";
    for (int city : current_solution) {
        std::cout << city << " ";
    }
    std::cout << std::endl;

    print_distance_matrix();  // Print distance matrix
}

double SimulatedAnnealing::run() {
    std::cout << "Starting Simulated Annealing..." << std::endl;

    // Inicjalizacja temperatury i iteracji (dodaj logi)
    std::cout << "Initial Temperature: " << temperature << std::endl;
    std::cout << "Max Iterations: " << max_iterations << std::endl;

    // Przykładowa implementacja krokowa algorytmu
    for (int i = 0; i < max_iterations; ++i) {
        // Wywołanie pojedynczej iteracji algorytmu
        iterate();
    }

    // Zwróć wynik końcowy
    std::cout << "Finished Simulated Annealing" << std::endl;
    return calculate_cost(current_solution);
}

// double SimulatedAnnealing::run() {
//     std::cout << "Starting Simulated Annealing..." << std::endl;
//
//     // Inicjalizacja temperatury i iteracji (dodaj logi)
//     std::cout << "Initial Temperature: " << temperature << std::endl;
//     std::cout << "Max Iterations: " << max_iterations << std::endl;
//
//     // Przykładowa implementacja krokowa algorytmu
//     for (int i = 0; i < max_iterations; ++i) {
//         // Loguj każdą iterację (na początku dla kilku iteracji, aby zobaczyć postęp)
//         if (i < 10 || i % 100 == 0) {
//             std::cout << "Iteration: " << i << ", Current Temperature: " << temperature << std::endl;
//         }
//
//         // Symulowana zmiana rozwiązania
//         // (wprowadź logi, by monitorować zmiany w rozwiązaniu i koszcie)
//         double current_cost = calculate_cost(current_solution);  // Loguj koszt trasy
//         std::cout << "Current cost: " << current_cost << std::endl;
//
//         std::vector<int> new_solution = get_neighbor(current_solution);  // Znajdź sąsiada
//         double new_cost = calculate_cost(new_solution);  // Oblicz koszt nowego rozwiązania
//         std::cout << "New cost: " << new_cost << std::endl;
//
//         // Loguj wybór rozwiązania (czy akceptujemy gorsze rozwiązania)
//         if (accept_solution(current_cost, new_cost)) {
//             current_solution = new_solution;
//             std::cout << "Accepted new solution" << std::endl;
//         } else {
//             std::cout << "Rejected new solution" << std::endl;
//         }
//
//         // Schładzaj temperaturę
//         cool_down();
//     }
//
//     // Zwróć wynik końcowy
//     std::cout << "Finished Simulated Annealing" << std::endl;
//     return calculate_cost(current_solution);
// }

void SimulatedAnnealing::cool_down() {
    temperature *= 0.9999;  // Example cooling schedule
}

bool SimulatedAnnealing::accept_solution(double current_cost, double new_cost) {
    if (new_cost < current_cost) return true;
    double acceptance_probability = std::exp((current_cost - new_cost) / temperature);
    return std::rand() / static_cast<double>(RAND_MAX) < acceptance_probability;
}

double SimulatedAnnealing::calculate_cost(const std::vector<int>& solution) {
    std::cout << "Calculating cost for solution..." << std::endl;

    // Sprawdź, czy solution jest puste
    if (solution.empty()) {
        std::cerr << "Error: solution is empty!" << std::endl;
        return -1;
    }

    double total_distance = 0.0;
    for (size_t i = 0; i < solution.size() - 1; ++i) {
        std::cout << "From city " << solution[i] << " to city " << solution[i + 1] << std::endl;

        if (solution[i] >= distances.size() || solution[i + 1] >= distances.size()) {
            std::cerr << "Invalid index in solution! Index: " << solution[i] << " or " << solution[i + 1] << std::endl;
            return -1;  // Zwróć wartość sygnalizującą błąd
        }

        // Obliczanie kosztu
        total_distance += distances[solution[i]][solution[i + 1]];
    }
    total_distance += distances[solution.back()][solution[0]];  // Powrót do miasta początkowego
    std::cout << "Total distance: " << total_distance << std::endl;
    return total_distance;
}

std::vector<int> SimulatedAnnealing::get_neighbor(const std::vector<int>& current_solution) {
    std::cout << "Generating neighbor for current solution..." << std::endl;

    std::vector<int> new_solution = current_solution;

    // Wybierz dwa losowe miasta do zamiany (sprawdź, czy indeksy są poprawne)
    int city1 = std::rand() % new_solution.size();
    int city2 = std::rand() % new_solution.size();

    std::cout << "Swapping city " << city1 << " with city " << city2 << std::endl;

    // Sprawdzenie poprawności indeksów
    if (city1 >= new_solution.size() || city2 >= new_solution.size()) {
        std::cerr << "Invalid index in neighbor generation! city1: " << city1 << ", city2: " << city2 << std::endl;
        return current_solution;  // Zwróć niezmodyfikowane rozwiązanie
    }

    std::swap(new_solution[city1], new_solution[city2]);
    return new_solution;
}

void SimulatedAnnealing::print_distance_matrix() {
    std::cout << "Distance Matrix:" << std::endl;
    for (size_t i = 0; i < distances.size(); ++i) {
        for (size_t j = 0; j < distances[i].size(); ++j) {
            std::cout << distances[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

// Dodaj nową funkcję do wykonywania pojedynczej iteracji
std::vector<int> SimulatedAnnealing::iterate() {
    // Logowanie iteracji dla debugowania
    std::cout << "Iteration: " << current_iteration << ", Current Temperature: " << temperature << std::endl;

    // Oblicz koszt bieżącego rozwiązania
    double current_cost = calculate_cost(current_solution);

    // Znajdź sąsiada
    std::vector<int> new_solution = get_neighbor(current_solution);
    double new_cost = calculate_cost(new_solution);

    // Sprawdź, czy zaakceptować nowe rozwiązanie
    if (accept_solution(current_cost, new_cost)) {
        current_solution = new_solution;
    }

    // Schładzanie
    cool_down();
    current_iteration++;  // Zwiększ liczbę iteracji

    // Zwróć bieżące rozwiązanie
    return current_solution;
}

int SimulatedAnnealing::get_max_iterations() const {
    return max_iterations;
}
