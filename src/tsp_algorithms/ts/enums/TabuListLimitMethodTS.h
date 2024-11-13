// src/tsp_algorithms/ts/enums/TabuListLimitMethodTS.h

#ifndef TABULISTLIMITMETHODTS_H
#define TABULISTLIMITMETHODTS_H


// Enum defining the method to calculate Tabu List limit
enum class TabuListLimitMethodTS {
    N,          // Limit is n (number of cities)
    SQRT_N,     // Limit is sqrt(n)
    THREE_N,    // Limit is 3n
    N_SQUARED,  // Limit is n^2
    CUSTOM      // User-defined limit
};

#endif // TABULISTLIMITMETHODTS_H
