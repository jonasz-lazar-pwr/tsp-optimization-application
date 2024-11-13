// src/tsp_algorithms/sa/enums/NeighborSelectionMethodSA.h

#ifndef NEIGHBORSELECTIONMETHODSA_H
#define NEIGHBORSELECTIONMETHODSA_H


// Enum defining the type of move in Simulated Annealing
enum class NeighborSelectionMethodSA {
    SWAP,    // Swap two cities
    INSERT,  // Insert one city at a different position
    INVERT   // Invert a segment of the tour
};

#endif //NEIGHBORSELECTIONMETHODSA_H
