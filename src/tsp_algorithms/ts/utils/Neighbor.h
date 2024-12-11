// src/tsp_algorithms/ts/utils/Neighbor.h

#ifndef NEIGHBOR_H
#define NEIGHBOR_H

#include <vector>
#include <variant>


// A struct representing a neighbor solution and the move (either Swap or 2-opt) that generated it
struct Neighbor {
    std::vector<int> solution;  // New solution (path)
    std::variant<std::pair<int, int>, std::pair<std::pair<int, int>, std::pair<int, int>>> move;  // Move: Swap or 2-opt
    int cost;  // Cost of the neighbor solution
};

#endif // NEIGHBOR_H