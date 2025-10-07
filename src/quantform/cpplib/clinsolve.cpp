#include <string>
#include <vector>
#include <map>
#include <cmath>

#include "lalib/lalib.hpp"  // Also includes ulib


/**
 * Compile to a shared object at the main src directory with:
 * 
 * > g++ -c -fPIC -static -std=c++17 -mavx -fopenmp -Wall quantform/cpplib/clinsolve.cpp -lm -o quantform/cpplib/clinsolve.o
 * > g++ -shared -o quantform/cpplib/clinsolve.so quantform/cpplib/clinsolve.o -lgomp
 * 
 * (note that -lgomp links OpenMP into the shared object and for whatever reason needs to be at the end of the line)
 * 
 */


using val_t = double;


extern "C" {

  void linsolve(int rows, int cols, int nValues, double* values, int* rowPointers, int* columnIndexes, double* rhsVector, double* x0Vector, char* solverMethod) {

    ulib::verbosity(2);
    //ulib::verbosity(5);
    //ulib::logfile("log.txt");

    std::vector<double> valueVec(values, values + nValues);
    std::vector<int> rowPointerVec(rowPointers, rowPointers + (rows + 1));
    std::vector<int> colIndexVec(columnIndexes, columnIndexes + nValues);
    std::vector<double> rhsVec(rhsVector, rhsVector + rows);
    std::vector<double> x0Vec(x0Vector, x0Vector + cols);

    lalib::Matrix<val_t> A  = lalib::Matrix<val_t>(rows, cols, valueVec, colIndexVec, rowPointerVec);
    lalib::Vector<val_t> b  = lalib::Vector<val_t>(rows, rhsVec);
    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(cols, x0Vec);

    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve(solverMethod, x0, 1000, 1e-7, PRINT_FREQUENCY, 1.0);

    lalib::Vector<val_t> x = solver.getSolution();
    

    for (int i = 0; i < cols; i++) {
      x0Vector[i] = x(i);
    }

  }

}