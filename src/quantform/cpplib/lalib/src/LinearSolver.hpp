#ifndef LINEARSOLVER_HPP
#define LINEARSOLVER_HPP

#include <string>
#include <chrono>
#include <math.h>
#include <functional>

#include "../lalib.hpp"
#include "Vector.hpp"
#include "Matrix.hpp"


namespace lalib {


  // The norm that is minimized in least squares
  template <class val_t>
  val_t minimizedNorm(Matrix<val_t> A, Vector<val_t> x, Vector<val_t> b, val_t p = (val_t)2.) {
    return (A.matmul(x) - b).pNorm();
  }


  /*
   * Class for linear solver algorithms.
   * Each algorithm will be implemented as their own method.
   * The solution vector and other useful info like number of iterations taken
   * and the final residual are also stored in the object.
   */
  template <class val_t>
  class LinearSolver {

    protected:

      // These will be filled by the solver method

      // The solution vector
      Vector<val_t> solution;

      // Iterations taken
      int nIterations = -1;

      // The final residual
      val_t residual = -1.;

      // The number of milliseconds taken
      int milliseconds = -1;

      // The given parameter for a solver
      val_t param = -1.;


      // These are filled by constructor method

      // The system matrix
      Matrix<val_t> systemMatrix;

      // The right-hand side vector
      Vector<val_t> rhsVector;


      // These are passed as parameters to solver methods

      // Maximum number of iterations allowed.
      int _maxIter;

      // The tolerance for residual
      val_t _tolerance;

      // The frequency with which residuals are printed. Mainly for debugging
      int _printFrequency;


    public:


      // ====================== CONSTRUCTORS ======================


      // Default constructor
      LinearSolver(void) { }


      // Copying constructor
      LinearSolver(const LinearSolver<val_t>& that) {

        this->solution = that.solution;
        this->nIterations = that.nIterations;
        this->residual = that.residual;
        this->param = that.param;
        this->systemMatrix = that.systemMatrix;
        this->rhsVector = that.rhsVector;
      }


      // Main constructor
      LinearSolver(Matrix<val_t> system, Vector<val_t> rhs) {

        this->systemMatrix = system;
        this->rhsVector = rhs;
      }


      // ====================== SOLVERS ======================


      // Wrapper method for the linear solvers. Requires the initial guess x0 and solver ('CG', 'CGNR', 'TCGNR' or 'IRLS') to be passed
      void solve(std::string solver, Vector<val_t> x0, int maxIter = MAX_ITER, val_t tolerance = TOLERANCE, 
                 int printFrequency = PRINT_FREQUENCY, val_t param = 1.) {

        this->param = param;
        this->_maxIter = maxIter;
        this->_tolerance = tolerance;
        this->_printFrequency = printFrequency;

        auto start = std::chrono::high_resolution_clock::now();

        if ( ulib::toLower(solver) == "cg" ) {
          this->_cgSolve(x0);
        }
        else if ( ulib::toLower(solver) == "cgnr" ) {
          this->_cgnrSolve(x0);
        }
        else if ( ulib::toLower(solver) == "tcgnr" ) {
          this->_tcgnrSolve(x0);
        }
        else if ( ulib::toLower(solver) == "irls" ) {
          this->_irlsSolve(x0);
        }
        else {
          ERROR(ulib::formString("Invalid solver: ", solver, " passed!"));
        }

        auto end = std::chrono::high_resolution_clock::now();

        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        this->milliseconds = (int)duration.count();
      }


      // Sparse conjugate gradient method. To be called by 'solve' method
      void _cgSolve(Vector<val_t> x0) {

        if ( this->systemMatrix.numRows() != x0.len() ||
             this->systemMatrix.numRows() != this->rhsVector.len() ) {
          ERROR("Improper dimensions!");
        }

        if ( this->systemMatrix.numRows() != this->systemMatrix.numCols() ) {
          ERROR("Coefficient matrix must be square!");
        }

        Vector<val_t> xk = Vector<val_t>(x0);
        Vector<val_t> r = this->rhsVector - this->systemMatrix.matmul(xk);
        Vector<val_t> p = Vector<val_t>(r);

        val_t oldResidual = r.dot(r);

        int iter = 0;
        for (; iter <= this->_maxIter; iter++) {

          Vector<val_t> Ap = this->systemMatrix.matmul(p);

          val_t alpha = oldResidual / (p.dot(Ap));

          xk += alpha * p;
          r -= alpha * Ap;

          val_t newResidual = r.dot(r);

          if ( newResidual < this->_tolerance ) {
            LOWPRIORITY(ulib::formString("Iteration: ", iter, " - Residual: ", newResidual, " - Norm: ", 
              minimizedNorm(this->systemMatrix, xk, this->rhsVector)));

            this->solution = xk;
            this->nIterations = iter;
            this->residual = newResidual;
            return;
          }

          val_t beta = newResidual / oldResidual;

          p *= beta;
          p += r;

          oldResidual = newResidual;

          if ( iter % this->_printFrequency == 0 ) {
            if ( ulib::verbosity() >= 4 ) {
              LOWPRIORITY(ulib::formString("Iteration: ", iter, " - Residual: ", newResidual, " - Norm: ", 
                minimizedNorm(this->systemMatrix, xk, this->rhsVector)));
            }
          }

        }

        WARNING(ulib::formString("Solver did not converge to the wanted tolerance (", oldResidual, " > ", this->_tolerance, ")!"));

        this->solution = xk;
        this->nIterations = iter;
        this->residual = oldResidual;
      }


