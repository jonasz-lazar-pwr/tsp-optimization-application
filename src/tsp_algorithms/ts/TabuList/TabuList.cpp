// src/algorithms/cpp/TS/TabuList/TabuList.cpp

#include "TabuList.h"


// --- Constructor ---
/*
 * Initializes the Tabu List with the given tenure, random tenure range, tenure type, and limit.
 */
TabuList::TabuList(int tenure, std::pair<int, int> random_tenure_range, TenureType tenure_type, int limit):
    tenure(tenure), random_tenure_range(random_tenure_range),
    tenure_type(tenure_type), rng(std::random_device{}()), limit(limit) {}

// --- Get Tenure ---
/*
 * Returns the tenure value, either constant or random based on the tenure type.
 */
int TabuList::get_tenure() {
    if (tenure_type == TenureType::RANDOM) {
        std::uniform_int_distribution<int> dist(random_tenure_range.first, random_tenure_range.second);
        return dist(rng);
    }
    return tenure;
}

// --- Enforce Limit ---
/*
 * Ensures that the Tabu List size does not exceed the specified limit.
 * Removes the oldest move if the limit is exceeded.
 */
void TabuList::enforce_limit() {
    if (tabu_map.size() > limit) {
        tabu_map.erase(tabu_map.begin());  // Remove the move with the smallest tenure
    }
}

// --- Add Move ---
/*
 * Adds a move to the Tabu List with the appropriate tenure.
 * The move is normalized to ensure the smaller city is first.
 */
void TabuList::add_move(int city1, int city2) {
    if (city1 > city2) {
        std::swap(city1, city2);  // Ensure the smaller city is always first
    }
    tabu_map.insert({get_tenure(), {city1, city2}});  // Insert the move with tenure

    // Ensure the Tabu List size does not exceed the limit
    enforce_limit();
}

// --- Check if Move is Tabu ---
/*
 * Checks if a move is tabu by looking for the move in the Tabu List.
 */
bool TabuList::is_tabu(int city1, int city2) const {
    if (city1 > city2) {
        std::swap(city1, city2);  // Normalize the move
    }

    for (const auto& entry : tabu_map) {
        if (entry.second.first == city1 && entry.second.second == city2) {
            return true;
        }
    }
    return false;
}

// --- Decrement Tenure ---
/*
 * Decreases the tenure of all moves in the Tabu List.
 * Removes moves whose tenure reaches zero.
 */
void TabuList::decrement_tenure() {
    std::vector<std::pair<int, std::pair<int, int>>> updated_moves;

    // Decrement tenure and remove moves with tenure <= 0
    for (auto it = tabu_map.begin(); it != tabu_map.end();) {
        int new_tenure = it->first - 1;
        if (new_tenure > 0) {
            updated_moves.push_back({new_tenure, it->second});
        }
        it = tabu_map.erase(it);
    }

    // Insert updated moves back into the Tabu List
    for (const auto& move : updated_moves) {
        tabu_map.insert(move);
    }
}

// Decrement tenure and remove moves with tenure <= 0
// for (auto it = tabu_map.begin(); it != tabu_map.end();) {
//     int new_tenure = it->first - 1;
//     if (new_tenure <= 0) {
//         it = tabu_map.erase(it);  // Remove the move
//     } else {
//         // Update the move with the new tenure
//         updated_moves.push_back({new_tenure, it->second});
//         it = tabu_map.erase(it); // Remove the old move
//     }
// }