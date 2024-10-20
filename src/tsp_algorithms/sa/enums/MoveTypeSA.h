// src/algorithms/cpp/sa/enums/MoveTypeSA.h

#ifndef MOVETYPESA_H
#define MOVETYPESA_H

// Enum defining the type of move in Simulated Annealing
enum class MoveTypeSA {
    SWAP,    // Swap two cities
    INSERT,  // Insert one city at a different position
    INVERT   // Invert a segment of the tour
};

#endif //MOVETYPESA_H
