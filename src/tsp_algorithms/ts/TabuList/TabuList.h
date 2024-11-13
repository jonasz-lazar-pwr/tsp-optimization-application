// src/tsp_algorithms/ts/TabuList/TabuList.h

#ifndef TABU_LIST_H
#define TABU_LIST_H

#include "TenureTypeTS.h"
#include <random>
#include <map>


// Class representing the Tabu List
class TabuList {
public:
    // Constructor with parameters for the Tabu List
    explicit TabuList(int constant_tenure, std::pair<int, int> random_tenure_range,
                      TenureTypeTS tenure_type, int limit);

    // Add a move to the Tabu List
    void add_move(int city1, int city2);

    // Check if a move is tabu
    bool is_tabu(int city1, int city2) const;

    // Decrease tenure of all moves on the Tabu List
    void decrement_tenure();

private:
    std::multimap<int, std::pair<int, int>> tabu_map;  // Stores moves with their tenure
    int constant_tenure;                               // Constant tenure duration
    std::pair<int, int> random_tenure_range;           // Range for random tenure
    TenureTypeTS tenure_type;                          // Type of tenure (CONSTANT or RANDOM)
    std::mt19937 rng;                                  // Random number generator
    int limit;                                         // Maximum size of the Tabu List

    // Get tenure value (constant or random based on the tenure type)
    int get_tenure();

    // Ensure that the Tabu List doesn't exceed its limit
    void enforce_limit();
};

#endif // TABU_LIST_H
