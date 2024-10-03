// src/algorithms/cpp/SA/SimulatedAnnealing.h

#ifndef SIMULATED_ANNEALING_H
#define SIMULATED_ANNEALING_H

#include <vector>

class SimulatedAnnealing {
public:
    // Konstruktor - inicjalizuje algorytm z podaną temperaturą, liczbą iteracji i macierzą odległości
    SimulatedAnnealing(double temp, int iter, const std::vector<std::vector<double>>& dist_matrix);

    // Getter for max_iterations
    int get_max_iterations() const;

    // Metoda wykonująca algorytm SA, zwracająca koszt końcowy rozwiązania
    double run();

    std::vector<int> iterate();

private:
    // Aktualna liczba iteracji
    int current_iteration = 0;  // Dodaj tę zmienną

    // Aktualna temperatura
    double temperature;

    // Maksymalna liczba iteracji
    int max_iterations;

    // Macierz odległości pomiędzy miastami
    std::vector<std::vector<double>> distances;

    // Bieżące rozwiązanie (kolejność odwiedzania miast)
    std::vector<int> current_solution;

    // Oblicza koszt (długość trasy) dla danego rozwiązania
    double calculate_cost(const std::vector<int>& solution);

    // Wybiera sąsiednie rozwiązanie (np. przez zamianę dwóch miast)
    std::vector<int> get_neighbor(const std::vector<int>& current_solution);

    void print_distance_matrix();

    // Sprawdza, czy zaakceptować nowe rozwiązanie (z prawdopodobieństwem zależnym od temperatury)
    bool accept_solution(double current_cost, double new_cost);

    // Obniża temperaturę w procesie schładzania (cooling schedule)
    void cool_down();
};

#endif // SIMULATED_ANNEALING_H
