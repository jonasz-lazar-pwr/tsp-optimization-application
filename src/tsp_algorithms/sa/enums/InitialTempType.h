// src/algorithms/cpp/sa/enums/InitialTempType.h

#ifndef INITIALTEMPTYPE_H
#define INITIALTEMPTYPE_H

// Enum defining the method for generating the initial temperature
enum class InitialTempType {
  AVG, // Average distance-based initial temperature
  MAX, // Maximum distance-based initial temperature
  SAMPLING // Sampling-based initial temperature (using random cost differences)
};

#endif //INITIALTEMPTYPE_H
