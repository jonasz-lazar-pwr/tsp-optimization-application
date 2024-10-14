// src/algorithms/cpp/TS/enums/TabuListLimitType.h

#ifndef TABU_LIST_LIMIT_TYPE_H
#define TABU_LIST_LIMIT_TYPE_H

// Enum defining the method to calculate Tabu List limit
enum class TabuListLimitType {
    N,          // Limit is n (number of cities)
    SQRT_N,     // Limit is sqrt(n)
    THREE_N,    // Limit is 3n
    N_SQUARED,  // Limit is n^2
    CUSTOM      // User-defined limit
};

#endif // TABU_LIST_LIMIT_TYPE_H
