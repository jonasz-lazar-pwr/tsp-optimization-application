// src/tsp_algorithms/ts/utils/MoveHashUtils.h

#ifndef MOVE_HASH_UTILS_H
#define MOVE_HASH_UTILS_H

#include <tuple>
#include <functional>


// Hash function for std::pair, used for Swap moves
struct hash_pair {
    template <typename T1, typename T2>
    std::size_t operator()(const std::pair<T1, T2>& p) const {
        auto hash1 = std::hash<T1>{}(p.first);
        auto hash2 = std::hash<T2>{}(p.second);
        return hash1 ^ hash2;
    }
};

// Hash function for std::tuple, used for 2-opt moves
struct hash_tuple {
    template <typename T1, typename T2, typename T3, typename T4>
    std::size_t operator()(const std::tuple<T1, T2, T3, T4>& t) const {
        auto hash1 = std::hash<T1>{}(std::get<0>(t));
        auto hash2 = std::hash<T2>{}(std::get<1>(t));
        auto hash3 = std::hash<T3>{}(std::get<2>(t));
        auto hash4 = std::hash<T4>{}(std::get<3>(t));
        return hash1 ^ hash2 ^ hash3 ^ hash4;
    }
};

#endif // MOVE_HASH_UTILS_H
