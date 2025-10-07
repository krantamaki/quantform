#ifndef LALIB_HPP
#define LALIB_HPP


/*
 * This is the file one should include when using lalib functions
 */


// Value by which index can be offset. Default 0 means that indexing starts at zero, 1 from one etc.
#define INDEX_OFFSET 0


// The datatype used in the tests
#define TEST_TYPE double


// The default maximum number of iterations for solvers
#define MAX_ITER 1e6


// The default tolerance for residual for solvers
#define TOLERANCE 1e-6


// The default print frequency for solvers
#define PRINT_FREQUENCY 100


// Include ulib
#include "../ulib/ulib.hpp"


// Include the sparse matrix implementation
#include "src/Matrix.hpp" 


// Include the vector implementation
#include "src/Vector.hpp" 


// Include the linear solvers
#include "src/LinearSolver.hpp"




namespace lalib {

  // Define the test suite here for ease of access
  ulib::TestSuite tests = ulib::TestSuite("lalib");

}


#endif