      // CGNR solver subprocess to be called by multiple linear solver methods
      void _cgnrSubprocess(Matrix<val_t> A, Matrix<val_t>A_T, Vector<val_t> b, Vector<val_t> x0) {

        Vector<val_t> xk = Vector<val_t>(x0);
        Vector<val_t> r = A_T.matmul(b) - A_T.matmul(A.matmul(xk));
        Vector<val_t> p = Vector<val_t>(r);

        val_t oldResidual = r.dot(r);

        int iter = 0;
        for (; iter <= this->_maxIter; iter++) {

          Vector<val_t> Ap = A.matmul(p);

          val_t alpha = oldResidual / (Ap.dot(Ap));

          xk += alpha * p;
          r -= alpha * A_T.matmul(Ap);

          val_t newResidual = r.dot(r);

          if ( newResidual < this->_tolerance ) {
            LOWPRIORITY(ulib::formString("Iteration: ", iter, " - Residual: ", newResidual, " - Norm: ", 
              minimizedNorm(A, xk, b)));

            this->solution = xk;
            this->nIterations = iter;
            this->residual = newResidual;
            return;
          }

          val_t beta = newResidual / oldResidual;

          p *= beta;
          p += r;

          oldResidual = newResidual;

          if ( iter % this->_printFrequency == 0 ) {
            if ( ulib::verbosity() >= 4 ) {
              LOWPRIORITY(ulib::formString("Iteration: ", iter, " - Residual: ", newResidual, " - Norm: ", 
                minimizedNorm(A, xk, b)));
            }
          }

        }

        WARNING(ulib::formString("Solver did not converge to the wanted tolerance (", oldResidual, " > ", this->_tolerance, ")!"));

        this->solution = xk;
        this->nIterations = iter;
        this->residual = oldResidual;

      }


      // Weighted CGNR solver subprocess to be called by multiple linear solver methods
      void _wcgnrSubprocess(Vector<val_t> w, Matrix<val_t> A, Matrix<val_t>A_T, Vector<val_t> b, Vector<val_t> x0) {

        // Form the weighting matrices
        Matrix<val_t> W = Matrix<val_t>(w);
        
        std::function<val_t(val_t)> square = [](val_t val) { return std::pow(val, 2.); };
        Vector<val_t> w2 = w.apply(square);

        Matrix<val_t> W2 = Matrix<val_t>(w2);

        // Solve the weighted system
        Vector<val_t> xk = Vector<val_t>(x0);
        Vector<val_t> r = W.matmul(A_T.matmul(b)) - W2.matmul(A_T.matmul(A.matmul(xk)));
        Vector<val_t> p = Vector<val_t>(r);

        val_t oldResidual = r.dot(r);

        int iter = 0;
        for (; iter <= this->_maxIter; iter++) {

          Vector<val_t> Ap = A.matmul(W.matmul(p));

          val_t alpha = oldResidual / (Ap.dot(Ap));

          xk += alpha * p;
          r -= alpha * W.matmul(A_T.matmul(Ap));

          val_t newResidual = r.dot(r);

          if ( newResidual < this->_tolerance ) {
            LOWPRIORITY(ulib::formString("Iteration: ", iter, " - Residual: ", newResidual, " - Norm: ", 
              minimizedNorm(A, xk, b)));

            this->solution = xk;
            this->nIterations = iter;
            this->residual = newResidual;
            return;
          }

          val_t beta = newResidual / oldResidual;

          p *= beta;
          p += r;

          oldResidual = newResidual;

          if ( iter % this->_printFrequency == 0 ) {
            if ( ulib::verbosity() >= 4 ) {
              LOWPRIORITY(ulib::formString("Iteration: ", iter, " - Residual: ", newResidual, " - Norm: ", 
                minimizedNorm(A, xk, b)));
            }
          }

        }

        WARNING(ulib::formString("Solver did not converge to the wanted tolerance (", oldResidual, " > ", this->_tolerance, ")!"));

        this->solution = xk;
        this->nIterations = iter;
        this->residual = oldResidual;

      }


