// src/algorithms/cpp/sa/enums/TempDecayType.h

#ifndef TEMPDECAYTYPE_H
#define TEMPDECAYTYPE_H

// Enum defining the method for temperature decay in Simulated Annealing
enum class TempDecayType {
    GEO,   // Geometric decay
    LOG,   // Logarithmic decay
    LINE   // Linear decay
};

#endif //TEMPDECAYTYPE_H