      // Sparse conjugate gradient on normal equations method. To be called by 'solve' method
      void _cgnrSolve(Vector<val_t> x0) {

        if ( this->systemMatrix.numCols() != x0.len() ||
             this->systemMatrix.numRows() != this->rhsVector.len() ) {
          ERROR("Improper dimensions!");
        }

        DEBUG("Calling transpose...");
        auto start = std::chrono::high_resolution_clock::now();
        // TODO: Fix the fast transpose
        //Matrix<val_t> systemMatrixT = this->systemMatrix.T();
        Matrix<val_t> systemMatrixT = this->systemMatrix.naiveTranspose();
        auto end = std::chrono::high_resolution_clock::now();
        DEBUG("Success!")

        LOWPRIORITY(ulib::formString("Time taken on transpose: ", (int)std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count(), " ms"));

        this->_cgnrSubprocess(this->systemMatrix, systemMatrixT, this->rhsVector, x0);

      }


      // Sparse Tikhonov regularized CGNR. To be called by 'solve' method
      void _tcgnrSolve(Vector<val_t> x0) {
        
        if ( this->systemMatrix.numCols() != x0.len() ||
             this->systemMatrix.numRows() != this->rhsVector.len() ) {
          ERROR("Improper dimensions!");
        }

        Matrix<val_t> newSysMatrix = this->systemMatrix.addRows(Matrix<val_t>(this->systemMatrix.numCols(), this->systemMatrix.numCols(), sqrt(this->param)));
        Vector<val_t> newRHSVector = this->rhsVector.addRows(Vector<val_t>(this->systemMatrix.numCols()));

        DEBUG("Calling transpose...");
        auto start = std::chrono::high_resolution_clock::now();
        //Matrix<val_t> systemMatrixT = this->systemMatrix.T();
        Matrix<val_t> newSysMatrixT = newSysMatrix.naiveTranspose();
        auto end = std::chrono::high_resolution_clock::now();
        DEBUG("Success!")

        LOWPRIORITY(ulib::formString("Time taken on transpose: ", (int)std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count(), " ms"));

        this->_cgnrSubprocess(newSysMatrix, newSysMatrixT, newRHSVector, x0);

      }


      // Sparse iteratively reweighted least squares. To be called by 'solve' method
      void _irlsSolve(Vector<val_t> x0) {

        if ( this->systemMatrix.numCols() != x0.len() ||
             this->systemMatrix.numRows() != this->rhsVector.len() ) {
          ERROR("Improper dimensions!");
        }

        DEBUG("Calling transpose...");
        auto start = std::chrono::high_resolution_clock::now();
        //Matrix<val_t> systemMatrixT = this->systemMatrix.T();
        Matrix<val_t> systemMatrixT = this->systemMatrix.naiveTranspose();
        auto end = std::chrono::high_resolution_clock::now();
        DEBUG("Success!")

        LOWPRIORITY(ulib::formString("Time taken on transpose: ", (int)std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count(), " ms"));
        int irlsIter = 0;
        val_t irlsNorm = 1000.;

        // Initial assumption is that W = I so just use the standard CGNR
        this->_cgnrSubprocess(this->systemMatrix, systemMatrixT, this->rhsVector, x0);
        Vector xk = this->solution;

        irlsNorm = minimizedNorm(this->systemMatrix, xk, this->rhsVector, this->param);
        irlsIter++; 


        val_t param = this->param;
        val_t tol   = this->_tolerance;

        std::function<val_t(val_t)> weight = [&param, &tol](val_t val) { return std::max(std::pow(std::abs(val), (param - 2.) / param), 
                                                                                         std::pow(std::abs(tol), (param - 2.) / param)); };

        while ( irlsNorm > this->_tolerance && irlsIter < this->_maxIter ) {

          Vector<val_t> w = xk.apply(weight);
          this->_wcgnrSubprocess(w, this->systemMatrix, systemMatrixT, this->rhsVector, xk);
          Vector xk = this->solution;

          irlsNorm = minimizedNorm(this->systemMatrix, xk, this->rhsVector, this->param);
          irlsIter++; 

        }

        if ( irlsIter == this->_maxIter ) {
          WARNING(ulib::formString("Solver did not converge to the wanted tolerance (", irlsNorm, " > ", this->_tolerance, ")!"));
        }

        this->solution = xk;
        this->residual = irlsNorm;
        this->nIterations = irlsIter;

      }


      Vector<val_t> getSolution() {
        if ( &this->solution ) {
          return this->solution;
        }

        ERROR("System has not been solved yet!");
        return this->solution;  // Should not get here
      }


      int getSolveTime() {
        if ( this->milliseconds >= 0 ) {
          return this->milliseconds;
        }

        ERROR("System has not been solved yet!");
        return this->milliseconds;  // Should not get here
      }

  };

}


#endif